"""Prospective extension, kept outside the checksum-frozen v2 scientific package."""

import argparse
import hashlib
import importlib.metadata
import json
import logging
import os
import shutil
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import yaml
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.semi_supervised import LabelSpreading

from tess_anomaly.coherence import COMPACT
from tess_anomaly.dataset import fit_transform
from tess_anomaly.research import enriched_features, one_sector, percentile, source_digest

ROOT = Path(__file__).resolve().parents[1]
METHODS = ["bls", "anomaly", "unsupervised_hybrid", "semi_affinity", "semi_anomaly", "semi_hybrid"]
PACKAGES = ["numpy", "pandas", "scipy", "astropy", "scikit-learn", "joblib"]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False), encoding="utf-8")


def seal(folder):
    write_json(
        folder / "manifest.json",
        {
            p.relative_to(folder).as_posix(): sha(p)
            for p in sorted(folder.rglob("*"))
            if p.is_file() and p.name != "manifest.json"
        },
    )


def verify(folder):
    for relative, expected in json.loads((folder / "manifest.json").read_text()).items():
        path = (folder / relative).resolve()
        if not path.is_relative_to(folder.resolve()) or sha(path) != expected:
            raise ValueError(f"Changed or invalid artifact: {relative}")


def check_frame(frame):
    needed = {
        "tic_id",
        "sector",
        "label",
        "disposition",
        "n_observations",
        "baseline_days",
        "transit_epoch",
        "catalog_period",
        *COMPACT,
    }
    if needed - set(frame):
        raise ValueError(f"Missing feature columns: {sorted(needed - set(frame))}")
    if frame.empty or frame[["tic_id", "sector"]].isna().any().any():
        raise ValueError("Empty sample or missing identifiers")
    if frame.duplicated(["tic_id", "sector"]).any():
        raise ValueError("Duplicate target-sector rows")
    if frame.groupby("tic_id").label.nunique(dropna=False).max() > 1:
        raise ValueError("Conflicting target labels")
    if not np.isfinite(frame.depth_snr).all():
        raise ValueError("Nonfinite BLS score")


def validate_protocol(p):
    if not p["features"] or set(p["features"]) - set(COMPACT):
        raise ValueError("Only the predefined photometric feature contract is allowed")
    if not 0 < p["label_fraction"] < 1 or not 0 < p["target_recall"] <= 1:
        raise ValueError("Invalid label fraction or recall target")
    if p["primary_method"] not in METHODS or p["budget"] < 1 or p["bootstrap_repeats"] < 2:
        raise ValueError("Invalid primary method, budget or bootstrap count")
    if not 0 <= p["bls_fraction"] <= 1 or p["gamma"] <= 0:
        raise ValueError("Invalid ranking or graph parameters")
    if not 0 < p["graph_clip"] <= 5 or p["gamma"] > 0.1:
        raise ValueError("Graph bounds must keep the RBF kernel numerically supported")
    partitions = [
        set(p[k]) for k in ["training_sectors", "calibration_sectors", "evaluation_sectors"]
    ]
    if any(not x for x in partitions) or any(
        partitions[i] & partitions[j] for i in range(3) for j in range(i)
    ):
        raise ValueError("Sector partitions must be nonempty and disjoint")
    if partitions[2] & set(range(1, 27)):
        raise ValueError("Previously inspected sectors cannot be v3 evaluation sectors")


def reference_labels(frame):
    """Catalogue references: unknown/conflicting/background labels always remain -1."""
    labels = []
    for row in frame.itertuples():
        d = set(str(row.disposition).split(";"))
        pos, neg = bool(d & {"CP", "KP"}), bool(d & {"FP", "FA"})
        labels.append(
            1
            if pos and not neg and row.label == "planet"
            else 0
            if neg and not pos and row.label == "false_positive"
            else -1
        )
    return np.asarray(labels)


def disjoint(a, b):
    if set(a.tic_id) & set(b.tic_id):
        raise ValueError("Target leakage")
    if set(a.sector) & set(b.sector):
        raise ValueError("Sector leakage")


def split(frame, p):
    cal = frame[frame.sector.isin(p["calibration_sectors"])]
    train = frame[frame.sector.isin(p["training_sectors"])]
    train = train[~train.tic_id.isin(cal.tic_id)]
    disjoint(train, cal)
    if min(train.tic_id.nunique(), cal.tic_id.nunique()) < 10:
        raise ValueError("Need at least ten targets in each partition")
    return one_sector(train), one_sector(cal)


def fit(train, cal, p):
    validate_protocol(p)
    disjoint(train, cal)
    train, cal = one_sector(train), one_sector(cal)
    cfg = dict(
        scaler="robust",
        max_missing_fraction=0.6,
        correlation_threshold=0.95,
        use_stellar_catalog_features=False,
    )
    transform, x = fit_transform(train, cfg, columns=p["features"])
    forest = IsolationForest(n_estimators=p["trees"], random_state=p["seed"]).fit(x)
    lof = LocalOutlierFactor(n_neighbors=min(p["neighbors"], len(x) - 1), novelty=True).fit(x)
    reliable = reference_labels(train)
    rng = np.random.default_rng(p["seed"])
    y = np.full(len(train), -1)
    for label in [0, 1]:
        eligible = np.flatnonzero(reliable == label)
        if len(eligible) < 2:
            raise ValueError("Insufficient reliable training labels in both classes")
        selected = rng.choice(
            eligible, max(1, int(len(eligible) * p["label_fraction"])), replace=False
        )
        y[selected] = label
    # Graph construction uses both labelled and genuinely unlabelled training observations.
    semi = LabelSpreading(kernel="rbf", gamma=p["gamma"], alpha=0.2, max_iter=1000, tol=1e-4).fit(
        np.clip(x, -p["graph_clip"], p["graph_clip"]), y
    )
    if semi.n_iter_ >= semi.max_iter:
        raise ValueError("Label spreading failed to converge")
    bundle = dict(
        transform=transform,
        forest=forest,
        lof=lof,
        semi=semi,
        protocol=p,
        training=train[transform.columns].copy(),
        train_ids=train.tic_id.tolist(),
        cal_ids=cal.tic_id.tolist(),
        labelled=pd.DataFrame({"tic_id": train.tic_id.to_numpy(), "fit_label": y}),
    )
    bundle["calibration"] = raw_scores(bundle, cal)
    return bundle


def raw_scores(b, frame):
    x = b["transform"].transform(frame)
    values = dict(
        bls=frame.depth_snr.to_numpy(dtype=float),
        isolation=-b["forest"].score_samples(x),
        lof=-b["lof"].score_samples(x),
        semi=b["semi"].predict_proba(
            np.clip(x, -b["protocol"]["graph_clip"], b["protocol"]["graph_clip"])
        )[:, list(b["semi"].classes_).index(1)],
    )
    if not all(np.isfinite(v).all() for v in values.values()):
        raise ValueError("Nonfinite model output; unsupported graph prediction or input")
    return values


def score(b, frame):
    raw = raw_scores(b, frame)
    p = {k: percentile(b["calibration"][k], v) for k, v in raw.items()}
    result = frame.copy()
    result["bls"] = raw["bls"]
    result["anomaly"] = (p["isolation"] + p["lof"]) / 2
    result["unsupervised_hybrid"] = (result.anomaly + p["bls"]) / 2
    result["semi_affinity"] = raw["semi"]
    result["graph_clipped_features"] = (
        abs(b["transform"].transform(frame)) > b["protocol"]["graph_clip"]
    ).sum(axis=1)
    # Reference-class affinity modulates anomaly priority; not a planet probability.
    result["semi_anomaly"] = result.anomaly * (0.5 + 0.5 * p["semi"])
    result["semi_hybrid"] = (p["bls"] + result.semi_anomaly) / 2
    return result


def candidates(frame, p, ephemerides=None):
    out = frame.copy()
    cap = out.get("search_max_period", np.minimum(p["max_period"], out.baseline_days / 2))
    minimum = out.get("search_min_period", p["min_period"])
    out["search_eligible"] = out.catalog_period.between(minimum, cap)
    out["period_relative_error"] = abs(out.best_period / out.catalog_period - 1)
    out["representative_period_match"] = (out.catalog_period > 0) & (
        out.period_relative_error <= p["period_tolerance"]
    )
    out["epoch_testable"] = False
    out["signal_match"] = False
    out["matched_catalogue_id"] = ""
    out["best_epoch_residual_days"] = np.nan
    if ephemerides is not None:
        needed = {
            "tic_id",
            "catalogue_id",
            "period_days",
            "epoch_bjd_tdb",
            "period_error_days",
            "epoch_error_days",
            "reliable",
        }
        if needed - set(ephemerides):
            raise ValueError(f"Missing ephemeris fields: {needed - set(ephemerides)}")
        for idx, row in out.iterrows():
            offset = {"BTJD (BJD_TDB - 2457000)": 2457000.0, "BJD_TDB": 0.0}.get(
                row.get("time_system")
            )
            if offset is None:
                continue
            options = ephemerides[ephemerides.tic_id.eq(row.tic_id)]
            for e in options.itertuples():
                nums = [e.period_days, e.epoch_bjd_tdb, e.period_error_days, e.epoch_error_days]
                if str(e.reliable).lower() != "true" or not np.isfinite(nums).all():
                    continue
                if e.period_days <= 0 or min(e.period_error_days, e.epoch_error_days) < 0:
                    continue
                epoch = row.transit_epoch + offset
                cycles = round((epoch - e.epoch_bjd_tdb) / e.period_days)
                uncertainty = np.hypot(e.epoch_error_days, cycles * e.period_error_days)
                # Reject stale ephemerides rather than widening a match until it passes.
                if not 0 < row.best_duration < e.period_days or uncertainty > row.best_duration / 2:
                    continue
                out.loc[idx, "epoch_testable"] = True
                residual = abs(epoch - (e.epoch_bjd_tdb + cycles * e.period_days))
                period_ok = abs(row.best_period / e.period_days - 1) <= p["period_tolerance"]
                if period_ok and residual <= row.best_duration / 2:
                    out.loc[idx, "signal_match"] = True
                    out.loc[idx, "matched_catalogue_id"] = str(e.catalogue_id)
                    out.loc[idx, "best_epoch_residual_days"] = residual
                    break
    out["candidate_status"] = "unvalidated photometric candidate"
    out["diagnostic_flags"] = np.where(out.epoch_testable, "", "ephemeris_unverified;")
    out["diagnostic_flags"] += np.where(out.number_observed_transits < 2, "few_events;", "")
    out["diagnostic_flags"] += np.where(out.best_depth <= 0, "nonpositive_depth;", "")
    return out


def ranked(frame, method):
    return (
        frame.sort_values(
            [method, "tic_id", "sector"], ascending=[False, True, True], kind="stable"
        )
        .drop_duplicates("tic_id")
        .reset_index(drop=True)
    )


def reports(frame, p):
    curves, budgets, complements = [], [], []
    for exposure, data in [("all_sectors", frame), ("one_sector", one_sector(frame))]:
        total = data.loc[data.label.eq("planet"), "tic_id"].nunique()
        eligible = set(data.loc[data.label.eq("planet") & data.search_eligible, "tic_id"])
        base = ranked(data, "bls")
        positives = set(data.loc[data.label.eq("planet"), "tic_id"])
        for method in METHODS:
            r = ranked(data, method)
            pos = r.label.eq("planet").to_numpy()
            counts = np.cumsum(pos)
            signals = np.cumsum(pos & r.signal_match.to_numpy())
            eligibility = np.cumsum(pos & r.tic_id.isin(eligible).to_numpy())
            testable = np.cumsum(pos & r.epoch_testable.to_numpy())
            for k in range(1, len(r) + 1):
                curves.append(
                    dict(
                        exposure=exposure,
                        method=method,
                        k=k,
                        recovered=int(counts[k - 1]),
                        positive_total=total,
                        recall=float(counts[k - 1] / total) if total else None,
                        signal_matched=int(signals[k - 1]),
                        selected_ephemeris_testable=int(testable[k - 1]),
                        eligible_recovered=int(eligibility[k - 1]),
                        eligible_total=len(eligible),
                    )
                )
            required = int(np.ceil(total * p["target_recall"]))
            hit = np.flatnonzero(counts >= required) if required else []
            budgets.append(
                dict(
                    exposure=exposure,
                    method=method,
                    required_hosts=required,
                    target_recall=p["target_recall"],
                    budget=int(hit[0] + 1) if len(hit) else None,
                )
            )
            k = min(p["budget"], len(base))
            bls_ids = set(base.tic_id.head(k))
            selected = set(base.tic_id.head(int(k * p["bls_fraction"])))
            selected |= set(r.loc[~r.tic_id.isin(selected), "tic_id"].head(k - len(selected)))
            complements.append(
                dict(
                    exposure=exposure,
                    method=method,
                    k=k,
                    gained=len((selected - bls_ids) & positives),
                    lost=len((bls_ids - selected) & positives),
                    recovered=len(selected & positives),
                    bls_recovered=len(bls_ids & positives),
                )
            )
    budget_table = pd.DataFrame(budgets)
    baseline = budget_table.loc[budget_table.method.eq("bls"), ["exposure", "budget"]].rename(
        columns={"budget": "bls_budget"}
    )
    budget_table = budget_table.merge(baseline, on="exposure", validate="many_to_one")
    budget_table["budget_difference_vs_bls"] = budget_table.budget - budget_table.bls_budget
    return pd.DataFrame(curves), budget_table, pd.DataFrame(complements)


def bootstrap(frame, p):
    rows = []
    for exposure, data in [("all_sectors", frame), ("one_sector", one_sector(frame))]:
        targets = data.groupby("tic_id", sort=True)[METHODS].max()
        pos = data.groupby("tic_id", sort=True).label.first().eq("planet").to_numpy()
        ids = targets.index.to_numpy()
        rng = np.random.default_rng(p["seed"])
        k = min(p["budget"], len(targets))

        def counts(draw):
            return {
                method: int(
                    pos[draw[np.lexsort((ids[draw], -targets[method].to_numpy()[draw]))[:k]]].sum()
                )
                for method in METHODS
            }

        original = counts(np.arange(len(targets)))
        draws = pd.DataFrame(
            [
                counts(rng.integers(len(targets), size=len(targets)))
                for _ in range(p["bootstrap_repeats"])
            ]
        )
        for method in METHODS[1:]:
            low, high = np.quantile(draws[method] - draws.bls, [0.025, 0.975])
            rows.append(
                dict(
                    exposure=exposure,
                    method=method,
                    k=k,
                    difference=original[method] - original["bls"],
                    low=float(low),
                    high=float(high),
                    scope="Paired targets with reranking; conditional on frozen fitted models",
                )
            )
    return pd.DataFrame(rows)


def explain(b, frame):
    """Controlled replacement contrasts, not causal effects or additive SHAP attributions."""
    rows = []
    chosen = ranked(frame, b["protocol"]["primary_method"]).head(b["protocol"]["explain_n"])
    for idx in chosen.index:
        row = chosen.loc[[idx]]
        original = score(b, row)
        for feature in b["transform"].columns:
            values = b["training"][feature].replace([np.inf, -np.inf], np.nan).dropna()
            value = float(row[feature].iloc[0])
            variants = pd.concat([row] * 3, ignore_index=True)
            variants[feature] = values.quantile([0.4, 0.5, 0.6]).to_numpy()
            changed = score(b, variants)
            for method in METHODS[1:]:
                delta = original[method].iloc[0] - changed[method].to_numpy()
                rows.append(
                    dict(
                        tic_id=int(row.tic_id.iloc[0]),
                        sector=int(row.sector.iloc[0]),
                        feature=feature,
                        value=value,
                        training_percentile=float((values <= value).mean())
                        if np.isfinite(value)
                        else np.nan,
                        method=method,
                        median_replacement_delta=float(delta[1]),
                        delta_min=float(delta.min()),
                        delta_max=float(delta.max()),
                        stable_sign=bool(np.all(delta >= 0) or np.all(delta <= 0)),
                    )
                )
    return pd.DataFrame(rows)


def freeze(frame, p, output, excluded):
    check_frame(frame)
    validate_protocol(p)
    if output.exists():
        raise ValueError("Refusing to overwrite freeze")
    train, cal = split(frame, p)
    b = fit(train, cal, p)
    b["excluded_ids"] = sorted(set(map(int, excluded)) | set(frame.tic_id.astype(int)))
    output.mkdir(parents=True)
    joblib.dump(b, output / "model.joblib")
    frame.to_csv(output / "development_features.csv", index=False)
    train.to_csv(output / "training.csv", index=False)
    cal.to_csv(output / "calibration.csv", index=False)
    b["labelled"].to_csv(output / "limited_labels.csv", index=False)
    b["transform"].missingness.to_csv(output / "feature_selection.csv", index=False)
    pd.DataFrame({"tic_id": b["excluded_ids"]}).to_csv(output / "excluded_tics.csv", index=False)
    write_json(output / "protocol.json", p)
    write_json(
        output / "provenance.json",
        dict(
            script_sha256=sha(__file__),
            source_digest=source_digest(),
            versions={n: importlib.metadata.version(n) for n in PACKAGES},
            status="Frozen after development inspection; new evaluation not yet performed",
        ),
    )
    shutil.copy2(__file__, output / "research_v3.py")
    seal(output)
    return b


def load_frozen(folder):
    verify(folder)
    provenance = json.loads((folder / "provenance.json").read_text())
    if (
        provenance["script_sha256"] != sha(__file__)
        or provenance["source_digest"] != source_digest()
    ):
        raise ValueError("Scientific implementation differs from frozen version")
    if provenance["versions"] != {n: importlib.metadata.version(n) for n in PACKAGES}:
        raise ValueError("Restore the frozen package versions")
    return joblib.load(folder / "model.joblib")  # Only load trusted local artifacts.


def export_features(workspace, output):
    frame = enriched_features(workspace)
    check_frame(frame)
    output.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output, index=False)
    cfg = yaml.safe_load((workspace / "outputs/config_used.yaml").read_text())
    sample = pd.read_csv(workspace / "data/catalog/sample.csv")
    audit = sample[["tic_id", "label"]].drop_duplicates("tic_id")
    audit["analysed"] = audit.tic_id.isin(frame.tic_id)
    audit.to_csv(output.with_suffix(".attrition.csv"), index=False)
    write_json(
        output.with_suffix(".provenance.json"),
        dict(
            feature_sha256=sha(output),
            preprocessing=cfg["preprocessing"],
            bls=cfg["bls"],
            data=cfg["data"],
            selected_targets=sorted(sample.tic_id.astype(int).unique().tolist()),
            source_digest=source_digest(),
            input_hashes={
                name: sha(workspace / name)
                for name in [
                    "data/features/features.csv",
                    "data/catalog/sample.csv",
                    "outputs/config_used.yaml",
                ]
            },
        ),
    )


def check_evaluation_provenance(path, b):
    meta = json.loads(path.with_suffix(".provenance.json").read_text())
    if meta["feature_sha256"] != sha(path) or meta["source_digest"] != source_digest():
        raise ValueError("Evaluation feature provenance mismatch")
    for key in ["preprocessing", "bls"]:
        if meta[key] != b["protocol"][key]:
            raise ValueError(f"Evaluation {key} differs from frozen protocol")
    if set(meta["selected_targets"]) & set(b["excluded_ids"]):
        raise ValueError("Evaluation selection includes inspected targets")
    if set(meta["data"]["sectors"]) != set(b["protocol"]["evaluation_sectors"]):
        raise ValueError("Acquisition sectors differ from frozen protocol")
    for key, value in b["protocol"]["evaluation_data"].items():
        if meta["data"][key] != value:
            raise ValueError(f"Acquisition setting differs: {key}")
    return meta


def evaluate(b, frame, output, ephemerides=None):
    check_frame(frame)
    if output.exists():
        raise ValueError("Refusing to overwrite evaluation")
    if set(frame.tic_id) & set(b["excluded_ids"]):
        raise ValueError("Previously inspected targets in evaluation")
    if not set(frame.sector) <= set(b["protocol"]["evaluation_sectors"]):
        raise ValueError("Evaluation contains non-predefined sectors")
    result = candidates(score(b, frame), b["protocol"], ephemerides)
    output.mkdir(parents=True)
    result.to_csv(output / "candidates.csv", index=False)
    if ephemerides is not None:
        ephemerides.to_csv(output / "ephemerides_used.csv", index=False)
    curves, budgets, complements = reports(result, b["protocol"])
    curves.to_csv(output / "recovery_curves.csv", index=False)
    budgets.to_csv(output / "inspection_budgets.csv", index=False)
    complements.to_csv(output / "complementarity.csv", index=False)
    bootstrap(result, b["protocol"]).to_csv(output / "paired_uncertainty.csv", index=False)
    explain(b, result).to_csv(output / "score_explanations.csv", index=False)
    write_json(output / "protocol.json", b["protocol"])
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    for exposure, group in curves.groupby("exposure"):
        fig, ax = plt.subplots(figsize=(7, 5))
        for method, part in group.groupby("method"):
            ax.plot(part.k, part.recall, label=method)
        ax.set(xlabel="Targets inspected", ylabel="Catalogue-host recall", title=exposure)
        ax.legend(fontsize=8)
        fig.tight_layout()
        fig.savefig(output / f"recovery_{exposure}.png", dpi=160)
        plt.close(fig)
    pd.DataFrame(
        columns=["case_id", "reviewer", "method", "start_utc", "end_utc", "decision", "blinded"]
    ).to_csv(output / "manual_review_template.csv", index=False)
    (output / "report.md").write_text(
        "# V3 evaluation\n\nAll methods and exposure controls retained in accompanying tables. "
        "Host recovery is not planet validation. Ephemeris matches require verified time systems and "
        "sufficiently precise catalogue ephemerides. Scores are not calibrated significance or "
        "planet probabilities; replacement contrasts are not causal attribution. "
        "Rank-budget savings are distinct from actual review time, which has not been measured.\n",
        encoding="utf-8",
    )
    seal(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command",
        choices=[
            "prepare",
            "export-features",
            "freeze",
            "prepare-evaluation",
            "evaluate",
            "sensitivity",
            "release",
            "review-times",
        ],
    )
    parser.add_argument("--protocol", type=Path, default=ROOT / "config/research_v3.yaml")
    parser.add_argument("--input", type=Path)
    parser.add_argument("--ephemerides", type=Path)
    parser.add_argument("--frozen", type=Path, default=ROOT / "experiments/research_v3/frozen")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    if args.output.exists():
        raise ValueError("Output already exists; select a new destination")
    p = yaml.safe_load(args.protocol.read_text(encoding="utf-8"))
    validate_protocol(p)
    if args.command == "prepare":
        frames = [
            enriched_features(ROOT / w).assign(source_workspace=w)
            for w in p["development_workspaces"]
        ]
        frame = pd.concat(frames, ignore_index=True)
        check_frame(frame)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        frame.to_csv(args.output, index=False)
    elif args.command == "export-features":
        export_features(args.input, args.output)
    elif args.command == "freeze":
        excluded = set()
        for path in p["inspected_samples"]:
            excluded.update(pd.read_csv(ROOT / path).tic_id.astype(int))
        freeze(pd.read_csv(args.input), p, args.output, excluded)
    elif args.command == "prepare-evaluation":
        b = load_frozen(args.frozen)
        cfg = yaml.safe_load((ROOT / "config/default.yaml").read_text())
        cfg["workspace"] = "experiments/independent_v3"
        cfg["random_seed"] = b["protocol"]["seed"]
        cfg["data"].update(b["protocol"]["evaluation_data"])
        cfg["data"]["sectors"] = b["protocol"]["evaluation_sectors"]
        if not args.frozen.resolve().is_relative_to(ROOT.resolve()):
            raise ValueError("Portable acquisition requires a freeze inside the repository")
        if args.output.resolve().parent != (ROOT / "config").resolve():
            raise ValueError("Write acquisition configuration into the repository config directory")
        cfg["data"]["exclude_tics_csv"] = Path(
            os.path.relpath(args.frozen.resolve() / "excluded_tics.csv", ROOT / cfg["workspace"])
        ).as_posix()
        # Freeze preprocessing/search choices independently of future edits to default.yaml.
        cfg["preprocessing"] = b["protocol"]["preprocessing"]
        cfg["bls"] = b["protocol"]["bls"]
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(yaml.safe_dump(cfg), encoding="utf-8")
    elif args.command == "evaluate":
        b = load_frozen(args.frozen)
        provenance = check_evaluation_provenance(args.input, b)
        evaluate(
            b,
            pd.read_csv(args.input),
            args.output,
            pd.read_csv(args.ephemerides) if args.ephemerides else None,
        )
        write_json(args.output / "input_provenance.json", provenance)
        shutil.copy2(args.input.with_suffix(".attrition.csv"), args.output / "sample_attrition.csv")
        seal(args.output)
    elif args.command == "sensitivity":
        frame = pd.read_csv(args.input)
        check_frame(frame)
        train, cal = split(frame, p)
        rows = []
        for seed in p["sensitivity_seeds"]:
            for fraction in p["sensitivity_label_fractions"]:
                for proportion in p["sensitivity_training_fractions"]:
                    current = dict(p, seed=seed, label_fraction=fraction)
                    try:
                        subset = train.sample(frac=proportion, random_state=seed)
                        b = fit(subset, cal, current)
                        table, _, _ = reports(candidates(score(b, cal), current), current)
                        table = table[table.k.eq(min(p["budget"], len(cal)))]
                        rows.extend(
                            dict(
                                **r,
                                seed=seed,
                                label_fraction=fraction,
                                training_fraction=proportion,
                                status="ok",
                            )
                            for r in table.to_dict("records")
                        )
                    except ValueError as e:
                        rows.append(
                            dict(
                                seed=seed,
                                label_fraction=fraction,
                                training_fraction=proportion,
                                status="failed",
                                error=str(e),
                            )
                        )
        args.output.mkdir(parents=True)
        pd.DataFrame(rows).to_csv(args.output / "development_sensitivity.csv", index=False)
        write_json(args.output / "protocol.json", p)
        seal(args.output)
    elif args.command == "review-times":
        frame = pd.read_csv(args.input)
        frame["seconds"] = (
            pd.to_datetime(frame.end_utc, utc=True) - pd.to_datetime(frame.start_utc, utc=True)
        ).dt.total_seconds()
        if frame.empty or frame.seconds.isna().any() or (frame.seconds <= 0).any():
            raise ValueError("Completed, positive-duration review records required")
        if not frame.blinded.astype(str).str.lower().eq("true").all():
            raise ValueError("Unblinded records cannot support the planned blinded comparison")
        if frame.duplicated(["case_id", "reviewer", "method"]).any():
            raise ValueError("Duplicate review records")
        args.output.mkdir(parents=True)
        frame.to_csv(args.output / "review_records.csv", index=False)
        frame.groupby("method").seconds.agg(["count", "sum", "median"]).to_csv(
            args.output / "descriptive_review_times.csv"
        )
        seal(args.output)
    else:
        load_frozen(args.frozen)
        args.output.mkdir(parents=True)
        for folder in ["src", "scripts", "config", "tests"]:
            shutil.copytree(
                ROOT / folder, args.output / folder, ignore=shutil.ignore_patterns("__pycache__")
            )
        for name in ["LICENSE", "pyproject.toml", "requirements.txt", "requirements-lock.txt",
                     "README.md", "RESEARCH_GUIDE.md", "output_audit.json", "CITATION.md"]:
            shutil.copy2(ROOT / name, args.output / name)
        shutil.copytree(args.frozen, args.output / "experiments/research_v3/frozen")
        for relative in json.loads((args.frozen / "protocol.json").read_text())[
            "inspected_samples"
        ]:
            target = args.output / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, target)
        shutil.copytree(ROOT / "paper/final", args.output / "paper/v2")
        shutil.copytree(ROOT / "paper/v3", args.output / "paper/v3")
        if args.input:
            verify(args.input)
            shutil.copytree(args.input, args.output / "evaluation_v3")
        (args.output / "RELEASE_STATUS.md").write_text(
            "# Local release candidate\n\nNot published; no URL or DOI assigned. "
            "Numerical feature-level v3 reproduction uses frozen training/calibration tables. "
            "Full photometry and v2 numerical archives are not bundled. Restore public MAST "
            "products recorded in development_features.csv for upstream reproduction. "
            "Author details and repository/deposition metadata remain to be supplied.\n"
        )
        seal(args.output)


if __name__ == "__main__":
    main()
