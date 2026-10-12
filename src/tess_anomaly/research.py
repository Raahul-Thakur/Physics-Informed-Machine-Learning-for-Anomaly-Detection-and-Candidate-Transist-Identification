"""Frozen unsupervised experiments with target-disjoint calibration and evaluation."""

import argparse
import copy
import hashlib
import importlib.metadata
import json
import logging
import shutil
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import yaml

from .anomaly import isolation_forest, lof
from .coherence import COHERENCE, COMPACT, coherence_features
from .config import load_config
from .dataset import fit_transform
from .evaluation import ranking_metrics, target_scores
from .features import FAMILIES
from .utils import write_json

LOG = logging.getLogger(__name__)
REPRESENTATIONS = {**FAMILIES, "compact": COMPACT, "extended": FAMILIES["all"] + COHERENCE}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_digest() -> str:
    h = hashlib.sha256()
    for p in sorted(Path(__file__).parent.rglob("*.py")):
        h.update(p.name.encode())
        h.update(p.read_bytes())
    return h.hexdigest()


def versions() -> dict:
    return {
        p: importlib.metadata.version(p)
        for p in ["numpy", "pandas", "scipy", "astropy", "scikit-learn", "joblib"]
    }


def enriched_features(root: Path) -> pd.DataFrame:
    """Reuse existing BLS and photometry; never replace baseline outputs."""
    frame = pd.read_csv(root / "data/features/features.csv")
    if frame.duplicated(["tic_id", "sector"]).any():
        raise ValueError("Duplicate target-sector feature rows")
    additions = []
    for i, row in enumerate(frame.to_dict("records")):
        with np.load(root / row["processed_path"]) as curve:
            additions.append(coherence_features(dict(curve), row))
        if (i + 1) % 100 == 0:
            LOG.info("Coherence features: %s/%s curves", i + 1, len(frame))
    return pd.concat([frame, pd.DataFrame(additions)], axis=1)


def one_sector(frame: pd.DataFrame) -> pd.DataFrame:
    """Coverage-only choice, without scores or catalogue labels."""
    return (
        frame.sort_values(
            ["tic_id", "n_observations", "baseline_days", "sector"],
            ascending=[True, False, False, True],
            kind="stable",
        )
        .drop_duplicates("tic_id")
        .sort_values(["tic_id", "sector"])
        .reset_index(drop=True)
    )


def percentile(reference: np.ndarray, values: np.ndarray) -> np.ndarray:
    """Fixed calibration empirical CDF with midpoint ties; no test-batch ranking."""
    reference = np.sort(np.asarray(reference)[np.isfinite(reference)])
    if len(reference) < 3:
        raise ValueError("At least three finite calibration scores required")
    values = np.asarray(values)
    result = (
        np.searchsorted(reference, values, side="left")
        + np.searchsorted(reference, values, side="right")
    ) / (2 * len(reference))
    return np.where(np.isfinite(values), result, np.nan)


def fit_bundle(
    training: pd.DataFrame, calibration: pd.DataFrame, cfg: dict, protocol: dict
) -> dict:
    if set(training.tic_id) & set(calibration.tic_id):
        raise ValueError("Training and calibration targets overlap")
    if min(training.tic_id.nunique(), calibration.tic_id.nunique()) < 3:
        raise ValueError("Need at least three targets in both training and calibration")
    models = {}
    for family in protocol["families"]:
        model_cfg = dict(cfg["models"])
        # Legacy families retain their original feature contracts for comparison.
        if family in {"compact", "extended"}:
            model_cfg["correlation_threshold"] = protocol["correlation_threshold"]
        transform, matrix = fit_transform(training, model_cfg, columns=REPRESENTATIONS[family])
        forest, _ = isolation_forest.fit(matrix, model_cfg["isolation_forest"], cfg["random_seed"])
        local = lof.fit_novelty(matrix, model_cfg["lof"])
        x_cal = transform.transform(calibration)
        raw = {
            "isolation_forest_score": -forest.score_samples(x_cal),
            "lof_score": lof.score_unseen(local, x_cal),
        }
        ensemble = np.mean([percentile(v, v) for v in raw.values()], axis=0)
        models[family] = dict(
            transform=transform,
            forest=forest,
            lof=local,
            calibration=raw,
            ensemble_calibration=ensemble,
            bls_calibration=calibration.depth_snr.to_numpy(),
        )
    return dict(
        models=models,
        protocol=protocol,
        cfg=cfg,
        training_ids=sorted(training.tic_id.unique().tolist()),
        calibration_ids=sorted(calibration.tic_id.unique().tolist()),
    )


def score_bundle(bundle: dict, frame: pd.DataFrame, independent: bool = True) -> dict:
    if independent and set(frame.tic_id) & set(bundle["development_ids"]):
        raise ValueError("Independent evaluation contains previously inspected development targets")
    outputs = {}
    for family, model in bundle["models"].items():
        x = model["transform"].transform(frame)
        result = frame.copy()
        result["isolation_forest_score"] = -model["forest"].score_samples(x)
        result["lof_score"] = lof.score_unseen(model["lof"], x)
        result["ensemble_score"] = np.mean(
            [
                percentile(model["calibration"][c], result[c].to_numpy())
                for c in ["isolation_forest_score", "lof_score"]
            ],
            axis=0,
        )
        result["hybrid_score"] = (
            percentile(model["bls_calibration"], result.depth_snr.to_numpy())
            + percentile(model["ensemble_calibration"], result.ensemble_score.to_numpy())
        ) / 2
        outputs[family] = result
    return outputs


def eligibility(frame: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """Representative-period grid eligibility, not actual transit visibility."""
    caps = np.minimum(
        cfg["bls"]["max_period_days"], frame.baseline_days / cfg["bls"]["min_transits"]
    )
    valid = frame.catalog_period.gt(0) & frame.catalog_period.notna()
    inside = (
        valid
        & frame.catalog_period.ge(cfg["bls"]["min_period_days"])
        & frame.catalog_period.le(caps)
    )
    result = frame[["tic_id", "label", "catalog_period"]].copy()
    result["search_eligible"] = inside
    result["period_known"] = valid
    return result.groupby("tic_id", as_index=False).agg(
        label=("label", "first"),
        catalog_period=("catalog_period", "first"),
        search_eligible=("search_eligible", "any"),
        period_known=("period_known", "any"),
    )


def complement_selection(
    targets: pd.DataFrame, budget: int, bls_fraction: float
) -> tuple[list, list]:
    if not 0 <= bls_fraction <= 1 or budget < 1:
        raise ValueError("Invalid complement budget or fraction")
    if targets.tic_id.duplicated().any():
        raise ValueError("Complementarity requires unique targets")
    if not np.isfinite(targets[["depth_snr", "ensemble_score"]]).all().all():
        raise ValueError("Complementarity requires finite BLS and anomaly scores")
    k = min(budget, len(targets))
    bls = targets.sort_values(["depth_snr", "tic_id"], ascending=[False, True]).tic_id.tolist()
    n_bls = int(np.floor(k * bls_fraction))
    base = bls[:n_bls]
    extra = (
        targets[~targets.tic_id.isin(base)]
        .sort_values(["ensemble_score", "tic_id"], ascending=[False, True])
        .tic_id.tolist()[: k - n_bls]
    )
    return bls[:k], base + extra


def complement_metrics(targets: pd.DataFrame, protocol: dict) -> tuple[dict, pd.DataFrame]:
    baseline, combined = complement_selection(targets, protocol["budget"], protocol["bls_fraction"])
    members = targets[["tic_id", "label"]].copy()
    members["bls_selected"] = members.tic_id.isin(baseline)
    members["complement_selected"] = members.tic_id.isin(combined)
    positive = members.label.eq("planet")
    difference = positive.to_numpy() * (
        members.complement_selected.to_numpy().astype(int)
        - members.bls_selected.to_numpy().astype(int)
    )
    rng = np.random.default_rng(protocol["bootstrap_seed"])
    bootstrap = np.array(
        [
            rng.choice(difference, len(difference), replace=True).sum()
            for _ in range(protocol["bootstrap_repeats"])
        ]
    )
    low, high = np.quantile(bootstrap, [0.025, 0.975])
    return dict(
        requested_budget=protocol["budget"],
        effective_budget=len(baseline),
        bls_recovered=int((positive & members.bls_selected).sum()),
        complement_recovered=int((positive & members.complement_selected).sum()),
        additional_hosts=int(
            (positive & members.complement_selected & ~members.bls_selected).sum()
        ),
        lost_hosts=int((positive & ~members.complement_selected & members.bls_selected).sum()),
        net_recovery_difference=int(difference.sum()),
        conditional_bootstrap_low=float(low),
        conditional_bootstrap_high=float(high),
        uncertainty_note="Paired target bootstrap conditional on fixed inspection lists; excludes model-fitting uncertainty",
    ), members


def evaluate_scores(scores: dict, bundle: dict, destination: Path, mode: str) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    metrics, complements, coverage = [], [], []
    for family, frame in scores.items():
        frame.to_csv(destination / f"scores_{family}.csv", index=False)
        for exposure, selected in [("all_sectors", frame), ("one_sector", one_sector(frame))]:
            targets = target_scores(selected)
            grid = eligibility(selected, bundle["cfg"])
            eligible_ids = set(grid.loc[grid.label.eq("planet") & grid.search_eligible, "tic_id"])
            grid["family"], grid["exposure"] = family, exposure
            coverage.append(grid)
            table = ranking_metrics(targets, bundle["cfg"]["evaluation"])
            table["eligible_positive_total"] = len(eligible_ids)
            counts = []
            for row in table.to_dict("records"):
                ids = (
                    targets.sort_values([row["method"], "tic_id"], ascending=[False, True])
                    .head(row["k"])
                    .tic_id
                )
                counts.append(len(set(ids) & eligible_ids))
            table["eligible_positive_recovered"] = counts
            table["eligible_positive_recall"] = (
                np.array(counts) / len(eligible_ids) if eligible_ids else np.nan
            )
            table["family"], table["exposure"] = family, exposure
            metrics.append(table)
            comparison, members = complement_metrics(targets, bundle["protocol"])
            comparison.update(family=family, exposure=exposure)
            complements.append(comparison)
            members.to_csv(destination / f"inspection_{family}_{exposure}.csv", index=False)
    pd.concat(metrics).to_csv(destination / "metrics.csv", index=False)
    pd.concat(coverage).to_csv(destination / "search_eligibility.csv", index=False)
    pd.DataFrame(complements).to_csv(destination / "complementarity.csv", index=False)
    first = next(iter(scores.values()))
    one_sector(first)[["tic_id", "sector", "n_observations", "baseline_days"]].to_csv(
        destination / "coverage_selected_sectors.csv", index=False
    )
    summary = (
        f"# {mode}\n\nScored {first.tic_id.nunique()} targets / {len(first)} curves.\n\n"
        f"Prespecified primary family: {bundle['protocol']['primary_family']}. "
        "Other families are comparisons; do not select a new winner using independent results.\n\n"
        "Training and calibration exclude evaluation targets in independent mode. Labels are used only in metrics. "
        "The choice of the compact experiment was informed by earlier labelled development results; "
        "model fitting and redundancy selection remain unsupervised.\n\n"
        "One-sector selection uses most valid cadences, then longest baseline, then smallest sector number, "
        "without labels or scores. Models are unchanged between exposure comparisons.\n\n"
        "Eligible-positive recall retains the entire inspection pool and changes only the positive denominator. "
        "It uses each host's representative period and the effective per-sector grid cap, not epoch visibility "
        "or completeness across all planets. Out-of-grid and missing-period hosts remain in full metrics.\n\n"
        "Complementarity uses the frozen BLS allocation plus additional anomaly-ranked unique targets. "
        "Bootstrap intervals are conditional on those fixed lists, not model-refitting uncertainty. "
        "Catalogue recovery is not validated planet purity or measured human inspection time.\n\n"
        "Development calibration results are not independent evidence. Unlabelled high-ranked objects "
        "remain inspection candidates. Feature proxies are neither causal attributions nor calibrated significance.\n"
    )
    (destination / "report.md").write_text(summary, encoding="utf-8")


def freeze(config: Path, protocol_path: Path, destination: Path) -> None:
    if destination.exists():
        raise ValueError("Freeze directory already exists; use a new version, never overwrite")
    cfg = load_config(config)
    protocol = yaml.safe_load(protocol_path.read_text())
    cfg["evaluation"]["top_k"] = sorted(set(cfg["evaluation"]["top_k"] + [protocol["budget"]]))
    if protocol["primary_family"] not in protocol["families"]:
        raise ValueError("Primary family must be included")
    if not 0 < protocol["calibration_fraction"] < 1:
        raise ValueError("Invalid calibration fraction")
    if cfg["models"]["autoencoder"]["enabled"]:
        raise ValueError("Frozen workflow currently supports IF and novelty LOF only")
    if not all(cfg["models"][k]["enabled"] for k in ["isolation_forest", "lof"]):
        raise ValueError("The frozen protocol requires both IF and novelty LOF")
    if (
        not 0 <= protocol["bls_fraction"] <= 1
        or protocol["budget"] < 1
        or protocol["bootstrap_repeats"] < 2
    ):
        raise ValueError("Invalid inspection or bootstrap settings")
    root = Path(cfg["root"])
    frame = enriched_features(root)
    ids = np.sort(frame.tic_id.unique())
    rng = np.random.default_rng(cfg["random_seed"])
    shuffled = rng.permutation(ids)
    n_cal = max(3, int(np.ceil(len(ids) * protocol["calibration_fraction"])))
    calibration_ids = set(shuffled[:n_cal])
    # A single calibration curve per target limits calibration exposure imbalance.
    calibration = one_sector(frame[frame.tic_id.isin(calibration_ids)])
    training = frame[~frame.tic_id.isin(calibration_ids)].sort_values(["tic_id", "sector"])
    bundle = fit_bundle(training, calibration, cfg, protocol)
    sample = pd.read_csv(root / "data/catalog/sample.csv")
    inspected = set(ids) | set(sample.tic_id)
    for relative in protocol.get("additional_development_samples", []):
        inspected.update(pd.read_csv(config.resolve().parent.parent / relative).tic_id)
    bundle["development_ids"] = sorted(inspected)
    bundle["source_digest"] = source_digest()
    destination.mkdir(parents=True)
    frame.to_csv(destination / "development_features.csv", index=False)
    joblib.dump(bundle, destination / "frozen_models.joblib")
    pd.DataFrame({"tic_id": bundle["development_ids"]}).to_csv(
        destination / "excluded_tics.csv", index=False
    )
    contract = dict(
        frozen_at_utc=datetime.now(timezone.utc).isoformat(),
        package_versions=versions(),
        source_digest=bundle["source_digest"],
        model_sha256=digest(destination / "frozen_models.joblib"),
        development_feature_sha256=digest(destination / "development_features.csv"),
        development_ids=bundle["development_ids"],
        training_ids=bundle["training_ids"],
        calibration_ids=bundle["calibration_ids"],
        protocol=protocol,
        config=cfg,
        representations=REPRESENTATIONS,
        selection_note="Compact experiment motivated by labelled development results; no independent results used",
    )
    write_json(destination / "protocol.json", contract)
    shutil.copytree(
        Path(__file__).parent,
        destination / "source_snapshot" / "tess_anomaly",
        ignore=shutil.ignore_patterns("__pycache__"),
    )
    for family, model in bundle["models"].items():
        model["transform"].missingness.to_csv(
            destination / f"feature_selection_{family}.csv", index=False
        )
    evaluate_scores(
        score_bundle(bundle, calibration, independent=False),
        bundle,
        destination / "development_calibration",
        "Development calibration diagnostics — not independent",
    )
    LOG.info(
        "Frozen experiment saved to %s; independent evaluation has NOT been performed", destination
    )


def load_frozen(destination: Path) -> dict:
    contract = json.loads((destination / "protocol.json").read_text())
    if contract["source_digest"] != source_digest():
        raise ValueError("Source differs from frozen protocol; use the frozen source version")
    if contract["package_versions"] != versions():
        raise ValueError("Scientific package versions differ from frozen protocol")
    if digest(destination / "frozen_models.joblib") != contract["model_sha256"]:
        raise ValueError("Frozen model checksum mismatch")
    return joblib.load(destination / "frozen_models.joblib")


def evaluate_independent(frozen: Path, root: Path, destination: Path) -> None:
    bundle = load_frozen(frozen)
    cfg = yaml.safe_load((root / "outputs/config_used.yaml").read_text())
    for key in ["preprocessing", "bls"]:
        if cfg[key] != bundle["cfg"][key]:
            raise ValueError(f"Evaluation {key} settings differ from frozen protocol")
    expected_data = {**bundle["cfg"]["data"], **bundle["protocol"].get("evaluation_data", {})}
    for key, value in expected_data.items():
        if cfg["data"].get(key) != value:
            raise ValueError(f"Evaluation sampling field {key} differs from frozen protocol")
    if cfg["random_seed"] != bundle["protocol"].get(
        "evaluation_seed", bundle["cfg"]["random_seed"]
    ):
        raise ValueError("Evaluation sampling seed differs from frozen protocol")
    sample = pd.read_csv(root / "data/catalog/sample.csv")
    features = pd.read_csv(root / "data/features/features.csv")
    if (set(sample.tic_id) | set(features.tic_id)) & set(bundle["development_ids"]):
        raise ValueError("Evaluation sample overlaps the inspected development population")
    if not set(features.tic_id) <= set(sample.tic_id):
        raise ValueError("Feature rows contain targets outside the requested evaluation sample")
    frame = enriched_features(root)
    scores = score_bundle(bundle, frame)
    evaluate_scores(scores, bundle, destination, "Independent target evaluation")
    write_json(
        destination / "evaluation_provenance.json",
        dict(
            protocol_sha256=digest(frozen / "protocol.json"),
            feature_sha256=digest(root / "data/features/features.csv"),
            requested_targets=int(sample.tic_id.nunique()),
            analysed_targets=int(frame.tic_id.nunique()),
            missing_targets=sorted(set(sample.tic_id) - set(frame.tic_id)),
            note="Target-disjoint from development; acquisition and sampling biases remain possible",
        ),
    )


def prepare_evaluation(frozen: Path, workspace: Path, config_path: Path) -> None:
    """Materialize the frozen sampling plan; never fit models on evaluation data."""
    bundle = load_frozen(frozen)
    if config_path.exists() or workspace.exists():
        raise ValueError(
            "Evaluation workspace/config already exists; do not replace a locked sample"
        )
    cfg = copy.deepcopy(bundle["cfg"])
    cfg.pop("root", None)
    cfg["workspace"] = str(workspace.resolve())
    cfg["random_seed"] = bundle["protocol"].get("evaluation_seed", cfg["random_seed"])
    cfg["data"].update(bundle["protocol"].get("evaluation_data", {}))
    cfg["data"]["exclude_tics_csv"] = str((frozen / "excluded_tics.csv").resolve())
    if set(pd.read_csv(cfg["data"]["exclude_tics_csv"]).tic_id) != set(bundle["development_ids"]):
        raise ValueError("Development exclusion list was altered")
    workspace.mkdir(parents=True)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(yaml.safe_dump(cfg), encoding="utf-8")
    LOG.info(
        "Prepared %s. Run only download and features stages before frozen evaluation.", config_path
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    fit = sub.add_parser("freeze")
    fit.add_argument("--config", type=Path, default=Path("config/default.yaml"))
    fit.add_argument("--protocol", type=Path, default=Path("config/research_v2.yaml"))
    fit.add_argument("--output", type=Path, default=Path("experiments/research_v2/frozen"))
    evaluate = sub.add_parser("evaluate")
    evaluate.add_argument("--frozen", type=Path, required=True)
    evaluate.add_argument("--evaluation-workspace", type=Path, required=True)
    evaluate.add_argument("--output", type=Path, required=True)
    prepare = sub.add_parser("prepare-evaluation")
    prepare.add_argument("--frozen", type=Path, required=True)
    prepare.add_argument("--workspace", type=Path, required=True)
    prepare.add_argument("--config-output", type=Path, required=True)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    if args.command == "freeze":
        freeze(args.config, args.protocol, args.output)
    elif args.command == "evaluate":
        evaluate_independent(args.frozen, args.evaluation_workspace, args.output)
    else:
        prepare_evaluation(args.frozen, args.workspace, args.config_output)


if __name__ == "__main__":
    main()
