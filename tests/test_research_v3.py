"""Behavioural tests of the prospective extension, using synthetic data only."""

import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("v3", ROOT / "scripts/research_v3.py")
v3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v3)


def frame(n=60, offset=0, sector=1):
    rng = np.random.default_rng(91 + offset)
    f = pd.DataFrame({c: rng.uniform(0.1, 1, n) for c in v3.COMPACT})
    f["tic_id"] = np.arange(offset + 1, offset + n + 1)
    f["sector"] = sector
    f["label"] = np.resize(["planet", "false_positive", "background"], n)
    f["disposition"] = np.resize(["CP", "FP", ""], n)
    f["n_observations"] = 1000
    f["baseline_days"] = 26
    f["best_period"] = 2.0
    f["best_duration"] = 0.1
    f["best_depth"] = 0.01
    f["depth_snr"] = rng.uniform(1, 50, n)
    f["number_observed_transits"] = 3
    f["transit_epoch"] = 2000.0
    f["catalog_period"] = 2.0
    f["time_system"] = "BTJD (BJD_TDB - 2457000)"
    return f


@pytest.fixture
def protocol():
    p = yaml.safe_load((ROOT / "config/research_v3.yaml").read_text())
    p.update(trees=10, neighbors=5, bootstrap_repeats=20, budget=5, explain_n=1)
    return p


@pytest.fixture
def bundle(protocol):
    return v3.fit(frame(), frame(20, 100, 14), protocol)


def test_unknown_and_conflicting_labels():
    f = frame(6)
    f["disposition"] = ["PC", "FP", "CP", "CP;FP", "FA", "KP"]
    assert v3.reference_labels(f).tolist() == [-1, 0, -1, -1, 0, -1]


def test_partitions_and_protocol_reject_leakage(protocol):
    with pytest.raises(ValueError, match="Target leakage"):
        v3.fit(frame(), frame(20, 0, 14), protocol)
    with pytest.raises(ValueError, match="Sector leakage"):
        v3.fit(frame(), frame(20, 100, 1), protocol)
    protocol["evaluation_sectors"] = [14]
    with pytest.raises(ValueError, match="Sector partitions"):
        v3.validate_protocol(protocol)


def test_unsupervised_scores_ignore_labels_and_order(protocol):
    a = frame()
    b = a.copy()
    b["label"] = np.resize(["false_positive", "planet", "background"], len(b))
    b["disposition"] = np.resize(["FP", "CP", ""], len(b))
    first = v3.fit(a, frame(20, 100, 14), protocol)
    second = v3.fit(b.sample(frac=1, random_state=3), frame(20, 100, 14), protocol)
    test = frame(12, 200, 27)
    np.testing.assert_array_equal(v3.score(first, test).anomaly, v3.score(second, test).anomaly)
    assert -1 in first["labelled"].fit_label.to_numpy()
    assert set(first["semi"].classes_) == {0, 1}


def test_calibration_fixed_and_no_evaluation_batch_dependence(bundle):
    f = frame(12, 200, 27)
    together = v3.score(bundle, f)
    single = v3.score(bundle, f.iloc[[0]])
    np.testing.assert_allclose(together[v3.METHODS].iloc[0], single[v3.METHODS].iloc[0])
    assert bundle["labelled"].fit_label.eq(-1).sum() > 0


def test_graph_extreme_values_remain_finite_and_flagged(bundle):
    f = frame(12, 200, 27)
    f.loc[0, bundle["transform"].columns] = 1e8
    result = v3.score(bundle, f)
    assert np.isfinite(result[v3.METHODS]).all().all()
    assert result.graph_clipped_features.iloc[0] > 0


def test_missing_feature_and_duplicate_rows_rejected():
    with pytest.raises(ValueError, match="Missing feature"):
        v3.check_frame(frame().drop(columns="best_depth"))
    with pytest.raises(ValueError, match="Duplicate"):
        v3.check_frame(pd.concat([frame(), frame()]))


def test_evaluation_provenance_tampering(tmp_path, bundle):
    path = tmp_path / "evaluation.csv"
    frame(12, 200, 27).to_csv(path, index=False)
    p = bundle["protocol"]
    bundle["excluded_ids"] = [1, 2, 3]
    meta = dict(
        feature_sha256=v3.sha(path),
        source_digest=v3.source_digest(),
        selected_targets=[201, 202],
        preprocessing=p["preprocessing"],
        bls=p["bls"],
        data=dict(**p["evaluation_data"], sectors=p["evaluation_sectors"]),
    )
    v3.write_json(path.with_suffix(".provenance.json"), meta)
    v3.check_evaluation_provenance(path, bundle)
    path.write_text("tampered")
    with pytest.raises(ValueError, match="provenance mismatch"):
        v3.check_evaluation_provenance(path, bundle)


def test_ephemerides_time_system_and_staleness(protocol):
    f = frame(3)
    e = pd.DataFrame(
        dict(
            tic_id=[1, 2, 3],
            catalogue_id=["a", "b", "c"],
            period_days=[2.0] * 3,
            epoch_bjd_tdb=[2459000.0, 2459000.0, 2457000.0],
            period_error_days=[0.0, 0.0, 1.0],
            epoch_error_days=[0.0, 0.0, 0.0],
            reliable=[True] * 3,
        )
    )
    f.loc[1, "time_system"] = "unknown"
    result = v3.candidates(f, protocol, e)
    assert result.signal_match.tolist() == [True, False, False]
    assert result.epoch_testable.tolist() == [True, False, False]
    assert not v3.candidates(f, protocol).signal_match.any()


def test_multiple_planet_catalogue_matching(protocol):
    f = frame(1)
    e = pd.DataFrame(
        dict(
            tic_id=[1, 1],
            catalogue_id=["wrong", "correct"],
            period_days=[3.0, 2.0],
            epoch_bjd_tdb=[2459000.0, 2459000.0],
            period_error_days=[0.0, 0.0],
            epoch_error_days=[0.0, 0.0],
            reliable=[True, True],
        )
    )
    assert v3.candidates(f, protocol, e).matched_catalogue_id.iloc[0] == "correct"


def test_metrics_deduplicate_targets_and_preserve_unlabelled(bundle, protocol):
    f = frame(12, 200, 27)
    more = f.assign(sector=28, n_observations=900)
    scored = v3.candidates(v3.score(bundle, pd.concat([f, more], ignore_index=True)), protocol)
    curves, budgets, comp = v3.reports(scored, protocol)
    assert curves.k.max() == 12
    assert curves.positive_total.unique().tolist() == [4]
    assert curves[curves.k.eq(12)].recovered.eq(4).all()
    assert len(budgets) == 2 * len(v3.METHODS)
    assert comp.recovered.between(0, 4).all()


def test_bootstrap_identical_methods_zero_difference(bundle, protocol):
    scored = v3.candidates(v3.score(bundle, frame(12, 200, 27)), protocol)
    for method in v3.METHODS:
        scored[method] = scored.bls
    result = v3.bootstrap(scored, protocol)
    assert (result[["difference", "low", "high"]] == 0).all().all()


def test_explanations_do_not_mutate_inputs(bundle):
    f = frame(12, 200, 27)
    before = f.copy(deep=True)
    result = v3.explain(bundle, v3.score(bundle, f))
    pd.testing.assert_frame_equal(f, before)
    assert len(result) > 0
    assert result.training_percentile.between(0, 1).all()
    assert (result.delta_min <= result.median_replacement_delta).all()


def test_freeze_and_evaluate_end_to_end(tmp_path, protocol):
    dev = pd.concat([frame(), frame(20, 100, 14)], ignore_index=True)
    b = v3.freeze(dev, protocol, tmp_path / "frozen", excluded=[999])
    v3.verify(tmp_path / "frozen")
    with pytest.raises(ValueError, match="Previously inspected"):
        v3.evaluate(b, frame(12, 0, 27), tmp_path / "bad")
    with pytest.raises(ValueError, match="non-predefined"):
        v3.evaluate(b, frame(12, 200, 14), tmp_path / "bad")
    v3.evaluate(b, frame(12, 200, 27), tmp_path / "evaluation")
    v3.verify(tmp_path / "evaluation")
    assert (tmp_path / "evaluation/recovery_all_sectors.png").exists()
    (tmp_path / "frozen/protocol.json").write_text("{}")
    with pytest.raises(ValueError, match="Changed"):
        v3.verify(tmp_path / "frozen")
