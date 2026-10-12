import numpy as np
import pytest

from tess_anomaly.bls import period_match, search_bls
from tess_anomaly.preprocessing import preprocess
from tess_anomaly.utils import synthetic_curve

PRE = dict(
    quality_bitmask=175,
    detrend_method="savgol",
    window_days=1.5,
    preserve_transits=True,
    gap_days=0.25,
    min_points=100,
)
BLS = dict(
    min_period_days=0.5,
    max_period_days=12,
    durations_hours=[1, 2, 3, 4],
    frequency_factor=5,
    objective="snr",
    oversample=10,
    min_transits=2,
)


def test_injection_recovery():
    raw, truth = synthetic_curve()
    summary, power = search_bls(preprocess(raw, PRE), BLS)
    assert abs(summary["best_period"] / truth["period"] - 1) < 0.005
    assert summary["best_depth"] == pytest.approx(truth["depth"], rel=0.2)
    assert summary["number_observed_transits"] >= 7
    assert summary["depth_snr"] > 20
    assert np.isfinite(power["power"]).all()


def test_harmonic_match_and_invalid_grid():
    assert period_match(6.4, 3.2)["harmonic_factor"] == 2
    assert period_match(6.4, 3.2)["harmonic_relative_error"] == 0
    raw, _ = synthetic_curve()
    with pytest.raises(ValueError):
        search_bls(preprocess(raw, PRE), dict(BLS, min_period_days=20))


@pytest.mark.parametrize("maximum", [12, 30])
def test_period_grid_excludes_automatic_overshoot(monkeypatch, maximum):
    from astropy.timeseries import BoxLeastSquares

    raw, _ = synthetic_curve()
    curve = preprocess(raw, PRE)
    cap = min(maximum, np.ptp(curve["time"]) / 2)
    monkeypatch.setattr(
        BoxLeastSquares,
        "autoperiod",
        lambda *args, **kwargs: np.array([0.49, 0.5, 3.2, cap, cap + 0.02]),
    )
    original = BoxLeastSquares.power

    def checked_power(self, periods, *args, **kwargs):
        assert np.all((np.asarray(periods) >= 0.5) & (np.asarray(periods) <= cap))
        return original(self, periods, *args, **kwargs)

    monkeypatch.setattr(BoxLeastSquares, "power", checked_power)
    summary, grid = search_bls(curve, dict(BLS, max_period_days=maximum))
    assert summary["best_period"] <= cap
    assert np.array_equal(grid["period"], [0.5, 3.2, cap])
