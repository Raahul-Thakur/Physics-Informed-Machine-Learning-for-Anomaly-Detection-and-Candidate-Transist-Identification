"""Verify strict BLS bounds and primary/all-feature ablation reproducibility."""

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from tess_anomaly.config import load_config
from tess_anomaly.evaluation import score_columns
from tess_anomaly.pipeline import train_frame


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="config/default.yaml")
    args = parser.parse_args()
    cfg = load_config(args.config)
    root = Path(cfg["root"])
    features = pd.read_csv(root / "data/features/features.csv")
    scores = pd.read_csv(
        root / "outputs/rankings/ranked_light_curves.csv", float_precision="round_trip"
    )
    keys = ["tic_id", "sector"]
    refit, _, _ = train_frame(features, cfg)
    expected = refit.set_index(keys).sort_index()
    actual = scores.set_index(keys).sort_index()
    pd.testing.assert_index_equal(expected.index, actual.index)
    errors = {}
    for column in score_columns(refit):
        np.testing.assert_array_equal(expected[column], actual[column])
        errors[column] = float(np.max(np.abs(expected[column] - actual[column])))
    metrics = pd.read_csv(root / "outputs/tables/model_performance.csv")
    ablation = pd.read_csv(root / "outputs/tables/ablation_results.csv")
    all_features = ablation[ablation.feature_family.eq("all")].drop(columns="feature_family")
    pd.testing.assert_frame_equal(metrics, all_features.reset_index(drop=True), check_exact=True)
    for row in features.to_dict("records"):
        cap = min(cfg["bls"]["max_period_days"], row["baseline_days"] / cfg["bls"]["min_transits"])
        lower = cfg["bls"]["min_period_days"]
        with np.load(root / row["power_path"]) as archive:
            periods = archive["period"]
            assert np.all((periods >= lower) & (periods <= cap)), row["tic_id"]
        assert lower <= row["best_period"] <= cap, row["tic_id"]
    hosts = features[features.label.eq("planet")].drop_duplicates("tic_id")
    outside = hosts.catalog_period.notna() & ~hosts.catalog_period.between(
        cfg["bls"]["min_period_days"], cfg["bls"]["max_period_days"]
    )
    candidates = pd.read_csv(root / "outputs/tables/top_candidates.csv")
    result = {
        "light_curves_checked": len(features),
        "unique_targets": int(features.tic_id.nunique()),
        "all_trial_periods_within_bounds": True,
        "all_feature_scores_exactly_reproduce_primary": True,
        "maximum_absolute_score_differences": errors,
        "all_feature_metrics_exactly_reproduce_primary": True,
        "hosts": len(hosts),
        "representative_periods_outside_configured_grid": int(outside.sum()),
        "top_candidate_labels": candidates.label.value_counts().to_dict(),
        "generalisation_and_workload_reduction_independently_evaluated": False,
    }
    path = root / "outputs/tables/correction_verification.json"
    path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
