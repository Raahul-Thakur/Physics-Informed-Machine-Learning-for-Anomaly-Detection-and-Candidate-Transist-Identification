"""Finite-sample calibration and prospective cohort safeguards."""

import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location(
    "abstract_evidence", ROOT / "scripts/abstract_evidence.py"
)
evidence = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evidence)


def test_rank_correction_ties_and_extremes():
    np.testing.assert_allclose(evidence.conformal_pvalues([1, 2, 2, 3], [0, 2, 4]), [1, 0.8, 0.2])
    with pytest.raises(ValueError):
        evidence.conformal_pvalues([], [1])
    with pytest.raises(ValueError):
        evidence.conformal_pvalues([1, np.nan], [1])


def test_holm_preserves_input_order_and_family():
    np.testing.assert_allclose(evidence.holm([0.04, 0.001, 0.03, 1]), [0.09, 0.004, 0.09, 1])
    with pytest.raises(ValueError):
        evidence.holm([-0.1])


def test_exact_exchangeable_ranks_are_super_uniform():
    # Exhaust every possible held-out rank from a fixed exchangeable set.
    values = np.arange(100.0)
    p = np.array(
        [evidence.conformal_pvalues(np.delete(values, i), values[i : i + 1])[0] for i in range(100)]
    )
    for alpha in [0.01, 0.025, 0.05, 0.1]:
        assert np.mean(p <= alpha) <= alpha


def test_cohort_is_order_independent_unlabelled_and_disjoint(tmp_path):
    sample = pd.DataFrame({"tic_id": range(1, 61), "label": ["background"] * 50 + ["planet"] * 10})
    bundle = {"excluded_ids": [100]}
    evidence.lock_cohort(sample, bundle, tmp_path / "a")
    evidence.lock_cohort(sample.sample(frac=1, random_state=9), bundle, tmp_path / "b")
    a = pd.read_csv(tmp_path / "a/roles.csv")
    pd.testing.assert_frame_equal(a, pd.read_csv(tmp_path / "b/roles.csv"))
    assert a.role.eq("test").sum() == 20
    assert a.tic_id.max() == 50
    with pytest.raises(ValueError, match="Previously inspected"):
        evidence.lock_cohort(sample, {"excluded_ids": [1]}, tmp_path / "c")
    with pytest.raises(ValueError, match="already exists"):
        evidence.lock_cohort(sample, bundle, tmp_path / "a")


def test_missing_tests_remain_in_corrected_family(tmp_path, monkeypatch):
    sample = pd.DataFrame({"tic_id": range(1, 501), "label": "background"})
    bundle = {
        "excluded_ids": [],
        "protocol": {"evaluation_sectors": [27]},
        "transform": SimpleNamespace(transform=lambda f: f[["statistic"]].to_numpy()),
        "forest": SimpleNamespace(score_samples=lambda x: -x[:, 0]),
    }
    evidence.lock_cohort(sample, bundle, tmp_path / "cohort")
    roles = pd.read_csv(tmp_path / "cohort/roles.csv")
    missing = roles.loc[roles.role.eq("test"), "tic_id"].iloc[0]
    frame = sample[sample.tic_id.ne(missing)].copy()
    frame["sector"] = 27
    frame["n_observations"] = 1000
    frame["baseline_days"] = 25
    frame["statistic"] = frame.tic_id / 500
    monkeypatch.setattr(evidence.v3, "check_frame", lambda f: None)
    evidence.significance(frame, bundle, tmp_path / "cohort", tmp_path / "result")
    tests = pd.read_csv(tmp_path / "result/target_tests.csv")
    assert len(tests) == 20
    row = tests.set_index("tic_id").loc[missing]
    assert row.p_value == 1 and not row.reject_reference_null
    summary = json.loads((tmp_path / "result/summary.json").read_text())
    assert summary["reference_scored"] == 480
    assert summary["test_scored"] == 19


def test_interventions_change_one_parameter_only():
    settings = dict(
        base_period=3.2,
        base_depth=0.003,
        base_duration_hours=1.5,
        periods_days=[1.2, 3.2, 8],
        depths=[0.001, 0.003, 0.01],
        durations_hours=[1.5, 3],
    )
    cases = evidence.intervention_cases(settings)
    assert len(cases) == 6
    base = cases[0][1]
    for parameter, case in cases[1:]:
        assert [key for key in base if base[key] != case[key]] == [parameter]
