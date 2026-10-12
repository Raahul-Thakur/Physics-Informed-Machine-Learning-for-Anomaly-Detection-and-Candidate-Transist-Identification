"""Stage CLI, versioned scientific caches, training, evaluation, and reporting."""

import argparse
import hashlib
import importlib.metadata
import json
import logging
import random
from functools import lru_cache
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import yaml

from .anomaly import isolation_forest, lof
from .anomaly.ensemble import ensemble, rank_normalize
from .bls import period_match, search_bls
from .catalog import select_sample
from .config import fingerprint, load_config, prepare
from .dataset import fit_transform
from .download import download_sample
from .evaluation import (
    correlations,
    group_statistics,
    ranking_metrics,
    score_columns,
    target_scores,
)
from .features import FAMILIES, extract_features
from .logging_utils import configure
from .preprocessing import preprocess
from .utils import provenance, synthetic_curve, write_json

LOG = logging.getLogger(__name__)
STAGES = ["download", "preprocess", "bls", "features", "train", "evaluate", "figures", "report"]


@lru_cache(maxsize=1)
def code_hash() -> str:
    digest = hashlib.sha256()
    for path in sorted(Path(__file__).parent.rglob("*.py")):
        digest.update(path.read_bytes())
    for package in ["numpy", "pandas", "scipy", "astropy", "lightkurve", "scikit-learn", "torch"]:
        try:
            digest.update(f"{package}={importlib.metadata.version(package)}".encode())
        except importlib.metadata.PackageNotFoundError:
            digest.update(f"{package}=not-installed".encode())
    return digest.hexdigest()[:16]


def curve_stages(root: Path, cfg: dict, stage: str, force: bool) -> None:
    manifest = pd.read_csv(root / "data/raw/manifest.csv")
    feature_rows, records, failures = [], [], []
    for row in manifest.to_dict("records"):
        try:
            raw_path = root / row["raw_path"]
            key = fingerprint(
                [
                    hashlib.sha256(raw_path.read_bytes()).hexdigest(),
                    cfg["preprocessing"],
                    cfg["bls"],
                    code_hash(),
                ]
            )
            stem = f"tic{int(row['tic_id'])}_s{int(row['sector'])}_{key}"
            processed = root / f"data/processed/{stem}.npz"
            bls_path = root / f"data/cache/{stem}_bls.json"
            power_path = root / f"data/cache/{stem}_power.npz"
            if force or not processed.exists():
                with np.load(raw_path) as raw:
                    curve = preprocess(dict(raw), cfg["preprocessing"])
                np.savez_compressed(processed, **curve)
            with np.load(processed) as archive:
                curve = dict(archive)
            row.update(
                processed_path=str(processed.relative_to(root)),
                bls_path=str(bls_path.relative_to(root)),
                power_path=str(power_path.relative_to(root)),
            )
            if stage != "preprocess":
                if force or not (bls_path.exists() and power_path.exists()):
                    result, power = search_bls(curve, cfg["bls"])
                    write_json(bls_path, result)
                    np.savez_compressed(power_path, **power)
                result = json.loads(bls_path.read_text())
                result = {k: np.nan if v is None else v for k, v in result.items()}
                if stage == "features":
                    feature_rows.append(extract_features(curve, result, row))
            records.append(row)
            LOG.info("%s complete TIC %s sector %s", stage, row["tic_id"], row["sector"])
        except Exception as exc:
            LOG.exception("%s failed TIC %s sector %s", stage, row["tic_id"], row["sector"])
            failures.append(
                dict(tic_id=row["tic_id"], sector=row["sector"], stage=stage, error=str(exc))
            )
    pd.DataFrame(failures, columns=["tic_id", "sector", "stage", "error"]).to_csv(
        root / f"outputs/logs/{stage}_failures.csv", index=False
    )
    pd.DataFrame(records).to_csv(root / "data/processed/manifest.csv", index=False)
    if not records:
        raise RuntimeError(f"All light curves failed during {stage}")
    if stage == "features":
        pd.DataFrame(feature_rows).to_csv(root / "data/features/features.csv", index=False)


def train_frame(
    frame: pd.DataFrame, cfg: dict, family: str = "all"
) -> tuple[pd.DataFrame, dict, np.ndarray]:
    transform, matrix = fit_transform(frame, cfg["models"], family)
    result, fitted, scores = frame.copy(), {"transform": transform}, {}
    if cfg["models"]["isolation_forest"]["enabled"]:
        fitted["isolation_forest"], scores["isolation_forest_score"] = isolation_forest.fit(
            matrix, cfg["models"]["isolation_forest"], cfg["random_seed"]
        )
    if cfg["models"]["lof"]["enabled"]:
        fitted["lof"], scores["lof_score"] = lof.fit(matrix, cfg["models"]["lof"])
    if cfg["models"]["autoencoder"]["enabled"]:
        from sklearn.model_selection import GroupShuffleSplit

        from .anomaly.autoencoder import fit

        split = next(
            GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=cfg["random_seed"]).split(
                frame, groups=frame.tic_id
            )
        )
        ae_transform, _ = fit_transform(frame.iloc[split[0]], cfg["models"], family)
        fitted["autoencoder_transform"] = ae_transform

        fitted["autoencoder"], scores["autoencoder_score"] = fit(
            ae_transform.transform(frame),
            frame.tic_id.to_numpy(),
            cfg["models"]["autoencoder"],
            cfg["random_seed"],
            split=split,
        )
    if not scores:
        raise ValueError("Enable at least one anomaly model")
    for name, values in scores.items():
        result[name] = values
    result["ensemble_score"] = ensemble(pd.DataFrame(scores, index=frame.index))
    result["hybrid_score"] = (
        rank_normalize(result.depth_snr) + rank_normalize(result.ensemble_score)
    ) / 2
    return result, fitted, matrix


def train(root: Path, cfg: dict) -> None:
    features = pd.read_csv(root / "data/features/features.csv")
    if len(features) < 3:
        raise ValueError(
            "At least three successful light curves are required to train the main models"
        )
    scores, models, matrix = train_frame(features, cfg)
    for column in score_columns(scores):
        scores[f"rank_{column}"] = scores[column].rank(method="min", ascending=False)
    scores = scores.sort_values(
        ["ensemble_score", "tic_id", "sector"], ascending=[False, True, True]
    )
    scores.to_csv(root / "outputs/rankings/ranked_light_curves.csv", index=False)
    targets = target_scores(scores)
    for column in score_columns(targets):
        targets[f"rank_{column}"] = targets[column].rank(method="min", ascending=False)
    targets.sort_values(["ensemble_score", "tic_id"], ascending=[False, True]).to_csv(
        root / "outputs/rankings/ranked_targets.csv", index=False
    )
    joblib.dump(models, root / "outputs/models/models.joblib")
    joblib.dump(models["transform"], root / "outputs/models/preprocessing.joblib")
    np.save(root / "outputs/models/feature_matrix.npy", models["transform"].transform(scores))
    scores[["tic_id", "sector"]].to_csv(
        root / "outputs/models/feature_matrix_rows.csv", index=False
    )
    models["transform"].missingness.to_csv(root / "outputs/tables/missing_data.csv", index=False)
    scores.reindex(columns=FAMILIES["all"]).describe().to_csv(
        root / "outputs/tables/summary_statistics.csv"
    )


def evaluate(root: Path, cfg: dict) -> None:
    # Preserve score ties across CSV serialization, including percentile hybrids.
    frame = pd.read_csv(
        root / "outputs/rankings/ranked_light_curves.csv", float_precision="round_trip"
    )
    targets = target_scores(frame)
    ranking_metrics(targets, cfg["evaluation"]).to_csv(
        root / "outputs/tables/model_performance.csv", index=False
    )
    group_statistics(targets).to_csv(root / "outputs/tables/group_statistics.csv", index=False)
    correlations(targets, score_columns(targets), score_columns(targets)).to_csv(
        root / "outputs/tables/correlations.csv", index=False
    )
    correlations(frame, FAMILIES["all"], score_columns(frame)).to_csv(
        root / "outputs/tables/feature_score_correlations.csv", index=False
    )
    frame.sort_values("hybrid_score", ascending=False).drop_duplicates("tic_id").head(
        cfg["evaluation"]["candidate_reports"]
    ).to_csv(root / "outputs/tables/top_candidates.csv", index=False)
    catalog = (
        pd.read_csv(root / "data/catalog/normalized_catalog.csv")
        if (root / "data/catalog/normalized_catalog.csv").exists()
        else pd.DataFrame()
    )
    checks = []
    for row in frame.to_dict("records"):
        reference = (
            catalog[catalog.tic_id == row["tic_id"]] if "tic_id" in catalog else pd.DataFrame()
        )
        for planet in reference.to_dict("records"):
            if planet.get("disposition") in {"CP", "KP", "PC"}:
                checks.append(
                    dict(
                        tic_id=row["tic_id"],
                        sector=row["sector"],
                        toi_id=planet.get("toi_id"),
                        recovered_period=row["best_period"],
                        catalog_period=planet.get("catalog_period"),
                        **period_match(row["best_period"], planet.get("catalog_period", np.nan)),
                    )
                )
    pd.DataFrame(
        checks,
        columns=[
            "tic_id",
            "sector",
            "toi_id",
            "recovered_period",
            "catalog_period",
            "relative_period_error",
            "harmonic_relative_error",
            "harmonic_factor",
        ],
    ).to_csv(root / "outputs/tables/period_sanity.csv", index=False)
    ablation = []
    if cfg["evaluation"]["ablation"]:
        # Preserve the primary fit's row order: seeded IF samples row positions.
        features = pd.read_csv(root / "data/features/features.csv")
        keys = ["tic_id", "sector"]
        pd.testing.assert_frame_equal(
            features[keys].sort_values(keys).reset_index(drop=True),
            frame[keys].sort_values(keys).reset_index(drop=True),
        )
        for family in FAMILIES:
            try:
                ranked, _, _ = train_frame(features, cfg, family)
                metrics = ranking_metrics(target_scores(ranked), cfg["evaluation"])
                metrics["feature_family"] = family
                ablation.append(metrics)
            except ValueError as exc:
                LOG.warning("Ablation %s unavailable: %s", family, exc)
                ablation.append(
                    pd.DataFrame(
                        [dict(feature_family=family, metric_note=f"Not calculated because {exc}")]
                    )
                )
    pd.concat(ablation, ignore_index=True).to_csv(
        root / "outputs/tables/ablation_results.csv", index=False
    ) if ablation else pd.DataFrame(columns=["feature_family", "metric_note"]).to_csv(
        root / "outputs/tables/ablation_results.csv", index=False
    )


def figures(root: Path, cfg: dict) -> None:
    from .plots import diagnostic, example_figures, make_figures

    frame = pd.read_csv(root / "outputs/rankings/ranked_light_curves.csv")
    transform = joblib.load(root / "outputs/models/preprocessing.joblib")
    make_figures(
        frame,
        transform.transform(frame),
        transform.columns,
        pd.read_csv(root / "outputs/tables/model_performance.csv"),
        root,
    )
    top = pd.read_csv(root / "outputs/tables/top_candidates.csv")
    examples = frame[frame.label == "planet"]
    example = (
        (examples if len(examples) else frame)
        .sort_values("depth_snr", ascending=False)
        .iloc[0]
        .to_dict()
    )
    with np.load(root / example["processed_path"]) as c, np.load(root / example["power_path"]) as p:
        example_figures(dict(c), dict(p), example, root / "outputs/figures")
    for row in top.to_dict("records"):
        with np.load(root / row["processed_path"]) as c, np.load(root / row["power_path"]) as p:
            diagnostic(
                dict(c),
                dict(p),
                row,
                root / f"outputs/figures/candidates/tic{int(row['tic_id'])}_s{int(row['sector'])}",
            )


def report(root: Path) -> list[str]:
    frame = pd.read_csv(root / "outputs/rankings/ranked_light_curves.csv")
    targets = target_scores(frame)
    sample = pd.read_csv(root / "data/catalog/sample.csv")
    metrics = pd.read_csv(root / "outputs/tables/model_performance.csv")
    failed = set(sample.tic_id) - set(targets.tic_id)
    statements = [
        f"Requested {sample.tic_id.nunique()} targets; analysed {len(frame)} light curves from {len(targets)} unique targets.",
        f"{len(failed)} requested targets produced no usable feature row.",
    ]
    cfg = yaml.safe_load((root / "outputs/config_used.yaml").read_text())
    minimum, maximum = cfg["bls"]["min_period_days"], cfg["bls"]["max_period_days"]
    hosts = frame[frame.label.eq("planet")].drop_duplicates("tic_id")
    known = hosts.catalog_period.notna() & hosts.catalog_period.gt(0)
    outside = known & ~hosts.catalog_period.between(minimum, maximum)
    statements.append(
        f"{int(outside.sum())} of {len(hosts)} hosts' representative catalogue periods lie "
        f"outside the configured {minimum:g}–{maximum:g} day search interval; "
        f"{int((~known).sum())} have no usable representative period. Individual-sector "
        "baseline caps can restrict coverage further. This is not an all-planets completeness estimate."
    )
    exposure = frame.groupby(["label", "tic_id"]).sector.nunique().rename("sectors").reset_index()
    exposure = exposure.groupby(["label", "sectors"]).size().rename("targets").reset_index()
    exposure.to_csv(root / "outputs/tables/sector_coverage.csv", index=False)
    candidates = pd.read_csv(root / "outputs/tables/top_candidates.csv")
    statements.append(
        f"{int(candidates.label.eq('background').sum())} of the top {len(candidates)} "
        "hybrid-ranked inspection candidates are unlabelled backgrounds. "
        "These rankings do not validate planets."
    )
    for label in ("planet", "false_positive", "background"):
        statements.append(
            f"The analysed sample contains {int(targets.label.eq(label).sum())} {label} targets."
        )
    k = max(1, int(np.ceil(len(targets) * 0.1)))
    for method in ("depth_snr", "ensemble_score", "hybrid_score"):
        match = metrics[(metrics.method == method) & (metrics.k == k)]
        if len(match) and np.isfinite(match.iloc[0].recall_at_k):
            row = match.iloc[0]
            statements.append(
                f"{method} recovered {int(row.recovered)}/{int(row.positive_total)} catalogue-positive targets ({100 * row.recall_at_k:.1f}%) in the top {k} targets."
            )
        else:
            statements.append(f"{method}: Not calculated because top-10% recovery is unavailable.")
    text = [
        "# Research summary",
        "",
        "These are descriptive results on a selected reference sample. Anomalies are not planet discoveries; PC labels are not confirmations.",
        "",
        *[f"- {s}" for s in statements],
        "",
        "## Ranking metrics",
        "```",
        metrics.to_string(index=False),
        "```",
    ]
    for name in (
        "correlations",
        "group_statistics",
        "ablation_results",
        "sector_coverage",
        "top_candidates",
    ):
        table = pd.read_csv(root / f"outputs/tables/{name}.csv")
        if name == "top_candidates":
            table = table[
                [
                    c
                    for c in [
                        "tic_id",
                        "sector",
                        "label",
                        "disposition",
                        "best_period",
                        "best_depth",
                        "depth_snr",
                        "ensemble_score",
                        "hybrid_score",
                    ]
                    if c in table
                ]
            ]
        text.extend(
            ["", f"## {name.replace('_', ' ').title()}", "```", table.to_string(index=False), "```"]
        )
    text.extend(
        [
            "",
            "## Interpretation limits",
            "Sector coverage differs between reference groups. Taking each target's maximum score across sectors gives more observed sectors more opportunities for a high score; group comparisons are not controlled for this exposure difference. Catalogue periods outside the search interval cannot be recovered directly within that interval, although harmonics may occur. Independent evaluation with exposure and search coverage accounted for is needed before claiming generalisation or reduced inspection workload.",
            "The primary experiment uses unsupervised anomaly detection; catalogue labels are used only for evaluation. The LOF novelty helper does not constitute an evaluated semi-supervised experiment. Physics-informed means astrophysically motivated feature engineering, not physical equations enforced during training. Stellar-catalogue-dependent radius and duration-consistency proxies are extracted where possible but excluded from default ML inputs because measurement availability differs between groups.",
            "Interpretability analyses describe properties associated with high anomaly scores. They do not establish causation, provide formal per-object model attribution, or calibrate anomaly scores as statistical significance. The primary models fit and rank the same unlabelled sample. Reduced manual inspection workload and generalisation remain research questions requiring independent evaluation.",
            "No held-out generalisation or causal improvement is established. Background objects are unlabelled. Precision@K measures catalogue-positive yield, not true planet purity. ROC-AUC and average precision exclude PC-only and background targets. BLS power and depth SNR are identical rankings under the default SNR objective. Catalogue-conditioned stellar-feature missingness can bias physics ablations. Non-parametric p-values are exploratory and uncorrected for multiple comparisons.",
        ]
    )
    (root / "outputs/research_summary.md").write_text("\n".join(text), encoding="utf-8")
    (root / "outputs/abstract_results.txt").write_text(
        "Descriptive unsupervised results from the fitted sample; anomaly scores are not calibrated statistical significance. Generalisation and reduced manual inspection workload have not been independently demonstrated.\n"
        + "\n".join(statements),
        encoding="utf-8",
    )
    return statements


def injection(root: Path, cfg: dict) -> None:
    rows = []
    for depth in [0.001, 0.003, 0.01]:
        raw, truth = synthetic_curve(depth=depth)
        curve = preprocess(raw, cfg["preprocessing"])
        result, _ = search_bls(curve, cfg["bls"])
        features = extract_features(curve, result, {})
        rows.append(
            dict(
                injected_depth=depth,
                recovered_depth=features["best_depth"],
                **period_match(result["best_period"], truth["period"]),
            )
        )
        write_json(root / f"outputs/tables/injection_truth_{depth}.json", truth)
    pd.DataFrame(rows).to_csv(root / "outputs/tables/injection_recovery.csv", index=False)


def run(cfg: dict, stage: str = "all", resume: bool = False, force: bool = False) -> Path:
    root = prepare(cfg)
    configure(root)
    random.seed(cfg["random_seed"])
    np.random.seed(cfg["random_seed"])
    (root / "outputs/config_used.yaml").write_text(yaml.safe_dump(cfg), encoding="utf-8")
    provenance(root, cfg, [], "running")
    try:
        for name in STAGES if stage == "all" else [stage]:
            from . import cache

            if resume and not force and cache.valid(root, cfg, name, code_hash()):
                LOG.info("Reusing verified stage %s", name)
                continue
            LOG.info("Starting stage %s", name)
            if name == "download":
                sample = select_sample(root, cfg, force)
                download_sample(root, sample, cfg["data"], force)
            elif name in {"preprocess", "bls", "features"}:
                curve_stages(root, cfg, name, force)
            elif name == "train":
                train(root, cfg)
            elif name == "evaluate":
                evaluate(root, cfg)
            elif name == "figures":
                figures(root, cfg)
            elif name in {"report", "abstract"}:
                statements = report(root)
                if name == "abstract":
                    print("\n".join(statements))
            elif name == "injection":
                injection(root, cfg)
            cache.record(root, cfg, name, code_hash())
        sample_path = root / "data/catalog/sample.csv"
        ids = pd.read_csv(sample_path).tic_id.tolist() if sample_path.exists() else []
        provenance(root, cfg, ids, f"completed:{stage}")
        LOG.info("Completed %s successfully. Outputs: %s", stage, root / "outputs")
    except Exception:
        provenance(root, cfg, [], f"failed:{stage}")
        LOG.exception("Experiment failed; existing valid artifacts are preserved")
        raise
    return root


def main(default_stage: str = "all") -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="config/small_test.yaml")
    parser.add_argument(
        "--stage", choices=STAGES + ["all", "injection", "abstract"], default=default_stage
    )
    parser.add_argument(
        "--resume", action="store_true", help="Reuse valid scientific caches (also the default)"
    )
    parser.add_argument(
        "--force", action="store_true", help="Refresh catalogue and recompute scientific caches"
    )
    args = parser.parse_args()
    run(load_config(args.config), args.stage, args.resume, args.force)


if __name__ == "__main__":
    main()
