"""Explicit interpretable feature families; catalogue quantities never become labels in X."""

import numpy as np
from astropy import constants as const
from scipy.stats import kurtosis, skew

from .bls import phase
from .preprocessing import mad

GENERIC = [
    "mean_flux",
    "median_flux",
    "std_flux",
    "variance",
    "mad",
    "rms",
    "iqr",
    "min_flux",
    "max_flux",
    "peak_to_peak",
    "skewness",
    "kurtosis",
    "point_to_point_scatter",
    "difference_rms",
    "median_absolute_successive_difference",
    "percentile_amplitude",
    "baseline_days",
    "n_observations",
    "n_segments",
    "duty_cycle",
    "largest_gap_days",
]
BLS = [
    "best_period",
    "best_duration",
    "best_depth",
    "depth_error",
    "depth_snr",
    "bls_max_power",
    "bls_median_power",
    "bls_peak_significance",
    "number_expected_transits",
    "number_observed_transits",
    "in_transit_points",
]
PHYSICS = [
    "median_in_transit",
    "median_out_transit",
    "measured_depth",
    "asymmetry_proxy",
    "odd_even_difference",
    "odd_even_significance",
    "secondary_depth_proxy",
    "fraction_in_transit",
    "radius_ratio_proxy",
    "radius_earth_proxy",
    "duration_ratio_proxy",
]
FAMILIES = {"generic": GENERIC, "bls": BLS, "physics": PHYSICS, "all": GENERIC + BLS + PHYSICS}


def median_or_nan(x: np.ndarray, minimum: int = 3) -> float:
    return float(np.median(x)) if len(x) >= minimum else np.nan


def extract_features(curve: dict, transit: dict, metadata: dict) -> dict:
    t, f, seg = curve["time"], curve["flux"], curve["segment"]
    dt = np.diff(t)
    diff = np.diff(f)[np.diff(seg) == 0]
    baseline, cadence = np.ptp(t), np.median(dt)
    p, d, epoch = transit["best_period"], transit["best_duration"], transit["transit_epoch"]
    ph = phase(t, p, epoch)
    inside = np.abs(ph) < d / 2
    outside = np.abs(ph) > d
    events = np.round((t - epoch) / p).astype(int)
    odd, even = f[inside & (events % 2 == 1)], f[inside & (events % 2 == 0)]
    difference = median_or_nan(odd) - median_or_nan(even)
    # Event-level scatter avoids treating correlated in-transit cadences as independent.
    depths = [
        (event, median_or_nan(f[inside & (events == event)])) for event in np.unique(events[inside])
    ]
    odd_events = np.array([v for k, v in depths if k % 2 and np.isfinite(v)])
    even_events = np.array([v for k, v in depths if not k % 2 and np.isfinite(v)])
    uncertainty = (
        np.sqrt(
            np.var(odd_events, ddof=1) / len(odd_events)
            + np.var(even_events, ddof=1) / len(even_events)
        )
        if min(len(odd_events), len(even_events)) >= 2
        else np.nan
    )
    out = median_or_nan(f[outside])
    depth = transit["best_depth"]
    ratio = np.sqrt(depth) if 0 < depth < 1 else np.nan
    radius, mass = metadata.get("stellar_radius", np.nan), metadata.get("stellar_mass", np.nan)
    radius = float(radius) if radius is not None else np.nan
    mass = float(mass) if mass is not None else np.nan
    rp = radius * const.R_sun.value / const.R_earth.value * ratio if radius > 0 else np.nan
    duration_ratio = np.nan
    if radius > 0 and mass > 0:
        a = (const.G.value * mass * const.M_sun.value * (p * 86400) ** 2 / (4 * np.pi**2)) ** (
            1 / 3
        )
        r_over_a = radius * const.R_sun.value / a
        if 0 < r_over_a < 1:
            duration_ratio = d / (p / np.pi * np.arcsin(r_over_a))
    stats = dict(
        mean_flux=np.mean(f),
        median_flux=np.median(f),
        std_flux=np.std(f),
        variance=np.var(f),
        mad=mad(f),
        rms=np.sqrt(np.mean((f - 1) ** 2)),
        iqr=np.percentile(f, 75) - np.percentile(f, 25),
        min_flux=np.min(f),
        max_flux=np.max(f),
        peak_to_peak=np.ptp(f),
        skewness=skew(f) if np.std(f) > 0 else np.nan,
        kurtosis=kurtosis(f) if np.std(f) > 0 else np.nan,
        point_to_point_scatter=mad(diff) / np.sqrt(2),
        difference_rms=np.sqrt(np.mean(diff**2)),
        median_absolute_successive_difference=np.median(np.abs(diff)),
        percentile_amplitude=np.percentile(f, 95) - np.percentile(f, 5),
        baseline_days=baseline,
        n_observations=len(t),
        n_segments=len(np.unique(seg)),
        duty_cycle=min(1, len(t) * cadence / (baseline + cadence)),
        largest_gap_days=np.max(dt),
        median_in_transit=median_or_nan(f[inside]),
        median_out_transit=out,
        measured_depth=out - median_or_nan(f[inside]),
        asymmetry_proxy=median_or_nan(f[inside & (ph < 0)]) - median_or_nan(f[inside & (ph >= 0)]),
        odd_even_difference=difference,
        odd_even_significance=abs(difference) / uncertainty if uncertainty > 0 else np.nan,
        secondary_depth_proxy=out - median_or_nan(f[np.abs(np.abs(ph) - p / 2) < d / 2]),
        fraction_in_transit=np.mean(inside),
        radius_ratio_proxy=ratio,
        radius_earth_proxy=rp,
        duration_ratio_proxy=duration_ratio,
    )
    return {
        **metadata,
        **transit,
        **{k: float(v) if np.isfinite(v) else np.nan for k, v in stats.items()},
    }
