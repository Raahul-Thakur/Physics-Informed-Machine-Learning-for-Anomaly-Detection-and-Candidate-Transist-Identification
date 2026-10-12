"""Archive inspected results and reproduce paper analyses without changing frozen models."""

import argparse
import json
import logging
import shutil
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tess_anomaly.evaluation import target_scores
from tess_anomaly.plots import diagnostic, save
from tess_anomaly.research import digest, load_frozen, one_sector

ROOT = Path(__file__).resolve().parents[1]
LOG = logging.getLogger(__name__)
PLAN = dict(
    primary_family="compact",
    budget=100,
    bootstrap_seed=20260916,
    bootstrap_repeats=5000,
    bootstrap="Paired nonparametric target bootstrap, reranking both fixed-model scores in each resample",
    review_per_group=2,
    review_groups=["both", "bls_only", "hybrid_only", "false_positive", "background"],
    review_selection="Top two by BLS rank for BLS-only; otherwise hybrid rank, with TIC ties. "
    "Positives are selected by membership in primary all-sector top-100 lists. "
    "False positives and backgrounds are the two highest hybrid-ranked members of their groups.",
    status="Reporting plan fixed after inspection of aggregate independent results, before object review. "
    "These additions are post-evaluation analyses, not newly preregistered hypotheses.",
)


def sha_tree(path):
    return {str(p.relative_to(path)): digest(p) for p in sorted(path.rglob("*")) if p.is_file()}


def archive(destination: Path):
    if destination.exists():
        raise ValueError("Archive exists; use --reproduce to verify and reuse it")
    load_frozen(ROOT / "experiments/research_v2/frozen")
    destination.mkdir(parents=True)
    trees = {
        "independent": ROOT / "experiments/independent_v2/frozen_evaluation",
        "frozen": ROOT / "experiments/research_v2/frozen",
        "development_exposure": ROOT / "experiments/research_v2/development_exposure",
        "injections": ROOT / "experiments/research_v2/injections",
        "development_baseline": ROOT / "experiments/default/outputs/tables",
        "configs": ROOT / "config",
        "manuscript_before": ROOT / "docs",
    }
    for name, source in trees.items():
        shutil.copytree(source, destination / name)
    for name, root in [
        ("development", ROOT / "experiments/default"),
        ("evaluation", ROOT / "experiments/independent_v2"),
    ]:
        for relative in [
            "data/catalog/sample.csv",
            "data/raw/manifest.csv",
            "data/processed/manifest.csv",
            "outputs/logs/download_failures.csv",
            "outputs/logs/features_failures.csv",
            "outputs/config_used.yaml",
            "outputs/run_metadata.json",
        ]:
            target = destination / name / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(root / relative, target)
    for name in ["requirements.txt", "requirements-lock.txt", "pyproject.toml"]:
        shutil.copy2(ROOT / name, destination / name)
    # Archive scripts/tests as well as the already-frozen scientific source.
    for name in ["scripts", "tests"]:
        shutil.copytree(
            ROOT / name, destination / name, ignore=shutil.ignore_patterns("__pycache__")
        )
    (destination / "reporting_plan.json").write_text(json.dumps(PLAN, indent=2), encoding="utf-8")
    # Retain hashes of external raw/processed files without duplicating gigabytes.
    referenced = {}
    eval_root = ROOT / "experiments/independent_v2"
    frame = pd.read_csv(destination / "independent/scores_compact.csv")
    for column in ["processed_path", "power_path"]:
        for value in frame[column].unique():
            path = eval_root / value
            referenced[str(path.relative_to(ROOT))] = digest(path)
    raw = pd.read_csv(eval_root / "data/raw/manifest.csv")
    for value in raw.raw_path.unique():
        path = eval_root / value
        referenced[str(path.relative_to(ROOT))] = digest(path)
    (destination / "external_data_hashes.json").write_text(json.dumps(referenced, indent=2))
    manifest = dict(
        created_utc=datetime.now(timezone.utc).isoformat(),
        files=sha_tree(destination),
        policy="Inspected independent result is now historical. Never tune against it and "
        "reuse it as untouched validation. New claims require another untouched population.",
    )
    (destination / "archive_manifest.json").write_text(json.dumps(manifest, indent=2))
    LOG.info("Preserved result archive: %s", destination)


def verify_archive(path):
    manifest = json.loads((path / "archive_manifest.json").read_text())
    for relative, expected in manifest["files"].items():
        if digest(path / relative) != expected:
            raise ValueError(f"Archived input changed: {relative}")
    for relative, expected in json.loads((path / "external_data_hashes.json").read_text()).items():
        if digest(ROOT / relative) != expected:
            raise ValueError(f"Referenced photometry changed: {relative}")


def paired_bootstrap(targets, repeats=5000, seed=20260916, k=100):
    """Resample targets, preserving paired scores; rerank at K in every replicate.

    Repeated draws are bootstrap copies, not accidental double-counted observed stars.
    Includes evaluation-sample/ranking uncertainty conditional on fixed trained models.
    """
    if targets.tic_id.duplicated().any() or len(targets) < k:
        raise ValueError("Require unique targets and at least K observations")
    frame = targets.sort_values("tic_id").reset_index(drop=True)
    ids = frame.tic_id.to_numpy()
    positive = frame.label.eq("planet").to_numpy()
    values = frame[["depth_snr", "hybrid_score"]].to_numpy()
    if not np.isfinite(values).all():
        raise ValueError("Non-finite primary ranking scores")

    def counts(draw):
        return [
            int(positive[draw[np.lexsort((ids[draw], -values[draw, j]))[:k]]].sum())
            for j in range(2)
        ]

    original = counts(np.arange(len(frame)))
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(repeats):
        draw = rng.integers(0, len(frame), len(frame))
        bls, hybrid = counts(draw)
        n_positive = int(positive[draw].sum())
        rows.append(
            dict(
                replicate=i,
                bls_recovered=bls,
                hybrid_recovered=hybrid,
                difference=hybrid - bls,
                positive_total=n_positive,
                recall_difference=(hybrid - bls) / n_positive if n_positive else np.nan,
            )
        )
    samples = pd.DataFrame(rows)
    low, high = samples.difference.quantile([0.025, 0.975])
    rlow, rhigh = samples.recall_difference.quantile([0.025, 0.975])
    return dict(
        k=k,
        n=len(frame),
        positive_total=int(positive.sum()),
        bls_recovered=original[0],
        hybrid_recovered=original[1],
        difference=original[1] - original[0],
        difference_ci_low=low,
        difference_ci_high=high,
        recall_difference=(original[1] - original[0]) / positive.sum()
        if positive.sum()
        else np.nan,
        recall_ci_low=rlow,
        recall_ci_high=rhigh,
        bootstrap_repeats=repeats,
        seed=seed,
        scope="Paired target resampling with reranking; conditional on frozen models. "
        "No training/calibration-refit or catalogue-label uncertainty.",
    ), samples


def review_selection(frame, k=100, per_group=2):
    targets = target_scores(frame)
    for score, name in [("depth_snr", "bls"), ("hybrid_score", "hybrid")]:
        order = targets.sort_values([score, "tic_id"], ascending=[False, True]).tic_id.tolist()
        targets[f"{name}_rank"] = targets.tic_id.map({tic: i + 1 for i, tic in enumerate(order)})
    pos = targets.label.eq("planet")
    bls, hybrid = targets.bls_rank.le(k), targets.hybrid_rank.le(k)
    groups = dict(
        both=pos & bls & hybrid,
        bls_only=pos & bls & ~hybrid,
        hybrid_only=pos & ~bls & hybrid,
        false_positive=targets.label.eq("false_positive"),
        background=targets.label.eq("background"),
    )
    rows = []
    for group, mask in groups.items():
        order = "bls_rank" if group == "bls_only" else "hybrid_rank"
        for target in (
            targets[mask].sort_values([order, "tic_id"]).head(per_group).to_dict("records")
        ):
            score = "depth_snr" if group == "bls_only" else "hybrid_score"
            row = (
                frame[frame.tic_id.eq(target["tic_id"])]
                .sort_values([score, "sector"], ascending=[False, True])
                .iloc[0]
                .to_dict()
            )
            row.update(
                review_group=group,
                bls_target_rank=target["bls_rank"],
                hybrid_target_rank=target["hybrid_rank"],
            )
            rows.append(row)
    return pd.DataFrame(rows)


def table(path, name, frame):
    frame.to_csv(path / "tables" / f"{name}.csv", index=False)


def generate(snapshot, output):
    verify_archive(snapshot)
    if output.exists():
        raise ValueError("Report output exists; reproduce into a new directory")
    (output / "tables").mkdir(parents=True)
    (output / "figures").mkdir()
    plan = json.loads((snapshot / "reporting_plan.json").read_text())
    independent = pd.read_csv(snapshot / "independent/metrics.csv")
    development = pd.read_csv(snapshot / "development_exposure/metrics.csv")
    table(output, "independent_metrics", independent)
    table(output, "development_calibration_metrics", development)
    table(
        output,
        "original_development_baseline",
        pd.read_csv(snapshot / "development_baseline/model_performance.csv"),
    )
    table(
        output,
        "independent_complementarity",
        pd.read_csv(snapshot / "independent/complementarity.csv"),
    )
    table(
        output,
        "development_complementarity",
        pd.read_csv(snapshot / "development_exposure/complementarity.csv"),
    )
    table(
        output, "search_eligibility", pd.read_csv(snapshot / "independent/search_eligibility.csv")
    )
    selection = []
    for family in ["generic", "bls", "physics", "all", "compact", "extended"]:
        f = pd.read_csv(snapshot / f"frozen/feature_selection_{family}.csv")
        f["family"] = family
        selection.append(f)
    table(output, "feature_selection", pd.concat(selection))
    definitions = {
        "mean_flux": ("Mean detrended relative flux", "relative flux"),
        "median_flux": ("Median detrended relative flux", "relative flux"),
        "std_flux": ("Population standard deviation of detrended flux", "relative flux"),
        "variance": ("Population variance of detrended flux", "relative flux squared"),
        "mad": ("1.4826 times median absolute deviation", "relative flux"),
        "rms": ("Root mean square of flux minus one", "relative flux"),
        "iqr": ("75th minus 25th flux percentile", "relative flux"),
        "min_flux": ("Minimum detrended flux", "relative flux"),
        "max_flux": ("Maximum detrended flux", "relative flux"),
        "peak_to_peak": ("Maximum minus minimum flux", "relative flux"),
        "skewness": ("Standardized third moment", "dimensionless"),
        "kurtosis": ("Fisher excess kurtosis", "dimensionless"),
        "point_to_point_scatter": (
            "MAD of within-segment successive differences / sqrt(2)",
            "relative flux",
        ),
        "difference_rms": ("RMS of within-segment successive differences", "relative flux"),
        "median_absolute_successive_difference": (
            "Median absolute within-segment successive difference",
            "relative flux",
        ),
        "percentile_amplitude": ("95th minus 5th flux percentile", "relative flux"),
        "baseline_days": ("Last minus first retained observation time", "days"),
        "n_observations": ("Retained unique cadences", "count"),
        "n_segments": ("Gap-separated segments", "count"),
        "duty_cycle": (
            "Cadence count times median cadence / (baseline + cadence), capped at one",
            "fraction",
        ),
        "largest_gap_days": ("Largest gap between retained times", "days"),
        "best_period": ("Period of strongest allowed BLS trial", "days"),
        "best_duration": ("Best-fit BLS box duration", "days"),
        "best_depth": ("Best-fit BLS relative depth", "relative flux"),
        "depth_error": ("BLS depth uncertainty under its noise model", "relative flux"),
        "depth_snr": ("BLS depth / depth error", "dimensionless"),
        "bls_max_power": (
            "Maximum BLS objective; equals depth SNR under SNR objective",
            "objective units",
        ),
        "bls_median_power": ("Median BLS objective over retained trials", "objective units"),
        "bls_peak_significance": (
            "(Maximum minus median power) / power MAD; not calibrated significance",
            "dimensionless",
        ),
        "number_expected_transits": (
            "Predicted epoch crossings within baseline, regardless of gaps",
            "count",
        ),
        "number_observed_transits": (
            "Distinct transit epochs with at least one sampled in-transit point",
            "count",
        ),
        "in_transit_points": ("Cadences inside the selected BLS transit window", "count"),
        "median_in_transit": ("Median flux inside the BLS window", "relative flux"),
        "median_out_transit": (
            "Median flux farther than one duration from transit centre",
            "relative flux",
        ),
        "measured_depth": ("Out-of-transit minus in-transit median", "relative flux"),
        "asymmetry_proxy": ("First-half minus second-half transit median", "relative flux"),
        "odd_even_difference": ("Odd minus even in-transit median flux", "relative flux"),
        "odd_even_significance": (
            "Absolute odd/even difference / event-scatter uncertainty; diagnostic",
            "dimensionless",
        ),
        "secondary_depth_proxy": (
            "Out-of-transit median minus phase-0.5 window median",
            "relative flux",
        ),
        "fraction_in_transit": ("In-transit fraction of retained observations", "fraction"),
        "radius_ratio_proxy": (
            "sqrt(BLS depth), only for depths between zero and one",
            "dimensionless",
        ),
        "radius_earth_proxy": (
            "Radius-ratio proxy times catalogue stellar radius; default ML exclusion",
            "Earth radii",
        ),
        "duration_ratio_proxy": (
            "Observed duration / circular central-transit duration proxy; default ML exclusion",
            "dimensionless",
        ),
        "event_depth_relative_mad": (
            "Local per-event depth MAD / absolute median depth, >=3 events",
            "dimensionless",
        ),
        "event_duration_relative_mad": (
            "Sampled half-depth width MAD / median width, >=3 events",
            "dimensionless",
        ),
        "single_event_power_fraction_proxy": (
            "Largest positive event depth-squared count/noise-squared contribution / total",
            "fraction",
        ),
        "local_noise_beta": (
            "Observed local bin-mean scatter / white-noise expectation",
            "dimensionless",
        ),
        "edge_to_centre_depth_ratio": (
            "Outer transit-region depth / central-region depth",
            "dimensionless",
        ),
        "ingress_egress_difference": (
            "Ingress-side minus egress-side outer-region median flux",
            "relative flux",
        ),
        "secondary_scan_depth": (
            "Maximum median dip over 80 phase positions outside primary region",
            "relative flux",
        ),
        "secondary_scan_depth_ratio": ("Secondary-scan depth / BLS primary depth", "dimensionless"),
    }
    names = sorted(set(pd.concat(selection).feature))
    table(
        output,
        "feature_definitions",
        pd.DataFrame(
            [
                dict(feature=name, definition=definitions[name][0], units=definitions[name][1])
                for name in names
            ]
        ),
    )
    contract = json.loads((snapshot / "frozen/protocol.json").read_text())
    split = pd.DataFrame({"tic_id": contract["development_ids"]})
    split["role"] = np.where(
        split.tic_id.isin(contract["training_ids"]),
        "training",
        np.where(
            split.tic_id.isin(contract["calibration_ids"]),
            "calibration",
            "earlier_inspected_excluded_only",
        ),
    )
    table(output, "development_split_ids", split)
    flow = []
    for name in ["development", "evaluation"]:
        root = snapshot / name
        selected = pd.read_csv(root / "data/catalog/sample.csv")
        downloaded = pd.read_csv(root / "data/raw/manifest.csv")
        processed = pd.read_csv(root / "data/processed/manifest.csv")
        for label in ["planet", "false_positive", "background"]:
            ids = set(selected.loc[selected.label.eq(label), "tic_id"])
            requested = contract["config"]["data"][
                {
                    "planet": "sample_size_planets",
                    "false_positive": "sample_size_false_positive",
                    "background": "sample_size_background",
                }[label]
            ]
            flow.append(
                dict(
                    population=name,
                    label=label,
                    requested=requested,
                    selected=len(ids),
                    downloaded=len(ids & set(downloaded.tic_id)),
                    analysed=len(ids & set(processed.tic_id)),
                    usable_target_sector_rows=int(processed.tic_id.isin(ids).sum()),
                )
            )
    flow = pd.DataFrame(flow)
    table(output, "sample_selection_attrition", flow)
    settings = [
        {"stage": stage, "parameter": key, "value": json.dumps(value)}
        for stage in ["preprocessing", "bls", "models"]
        for key, value in contract["config"][stage].items()
    ]
    table(output, "preprocessing_and_search_settings", pd.DataFrame(settings))
    frame = pd.read_csv(snapshot / "independent/scores_compact.csv", float_precision="round_trip")
    uncertainty = []
    sector_counts = []
    for exposure, subset in [("all_sectors", frame), ("one_sector", one_sector(frame))]:
        targets = target_scores(subset)
        result, draws = paired_bootstrap(
            targets, plan["bootstrap_repeats"], plan["bootstrap_seed"], plan["budget"]
        )
        result["exposure"] = exposure
        uncertainty.append(result)
        table(output, f"bootstrap_draws_{exposure}", draws)
        counts = targets.groupby(["label", "n_sectors"]).size().rename("targets").reset_index()
        counts["exposure"] = exposure
        sector_counts.append(counts)
    uncertainty = pd.DataFrame(uncertainty)
    table(output, "paired_primary_uncertainty", uncertainty)
    table(output, "sector_coverage", pd.concat(sector_counts))
    review = review_selection(frame, plan["budget"], plan["review_per_group"])
    table(output, "diagnostic_review_selection", review)
    # Copy exact photometry for selected illustrations into the report package.
    (output / "diagnostic_data").mkdir()
    for row in review.to_dict("records"):
        stem = f"{row['review_group']}_tic{int(row['tic_id'])}_s{int(row['sector'])}"
        root = ROOT / "experiments/independent_v2"
        with np.load(root / row["processed_path"]) as c, np.load(root / row["power_path"]) as p:
            diagnostic(dict(c), dict(p), row, output / "figures" / "diagnostics" / stem)
        shutil.copy2(root / row["processed_path"], output / "diagnostic_data" / f"{stem}_curve.npz")
        shutil.copy2(root / row["power_path"], output / "diagnostic_data" / f"{stem}_power.npz")
    injections = pd.read_csv(snapshot / "injections/injection_trials.csv")
    table(output, "injection_trials", injections)
    table(output, "injection_summary", pd.read_csv(snapshot / "injections/injection_summary.csv"))
    figures(output, frame, independent, development, flow, uncertainty, injections)
    write_manuscript(output, uncertainty, review, contract)
    (output / "artifact_checksums.json").write_text(json.dumps(sha_tree(output), indent=2))
    LOG.info("Paper artifacts: %s", output)


def figures(output, frame, metrics, development, flow, uncertainty, injections):
    out = output / "figures"
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    for ax, population in zip(axes, ["development", "evaluation"]):
        group = flow[flow.population.eq(population)]
        x = np.arange(len(group))
        for j, column in enumerate(["requested", "selected", "analysed"]):
            ax.bar(x + (j - 1) * 0.23, group[column], width=0.23, label=column)
        ax.set(
            xticks=x,
            xticklabels=["Hosts", "False positives", "Background"],
            ylabel="Targets",
            title=population.title(),
        )
        ax.legend(fontsize=8)
    save(fig, out / "sample_selection")
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    for ax, exposure in zip(axes, ["all_sectors", "one_sector"]):
        for method, label in [
            ("depth_snr", "BLS"),
            ("hybrid_score", "Compact hybrid"),
            ("ensemble_score", "Compact ensemble"),
        ]:
            sub = metrics[
                metrics.family.eq("compact")
                & metrics.exposure.eq(exposure)
                & metrics.method.eq(method)
            ].sort_values("k")
            ax.plot(sub.k, sub.recall_at_k, "o-", label=label)
        ax.set(
            xlabel="Inspection budget K",
            ylabel="Catalogue-host recall",
            title=exposure.replace("_", " "),
        )
        ax.legend(fontsize=8)
    save(fig, out / "independent_recovery")
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    for ax, data, title in zip(
        axes,
        [development, metrics],
        ["Development calibration (not independent)", "Independent evaluation"],
    ):
        sub = data[
            data.method.eq("hybrid_score") & data.k.eq(100) & data.exposure.eq("all_sectors")
        ]
        ax.bar(sub.family, sub.recovered, color="#4477aa")
        base = (
            data[data.method.eq("depth_snr") & data.k.eq(100) & data.exposure.eq("all_sectors")]
            .iloc[0]
            .recovered
        )
        ax.axhline(base, color="#cc6677", ls="--", label="BLS")
        ax.set(ylabel="Hosts recovered at K=100", title=title)
        ax.tick_params(axis="x", rotation=35)
        ax.legend()
    save(fig, out / "hybrid_feature_comparisons")
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.errorbar(
        uncertainty.difference,
        np.arange(2),
        xerr=[
            uncertainty.difference - uncertainty.difference_ci_low,
            uncertainty.difference_ci_high - uncertainty.difference,
        ],
        fmt="o",
        capsize=5,
    )
    ax.axvline(0, color="grey", ls="--")
    ax.set(
        yticks=[0, 1],
        yticklabels=["All sectors", "One sector"],
        xlabel="Hybrid − BLS hosts recovered at K=100",
        title="Paired target bootstrap; models held fixed",
    )
    save(fig, out / "paired_primary_uncertainty")
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for method, group in injections[injections.status.eq("ok")].groupby("method"):
        sub = group.groupby("injected_depth").direct_period_recovered.mean()
        axes[0].plot(sub.index, sub.values, "o-", label=method)
        sub = group.groupby("injected_depth").paired_depth_relative_bias.median()
        axes[1].plot(sub.index, sub.values * 100, "o-", label=method)
    axes[0].set(ylabel="Direct-period retrieval fraction", ylim=(0, 1))
    axes[1].set(ylabel="Median paired depth bias [%]")
    for ax in axes:
        ax.set(xscale="log", xlabel="Injected relative depth")
        ax.legend(fontsize=8)
    fig.suptitle("Development injection pilot: 6 real targets, 108 signals per method")
    save(fig, out / "injection_comparison")
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    targets = target_scores(frame)
    for label, group in targets.groupby("label"):
        axes[0].scatter(group.depth_snr, group.hybrid_score, s=10, alpha=0.5, label=label)
    axes[0].set(xscale="log", xlabel="BLS depth SNR", ylabel="Frozen compact hybrid score")
    axes[0].legend(fontsize=8)
    counts = targets.groupby(["label", "n_sectors"]).size().unstack(fill_value=0)
    counts.plot.bar(ax=axes[1], rot=20)
    axes[1].set(ylabel="Targets", xlabel="Reference population", title="Usable sector coverage")
    save(fig, out / "independent_scores_and_coverage")
    g = pd.read_csv(output / "tables/search_eligibility.csv")
    g = g[g.family.eq("compact") & g.exposure.eq("all_sectors") & g.label.eq("planet")]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(
        ["Grid eligible", "Known, outside grid", "Period missing"],
        [
            g.search_eligible.sum(),
            (g.period_known & ~g.search_eligible).sum(),
            (~g.period_known).sum(),
        ],
    )
    ax.set(
        ylabel="Catalogue-positive hosts",
        title="Representative-period eligibility; not transit visibility",
    )
    save(fig, out / "search_eligibility")
    c = pd.read_csv(output / "tables/independent_complementarity.csv")
    c = c[c.family.eq("compact")]
    fig, ax = plt.subplots(figsize=(7, 4))
    x = np.arange(len(c))
    ax.bar(x - 0.2, c.bls_recovered, 0.4, label="BLS")
    ax.bar(x + 0.2, c.complement_recovered, 0.4, label="80 BLS + 20 additional anomalies")
    ax.set(xticks=x, xticklabels=c.exposure, ylabel="Hosts recovered at K=100")
    ax.legend(fontsize=8)
    save(fig, out / "complementarity")


def write_manuscript(output, uncertainty, review, contract):
    a = uncertainty[uncertainty.exposure.eq("all_sectors")].iloc[0]
    b = uncertainty[uncertainty.exposure.eq("one_sector")].iloc[0]
    text = f"""# Interpretable unsupervised anomaly ranking of transit-like signals in TESS photometry

## Abstract

We investigate astrophysically motivated, unsupervised anomaly ranking alongside Box Least Squares (BLS) transit searches in public TESS photometry. Physics-informed denotes feature engineering, not physical equations enforced during training. Quality filtering, normalization, segment-local detrending and BLS searches yield variability, transit morphology and event-coherence features. Catalogue-dependent stellar proxies are excluded from default model inputs. Following descriptive development on 996 targets, models were fitted without labels on 796 targets and score calibration used 200 separate development targets. The compact feature hypothesis was informed by earlier labelled development results; transformations, models and ranking formula were frozen before independent evaluation. On 924 target-disjoint evaluation targets, including 300 catalogue-positive hosts, the compact hybrid recovered {int(a.hybrid_recovered)}/300 hosts at an inspection budget of 100, compared with {int(a.bls_recovered)}/300 for BLS. The paired target-bootstrap interval for the difference of {int(a.difference)} hosts was [{a.difference_ci_low:g}, {a.difference_ci_high:g}], conditional on the frozen models. Single-sector and fixed-allocation complementary rankings also did not exceed BLS recovery at this budget. Injection experiments characterize a detrending tradeoff, while diagnostic plots describe associations rather than causal attribution or planetary validation. The experiment demonstrates a reproducible independent evaluation but does not demonstrate improved catalogue-host recovery or reduced inspection workload.

## 1. Research question

Do interpretable unsupervised anomaly scores add useful candidate-prioritisation information beyond conventional BLS statistics at a fixed inspection budget? An unusual light curve need not contain a planet. Catalogue-positive host recovery is the operational reference outcome; it is not confirmed transit recovery or true planetary purity.

## 2. Data and populations

The development sample contains 996 targets: 300 planet/candidate hosts, 196 false-positive references and 500 unlabelled backgrounds, in sectors 1–13. The independent sample contains 924 targets: 300 hosts, 124 false positives and 500 backgrounds, in sectors 14–26. Requested false-positive counts exceeded available samples; the actual counts are reported. All selected independent targets produced usable features, yielding 1,415 target-sector curves. Independent targets do not overlap the 1,064 previously inspected systems, including earlier small experiments. Catalogue-stratified sampling, incomplete labels and changed sector coverage limit survey-wide inference. Backgrounds are not verified negatives. Tables preserve sample IDs, requested/selected/analysed counts and failure records.

## 3. Methods

Raw quality flags are retained during acquisition, then mask 175 is applied during preprocessing. Flux is normalized and detrended separately across gaps larger than 0.25 days, using a 1.5-day Savitzky–Golay window with iterative masking during trend estimation. Negative observations are not simply clipped from the light curve. Weighted BLS searches use trial periods from 0.5 days to the smaller of 12 days and half the observed baseline, durations of 1–4 hours, and the SNR objective. Automatic period-grid overshoots are explicitly removed. This baseline cap is a heuristic support criterion, not proof of observed transit visibility.

Feature families include generic variability/observing properties, BLS statistics, morphology proxies, all legacy features, compact morphology/coherence and an extended family. Event-depth and sampled-width consistency, event dominance, local binned-noise ratios, edge/centre morphology and a coarse secondary-phase scan are measured. These are approximate photometric diagnostics; none independently validates a planet. Feature definitions and missing-data/selection decisions accompany the supplement. Compact and extended redundancy removal uses absolute Spearman correlation ≥0.95 on training data only, in fixed feature order. Stellar-catalogue radius and duration-consistency proxies remain excluded by default because measurement availability is population-dependent.

The 796 training targets fit median imputation, robust scaling, Isolation Forest and novelty-enabled Local Outlier Factor without labels. Separate 200-target development calibration distributions fix midpoint empirical CDF score mappings; calibration uses one coverage-selected curve per target. Equal-weight IF and LOF calibrated percentiles form the ensemble; BLS and ensemble percentiles form the fixed hybrid. Evaluation never refits transforms, models or score calibration. Choosing compact features was motivated by prior labelled development comparisons and is disclosed as label-informed experiment selection, despite unsupervised fitting.

The primary analysis takes each method's maximum score across sectors per TIC. A sensitivity analysis selects the sector with most valid cadences, then longest baseline, then smallest sector number, without reading scores or labels. ROC-AUC/AP use CP/KP hosts versus FP/FA references, excluding PC-only hosts and backgrounds. Full-sample recall retains all hosts; an additional denominator includes the 192 hosts whose representative periods lie within the effective grid. Fourteen hosts lack usable periods and 94 have known periods outside the effective grid. Eligibility is not an ephemeris-based visibility or multi-planet completeness calculation.

A fixed complementary list contains 80 BLS-selected targets plus the 20 highest anomaly-ranked targets not already selected. Additional and lost hosts are both reported. The reporting-stage uncertainty analysis resamples independent targets jointly for BLS and hybrid, then reranks the resampled target copies at K=100 in 5,000 replicates. Percentile 95% intervals describe evaluation-sample and ranking variability conditional on the frozen models. They do not include training/calibration-refit uncertainty, label errors, or population-selection bias. The pre-existing complementarity intervals instead condition on fixed inspection lists; these two uncertainty definitions must not be conflated. No bootstrap interval is presented as a formal causal or discovery significance test.

## 4. Results

The frozen primary compact hybrid recovers {int(a.hybrid_recovered)}/300 hosts (9.3%) at K=100, versus {int(a.bls_recovered)}/300 (11.0%) for BLS, a difference of {int(a.difference)} hosts (−1.7 percentage points of host recall). The paired reranked-bootstrap interval is [{a.difference_ci_low:g}, {a.difference_ci_high:g}] hosts. The single-sector comparison gives hybrid {int(b.hybrid_recovered)} versus BLS {int(b.bls_recovered)}, difference {int(b.difference)}, interval [{b.difference_ci_low:g}, {b.difference_ci_high:g}]. At the same all-sector budget, the compact ensemble recovers 23 hosts. The 80/20 complementary list recovers 27 versus 33 for BLS, gaining one and losing seven hosts. Under one-sector selection it recovers 28 versus 34. None of the alternative hybrid feature-family comparisons exceeds BLS at K=100. These comparisons are reported without choosing a new primary method after viewing independent outcomes.

All 216 pre-detrending injection trials succeeded: 108 paired signals per method, across six real light curves, three depths, three periods and two durations. Savitzky–Golay retrieved the injected period in 60/108 trials; rolling median in 55/108. Median paired template-depth bias was −7.3% and −1.6%, respectively. This small trapezoid-in-real-noise pilot indicates a depth-preservation/retrieval tradeoff, not general survey completeness. Existing noise and uncertainties were retained; no photon-noise realization was regenerated. Uninjected controls can contain real signals and therefore do not establish calibrated false-alarm rates.

## 5. Diagnostic review and limitations

The supplement selects two examples each from common recoveries, BLS-only recoveries, hybrid-only recoveries, false positives and high-ranked backgrounds using a fixed rank/TIC rule. The rule was established after aggregate evaluation results were inspected, before object-level review. Selection is descriptive, not evidence of prevalence or an independent confirmatory experiment. Each plot shows retained photometry, detrended flux, BLS power and folded morphology. Review notes distinguish measured properties, visual observations and unresolved interpretations. Neither catalogue membership nor a periodogram peak establishes that the detected dip is planetary; morphology associations are not formal per-object model attribution.

Performance differs from the original development experiment (BLS 45 versus all-feature hybrid 25 at K=100), which used the inspected sample for fitting and ranking. That baseline, the development calibration diagnostics, and the independent result are tabulated separately. Differences cannot be assigned uniquely to model generalisation because populations, representation choices and score calibration differ. Sector coverage and catalogue selection remain confounders. The now-inspected independent sample cannot serve as untouched validation for future changes motivated by these results.

## 6. Conclusion

This work implements and independently evaluates an interpretable, unsupervised anomaly-ranking layer alongside BLS. The compact hybrid recovered 28/300 catalogue-positive hosts among the top 100 targets, compared with 33/300 for BLS. The evaluated anomaly and complementary rankings did not demonstrate improved recovery at this budget. No reduction in manual inspection time or validated planetary discovery is established. A credible contribution is the reproducible framework, transparent negative comparison, coverage-aware diagnostics and documented preprocessing tradeoffs. New model choices based on the present evaluation require another untouched population for new generalisation claims.

## Data and code availability

The local archive preserves evaluated scores, settings, models, source snapshot, dependency versions, IDs and SHA-256 checksums. Referenced raw and processed data remain in the repository experiment workspace; external-data checksums identify them. The report includes copies of all selected diagnostic curves. A clean-machine reproduction must restore those referenced files or reacquire the matching public observations before verifying hashes. The archive is not a standalone copy of the full photometry collection. See REPRODUCE.md for the exact workflow. Journal-specific formatting, author information and a final literature/context review remain author tasks.
"""
    (output / "manuscript.md").write_text(text, encoding="utf-8")
    abstract = text.split("## Abstract\n\n")[1].split("\n\n## 1.")[0]
    (output / "abstract.md").write_text(
        "# Research abstract\n\n" + abstract + "\n", encoding="utf-8"
    )
    (output / "REPRODUCE.md").write_text(
        "# Reproduce the preserved paper analysis\n\n"
        "From the repository directory, using the recorded Python environment:\n\n"
        "```powershell\npython scripts/paper_report.py --reproduce --archive paper/archive_2026-09-16 "
        "--output paper/reproduction\n```\n\n"
        "The command verifies archive and referenced photometry hashes, resamples paired targets with "
        "the saved seed and regenerates tables, figures and manuscript into a new directory. It never "
        "refits models or overwrites the independent evaluation. Copies of scripts, tests, frozen source, "
        "package versions and requirements-lock.txt are retained in the archive. Restore the frozen "
        "source and recorded environment if the working scientific code changes. Human visual review "
        "notes are a separate supplement and are not regenerated as if produced by an algorithm.\n\n"
        "Run `python -m pytest -q` for checks. Exact numerical table equality is expected under the "
        "recorded environment; PDF timestamps can differ, so figure file hashes need not match. "
        "The independent sample is now inspected: do not reuse it as untouched validation after tuning.\n",
        encoding="utf-8",
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, default=Path("paper/archive_2026-09-16"))
    parser.add_argument("--output", type=Path, default=Path("paper/final"))
    parser.add_argument("--reproduce", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("fontTools.subset").setLevel(logging.WARNING)
    if not args.reproduce:
        archive(args.archive)
    generate(args.archive, args.output)


if __name__ == "__main__":
    main()
