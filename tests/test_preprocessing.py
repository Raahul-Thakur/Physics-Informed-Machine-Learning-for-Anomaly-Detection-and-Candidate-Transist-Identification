import numpy as np
import pytest

from tess_anomaly.preprocessing import preprocess
from tess_anomaly.utils import synthetic_curve

CFG = dict(
    quality_bitmask=175,
    detrend_method="savgol",
    window_days=1.5,
    preserve_transits=True,
    gap_days=0.25,
    min_points=100,
)


def test_filter_alignment_gaps_and_transit_retention():
    raw, _ = synthetic_curve()
    raw["flux"][0] = np.nan
    raw["flux_err"][1] = -1
    raw["quality"][2] = 1
    raw["time"][3] = np.inf
    out = preprocess(raw, CFG)
    assert len(out["time"]) == len(raw["time"]) - 4
    assert len(out["flux"]) == len(out["quality"]) == len(out["flux_err"])
    assert np.isfinite(out["flux"]).all()
    assert len(np.unique(out["segment"])) == 2
    assert out["flux"].min() < 0.994


def test_missing_errors_supported_and_duplicate_times_removed():
    raw, _ = synthetic_curve()
    raw["flux_err"][:] = np.nan
    raw["time"][1] = raw["time"][0]
    out = preprocess(raw, CFG)
    assert np.all(np.diff(out["time"]) > 0)
    assert np.isnan(out["flux_err"]).all()


def test_all_invalid_measured_errors_do_not_become_unweighted_data():
    raw, _ = synthetic_curve()
    raw["flux_err"][:] = -1
    with pytest.raises(ValueError, match="Insufficient"):
        preprocess(raw, CFG)


@pytest.mark.parametrize("method", ["median", "rolling_median", "savgol"])
def test_detrending_methods(method):
    raw, _ = synthetic_curve()
    out = preprocess(raw, dict(CFG, detrend_method=method))
    assert np.isfinite(out["trend"]).all()
    assert np.median(out["flux"]) == pytest.approx(1, abs=0.005)
