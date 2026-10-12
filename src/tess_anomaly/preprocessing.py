"""Quality filtering and transit-preserving, segment-local detrending."""

import numpy as np
import pandas as pd
from scipy.signal import savgol_filter


def mad(x: np.ndarray) -> float:
    """Gaussian-consistent median absolute deviation."""
    if len(x) == 0:
        return np.nan
    return float(1.4826 * np.median(np.abs(x - np.median(x))))


def preprocess(raw: dict, cfg: dict) -> dict:
    """Never delete negative outliers. Mask dips only while estimating the trend.

    Uncertainties entirely absent imply unweighted BLS; partially invalid errors
    are filtered. All operations maintain cadence alignment.
    """
    t, f = np.asarray(raw["time"], float), np.asarray(raw["flux"], float)
    e = np.asarray(raw.get("flux_err", np.full(len(t), np.nan)), float)
    q = np.asarray(raw.get("quality", np.zeros(len(t))), np.int64)
    if not (t.shape == f.shape == e.shape == q.shape):
        raise ValueError("Cadence arrays must have identical shapes")
    mask = np.isfinite(t) & np.isfinite(f) & (f > 0)
    errors_absent = np.all(np.isnan(e))
    if not errors_absent:
        mask &= np.isfinite(e) & (e > 0)
    bitmask = int(cfg.get("quality_bitmask", 175))
    mask &= (q & bitmask) == 0
    if np.any(mask):
        scale = np.median(f[mask])
        mask &= f / scale <= cfg.get("max_normalized_flux", 1e6)
    t, f, e, q = t[mask], f[mask], e[mask], q[mask]
    if len(t) < cfg.get("min_points", 200):
        raise ValueError("Insufficient valid cadences")
    order = np.argsort(t)
    t, f, e, q = t[order], f[order], e[order], q[order]
    unique = np.r_[True, np.diff(t) > 0]
    t, f, e, q = t[unique], f[unique], e[unique], q[unique]
    if len(t) < cfg.get("min_points", 200):
        raise ValueError("Insufficient valid cadences")
    norm = np.median(f)
    y, err = f / norm, e / norm
    segment = np.cumsum(np.r_[False, np.diff(t) > cfg["gap_days"]])
    trend = np.empty(len(t))
    for seg in np.unique(segment):
        indices = np.flatnonzero(segment == seg)
        ts, ys = t[indices], y[indices]
        if len(ts) < 5 or cfg["detrend_method"] == "median":
            fitted = np.full(len(ts), np.median(ys))
        else:
            cadence = np.median(np.diff(ts))
            window = max(5, int(cfg["window_days"] / cadence) | 1)
            window = min(window, len(ts) if len(ts) % 2 else len(ts) - 1)
            work = ys.copy()
            for _ in range(3 if cfg.get("preserve_transits", True) else 1):
                if cfg["detrend_method"] == "savgol":
                    fitted = savgol_filter(work, window, 2)
                elif cfg["detrend_method"] == "rolling_median":
                    fitted = (
                        pd.Series(work)
                        .rolling(window, center=True, min_periods=1)
                        .median()
                        .to_numpy()
                    )
                else:
                    raise ValueError("detrend_method must be median, savgol or rolling_median")
                residual = ys - fitted
                scale = mad(residual)
                keep = np.abs(residual) <= 3 * scale if scale > 0 else np.ones(len(ys), bool)
                if keep.sum() >= 3:
                    work = np.interp(ts, ts[keep], ys[keep])
            # Interpolation is exclusively within a segment and only for trend fitting.
        trend[indices] = fitted
    if np.any(~np.isfinite(trend) | (trend <= 0)):
        raise ValueError("Invalid detrending baseline")
    return dict(
        time=t,
        raw_flux=f,
        normalized_flux=y,
        trend=trend,
        flux=y / trend,
        flux_err=err / trend,
        quality=q,
        segment=segment,
        n_removed=np.array(len(mask) - len(t)),
    )
