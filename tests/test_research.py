import copy
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import pytest
import yaml

from tess_anomaly.coherence import COHERENCE, COMPACT, coherence_features
from tess_anomaly.config import load_config
from tess_anomaly.dataset import fit_transform
from tess_anomaly.real_injections import inject, run_injections
from tess_anomaly.research import (
    complement_metrics,
    complement_selection,
    eligibility,
    evaluate_scores,
    fit_bundle,
    one_sector,
    score_bundle,
)


def fixtures():
    cfg = load_config(Path(__file__).parents[1] / "config/default.yaml")
    cfg["models"]["isolation_forest"]["n_estimators"] = 20
    cfg["evaluation"]["top_k"] = [5, 10]
    protocol = dict(
        families=["compact"],
        primary_family="compact",
        correlation_threshold=0.95,
        budget=10,
        bls_fraction=0.8,
        bootstrap_seed=4,
        bootstrap_repeats=100,
    )
    rng = np.random.default_rng(5)
    frame = pd.DataFrame({c: rng.uniform(0.1, 1, 80) for c in COMPACT})
    frame["tic_id"] = np.arange(80)
    frame["sector"] = 1
    frame["label"] = ["planet", "false_positive", "background", "background"] * 20
    frame["disposition"] = ["CP", "FP", "UNLABELLED", "UNLABELLED"] * 20
    frame["bls_max_power"] = frame.depth_snr
    frame["catalog_period"] = 3.0
    frame["baseline_days"] = 25.0
    frame["n_observations"] = 1000
    return cfg, protocol, frame


def test_frozen_scoring_is_label_free_batch_invariant_and_disjoint(tmp_path):
    cfg, protocol, frame = fixtures()
    bundle = fit_bundle(frame.iloc[:40], frame.iloc[40:60], cfg, protocol)
    bundle["development_ids"] = list(range(60))
    before = copy.deepcopy(bundle["models"]["compact"]["transform"].pipeline["imputer"].statistics_)
    joblib.dump(bundle, tmp_path / "frozen.joblib")
    bundle = joblib.load(tmp_path / "frozen.joblib")
    test = frame.iloc[60:]
    original = score_bundle(bundle, test)["compact"]
    single = score_bundle(bundle, test.iloc[:1])["compact"]
    np.testing.assert_array_equal(original.hybrid_score.iloc[:1], single.hybrid_score)
    changed = test.assign(label="planet", disposition="CP", catalog_period=9000)
    np.testing.assert_array_equal(
        original.hybrid_score, score_bundle(bundle, changed)["compact"].hybrid_score
    )
    np.testing.assert_array_equal(
        before, bundle["models"]["compact"]["transform"].pipeline["imputer"].statistics_
    )
    with pytest.raises(ValueError, match="development"):
        score_bundle(bundle, frame.iloc[:2])
    with pytest.raises(ValueError, match="overlap"):
        fit_bundle(frame.iloc[:40], frame.iloc[30:60], cfg, protocol)
    evaluate_scores(
        {"compact": original}, bundle, tmp_path / "evaluation", "Synthetic workflow test"
    )
    metrics = pd.read_csv(tmp_path / "evaluation/metrics.csv")
    assert set(metrics.exposure) == {"all_sectors", "one_sector"}
    assert (metrics.eligible_positive_total == 5).all()


def test_redundancy_is_selected_from_training_only():
    x = np.arange(30.0)
    frame = pd.DataFrame({"std_flux": x, "variance": x * x, "mad": np.sin(x)})
    cfg = dict(max_missing_fraction=0.6, scaler="robust", correlation_threshold=0.95)
    transform, _ = fit_transform(frame, cfg, columns=list(frame))
    assert transform.columns == ["std_flux", "mad"]
    assert (
        transform.missingness.set_index("feature").loc["variance", "redundant_with"] == "std_flux"
    )
    transform.transform(frame.assign(variance=np.cos(x)))
    assert transform.columns == ["std_flux", "mad"]


def test_sector_choice_and_eligible_denominator_do_not_use_scores():
    cfg, _, frame = fixtures()
    two = frame.iloc[:2].copy()
    two["sector"] = 2
    two["n_observations"] = 2000
    two["depth_snr"] = -100
    both = pd.concat([frame, two])
    chosen = one_sector(both)
    assert chosen.set_index("tic_id").loc[0, "sector"] == 2
    both.loc[both.tic_id.eq(0), "catalog_period"] = 13
    both.loc[both.tic_id.eq(4), "catalog_period"] = np.nan
    grid = eligibility(both, cfg).set_index("tic_id")
    assert not grid.loc[0, "search_eligible"]
    assert not grid.loc[4, "period_known"]
    assert len(grid) == 80


def test_complement_is_deduplicated_and_counts_gains_and_losses():
    targets = pd.DataFrame(
        dict(
            tic_id=np.arange(120),
            depth_snr=np.arange(120)[::-1],
            ensemble_score=np.arange(120),
            label="background",
        )
    )
    targets.loc[[0, 90, 110], "label"] = "planet"
    baseline, combined = complement_selection(targets, 100, 0.8)
    assert len(set(combined)) == 100
    assert combined[:80] == list(range(80))
    assert baseline == list(range(100))
    result, _ = complement_metrics(
        targets, dict(budget=100, bls_fraction=0.8, bootstrap_seed=2, bootstrap_repeats=100)
    )
    assert result["additional_hosts"] == result["lost_hosts"] == 1
    assert result["net_recovery_difference"] == 0


def test_coherence_detects_event_dominance_and_off_half_secondary():
    rng = np.random.default_rng(22)
    t = np.arange(0, 25, 0.005)
    from tess_anomaly.bls import phase

    ph = phase(t, 3, 0.8)
    f = 1 + rng.normal(0, 0.0001, len(t))
    f[np.abs(ph) < 0.06] -= 0.01
    f[np.abs(phase(t, 3, 0.8 + 0.3 * 3)) < 0.06] -= 0.004
    curve = dict(time=t, flux=f, segment=np.zeros(len(t)))
    transit = dict(best_period=3, best_duration=0.12, transit_epoch=0.8, best_depth=0.01)
    regular = coherence_features(curve, transit)
    assert regular["secondary_scan_depth"] > 0.003
    assert regular["event_depth_relative_mad"] < 0.05
    modified = f.copy()
    modified[np.abs(t - 0.8) < 0.06] -= 0.04
    dominant = coherence_features(dict(curve, flux=modified), transit)
    assert (
        dominant["single_event_power_fraction_proxy"] > regular["single_event_power_fraction_proxy"]
    )
    assert set(regular) == set(COHERENCE)


def test_real_injections_preserve_raw_and_record_paired_methods(tmp_path):
    from tess_anomaly.utils import synthetic_curve

    cfg, _, _ = fixtures()
    cfg["root"] = str(tmp_path)
    (tmp_path / "data/raw").mkdir(parents=True)
    raw, _ = synthetic_curve()
    original = raw["flux"].copy()
    changed = inject(raw, 3.2, 0.8, 0.12, 0.01)
    np.testing.assert_array_equal(original, raw["flux"])
    assert changed["flux"].min() < original.min()
    np.savez(tmp_path / "data/raw/curve.npz", **raw)
    pd.DataFrame([dict(tic_id=1, sector=1, raw_path="data/raw/curve.npz")]).to_csv(
        tmp_path / "data/raw/manifest.csv", index=False
    )
    run_injections(
        cfg,
        dict(
            seed=4,
            n_targets=1,
            periods_days=[3.2],
            depths=[0.01],
            durations_hours=[3],
            phases_per_case=1,
            methods=["savgol", "rolling_median"],
            period_tolerance=0.01,
        ),
        tmp_path / "injections",
    )
    result = pd.read_csv(tmp_path / "injections/injection_trials.csv")
    assert len(result) == 2
    assert result.status.eq("ok").all()
    assert result.epoch.nunique() == 1
    assert result.paired_template_depth.between(0.005, 0.015).all()
    with np.load(tmp_path / "data/raw/curve.npz") as stored:
        np.testing.assert_array_equal(stored["flux"], original)


def test_freeze_prepare_and_independent_evaluation_end_to_end(tmp_path, monkeypatch):
    from tess_anomaly import research

    cfg, protocol, frame = fixtures()
    development = tmp_path / "development"
    (development / "data/catalog").mkdir(parents=True)
    frame[["tic_id"]].to_csv(development / "data/catalog/sample.csv", index=False)
    cfg["workspace"] = str(development)
    config = tmp_path / "development.yaml"
    config.write_text(yaml.safe_dump(cfg))
    protocol["calibration_fraction"] = 0.25
    settings = tmp_path / "protocol.yaml"
    settings.write_text(yaml.safe_dump(protocol))
    unseen = frame.iloc[:20].copy()
    unseen["tic_id"] += 1000
    monkeypatch.setattr(
        research, "enriched_features", lambda root: frame if root == development else unseen
    )
    frozen = tmp_path / "frozen"
    research.freeze(config, settings, frozen)
    loaded = research.load_frozen(frozen)
    assert set(loaded["training_ids"]).isdisjoint(loaded["calibration_ids"])
    assert len(loaded["development_ids"]) == 80
    with pytest.raises(ValueError, match="already exists"):
        research.freeze(config, settings, frozen)
    evaluation = tmp_path / "evaluation"
    eval_config = tmp_path / "evaluation.yaml"
    research.prepare_evaluation(frozen, evaluation, eval_config)
    (evaluation / "outputs").mkdir()
    (evaluation / "outputs/config_used.yaml").write_text(eval_config.read_text())
    (evaluation / "data/features").mkdir(parents=True)
    (evaluation / "data/catalog").mkdir(parents=True)
    unseen.to_csv(evaluation / "data/features/features.csv", index=False)
    unseen[["tic_id"]].to_csv(evaluation / "data/catalog/sample.csv", index=False)
    research.evaluate_independent(frozen, evaluation, tmp_path / "results")
    assert (tmp_path / "results/evaluation_provenance.json").exists()
    monkeypatch.setattr(research, "source_digest", lambda: "changed")
    with pytest.raises(ValueError, match="Source differs"):
        research.load_frozen(frozen)
