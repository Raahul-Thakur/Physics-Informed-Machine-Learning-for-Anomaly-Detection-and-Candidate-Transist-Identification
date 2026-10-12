"""Astropy BLS with duration-based frequency sampling and harmonic diagnostics."""

import numpy as np
from astropy.timeseries import BoxLeastSquares
from scipy.signal import find_peaks

from .preprocessing import mad


def phase(time: np.ndarray, period: float, epoch: float) -> np.ndarray:
    """Signed time from the nearest transit centre, in days."""
    return (time - epoch + period / 2) % period - period / 2


def search_bls(curve: dict, cfg: dict) -> tuple[dict, dict]:
    t, y, e = curve["time"], curve["flux"], curve["flux_err"]
    baseline = np.ptp(t)
    maximum = min(cfg["max_period_days"], baseline / cfg.get("min_transits", 2))
    minimum = cfg["min_period_days"]
    durations = np.asarray(cfg["durations_hours"], float) / 24
    durations = durations[(durations > 0) & (durations < minimum)]
    if maximum <= minimum or len(durations) == 0:
        raise ValueError("Baseline/period/duration grid cannot support a BLS search")
    dy = e if np.all(np.isfinite(e) & (e > 0)) else None
    model = BoxLeastSquares(t, y, dy)
    periods = model.autoperiod(
        durations,
        minimum_period=minimum,
        maximum_period=maximum,
        frequency_factor=cfg["frequency_factor"],
    )
    # The automatic frequency grid can overshoot its requested endpoint.
    periods = periods[(periods >= minimum) & (periods <= maximum)]
    if not len(periods):
        raise ValueError("No BLS trials within the requested period bounds")
    result = model.power(
        periods,
        durations,
        objective=cfg["objective"],
        oversample=cfg["oversample"],
    )
    i = int(np.nanargmax(result.power))
    period, duration, epoch = (
        float(result.period[i]),
        float(result.duration[i]),
        float(result.transit_time[i]),
    )
    power = np.asarray(result.power)
    spread = mad(power)
    peaks, _ = find_peaks(power)
    independent = peaks[np.abs(result.period[peaks] - period) > period * duration / baseline * 3]
    second = int(independent[np.argmax(power[independent])]) if len(independent) else None
    inside = np.abs(phase(t, period, epoch)) < duration / 2
    events = np.round((t[inside] - epoch) / period).astype(int)
    expected = max(
        0, int(np.floor((t[-1] - epoch) / period) - np.ceil((t[0] - epoch) / period) + 1)
    )
    summary = dict(
        search_min_period=minimum,
        search_max_period=maximum,
        best_period=period,
        best_duration=duration,
        transit_epoch=epoch,
        best_depth=float(result.depth[i]),
        depth_error=float(result.depth_err[i]),
        depth_snr=float(result.depth_snr[i]),
        bls_max_power=float(power[i]),
        bls_median_power=float(np.median(power)),
        bls_peak_significance=float((power[i] - np.median(power)) / spread)
        if spread > 0
        else np.nan,
        second_peak_period=float(result.period[second]) if second is not None else np.nan,
        number_expected_transits=expected,
        number_observed_transits=len(np.unique(events)),
        in_transit_points=int(inside.sum()),
        weighted_bls=dy is not None,
    )
    for factor, name in [(0.5, "half"), (2, "double")]:
        p = period * factor
        summary[f"harmonic_{name}_power"] = (
            float(
                model.power(
                    [p],
                    durations[durations < p],
                    objective=cfg["objective"],
                    oversample=cfg["oversample"],
                ).power[0]
            )
            if minimum <= p <= maximum
            else np.nan
        )
    return summary, dict(
        period=np.asarray(result.period), power=power, phase_days=phase(t, period, epoch)
    )


def period_match(recovered: float, catalogue: float) -> dict:
    if not np.isfinite(catalogue) or catalogue <= 0:
        return dict(
            relative_period_error=np.nan, harmonic_relative_error=np.nan, harmonic_factor=np.nan
        )
    factors = np.array([0.5, 1, 2])
    errors = np.abs(recovered - factors * catalogue) / (factors * catalogue)
    best = int(np.argmin(errors))
    return dict(
        relative_period_error=abs(recovered - catalogue) / catalogue,
        harmonic_relative_error=errors[best],
        harmonic_factor=factors[best],
    )
