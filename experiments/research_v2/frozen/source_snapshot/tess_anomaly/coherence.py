"""Photometric coherence proxies; none are classifications or calibrated significances."""

import numpy as np

from .bls import phase
from .features import median_or_nan
from .preprocessing import mad

COHERENCE = [
    "event_depth_relative_mad",
    "event_duration_relative_mad",
    "single_event_power_fraction_proxy",
    "local_noise_beta",
    "edge_to_centre_depth_ratio",
    "ingress_egress_difference",
    "secondary_scan_depth",
    "secondary_scan_depth_ratio",
]
COMPACT = [
    "best_period",
    "best_duration",
    "best_depth",
    "depth_snr",
    "number_observed_transits",
    "odd_even_difference",
    "asymmetry_proxy",
    "point_to_point_scatter",
    *COHERENCE,
]


def coherence_features(curve: dict, transit: dict) -> dict:
    t, f = curve["time"], curve["flux"]
    p, d, epoch = (transit[k] for k in ["best_period", "best_duration", "transit_epoch"])
    ph = phase(t, p, epoch)
    event = np.rint((t - epoch) / p).astype(int)
    cadence = np.median(np.diff(t))
    depths, widths, powers = [], [], []
    for number in np.unique(event[np.abs(ph) < d / 2]):
        inside = (event == number) & (np.abs(ph) < d / 2)
        outside = (event == number) & (np.abs(ph) > d) & (np.abs(ph) < 2 * d)
        if inside.sum() < 3 or outside.sum() < 5:
            continue
        level = np.median(f[outside])
        depth = level - np.median(f[inside])
        depths.append(depth)
        noise = mad(f[outside])
        powers.append(max(depth, 0) ** 2 * inside.sum() / noise**2 if noise > 0 else np.nan)
        # Sampled half-depth width; not a fitted physical transit duration.
        below = (event == number) & (np.abs(ph) < d) & (f < level - depth / 2)
        if depth > 0 and below.sum() >= 3:
            widths.append(np.ptp(t[below]) + cadence)
    local = (np.abs(ph) > d) & (np.abs(ph) < 2 * d)
    block_means, block_counts = [], []
    # Segment-local bins do not bridge photometric gaps.
    for segment in np.unique(curve["segment"]):
        ids = np.flatnonzero(local & (curve["segment"] == segment))
        if not len(ids):
            continue
        bins = np.floor((t[ids] - t[ids[0]]) / (d / 2)).astype(int)
        for b in np.unique(bins):
            values = f[ids[bins == b]]
            if len(values) >= 3:
                block_means.append(np.mean(values))
                block_counts.append(len(values))
    noise = np.std(f[local]) if local.sum() >= 5 else np.nan
    beta = (
        np.std(block_means, ddof=1) / (noise * np.sqrt(np.mean(1 / np.array(block_counts))))
        if len(block_means) >= 4 and noise > 0
        else np.nan
    )
    level = median_or_nan(f[np.abs(ph) > d])
    centre = level - median_or_nan(f[np.abs(ph) < d / 6])
    edges = level - median_or_nan(f[(np.abs(ph) > d / 3) & (np.abs(ph) < d / 2)])
    ingress = median_or_nan(f[(ph > -d / 2) & (ph < -d / 3)])
    egress = median_or_nan(f[(ph < d / 2) & (ph > d / 3)])
    secondary = []
    for centre_phase in np.linspace(-p / 2, p / 2, 80, endpoint=False):
        if abs(centre_phase) <= 2 * d:
            continue
        selection = np.abs(phase(ph, p, centre_phase)) < d / 2
        if selection.sum() >= 5:
            secondary.append(level - np.median(f[selection]))
    secondary_depth = max(secondary) if secondary else np.nan
    depth_scale = abs(np.median(depths)) if depths else np.nan
    total = np.sum(powers)
    return dict(
        event_depth_relative_mad=mad(np.array(depths)) / depth_scale
        if len(depths) >= 3 and depth_scale > 0
        else np.nan,
        event_duration_relative_mad=mad(np.array(widths)) / np.median(widths)
        if len(widths) >= 3
        else np.nan,
        single_event_power_fraction_proxy=max(powers) / total
        if len(powers) >= 2 and total > 0
        else np.nan,
        local_noise_beta=beta,
        edge_to_centre_depth_ratio=edges / centre if centre > 0 else np.nan,
        ingress_egress_difference=ingress - egress,
        secondary_scan_depth=secondary_depth,
        secondary_scan_depth_ratio=secondary_depth / transit["best_depth"]
        if transit["best_depth"] > 0
        else np.nan,
    )
