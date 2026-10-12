"""Paired, pre-detrending trapezoid injections into copies of real photometry."""

import argparse
import itertools
import logging
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from .bls import period_match, phase, search_bls
from .config import load_config
from .preprocessing import preprocess
from .research import digest
from .utils import write_json

LOG = logging.getLogger(__name__)


def trapezoid(time, period, epoch, duration, ingress_fraction=0.2):
    if not (0 < duration < period and 0 < ingress_fraction <= 0.5):
        raise ValueError("Invalid injection geometry")
    distance = np.abs(phase(time, period, epoch))
    return np.clip((duration / 2 - distance) / (duration * ingress_fraction), 0, 1)


def inject(raw: dict, period: float, epoch: float, duration: float, depth: float) -> dict:
    if not 0 < depth < 1:
        raise ValueError("Depth must lie in (0, 1)")
    copy = {k: np.array(v, copy=True) for k, v in raw.items()}
    copy["flux"] = copy["flux"] * (1 - depth * trapezoid(copy["time"], period, epoch, duration))
    return copy


def run_injections(cfg: dict, settings: dict, destination: Path):
    if destination.exists():
        raise ValueError("Injection output exists; choose a new directory")
    root = Path(cfg["root"])
    manifest = pd.read_csv(root / "data/raw/manifest.csv").sort_values(["tic_id", "sector"])
    # One raw sector per target, selected before any recovery measurement.
    manifest = manifest.drop_duplicates("tic_id")
    manifest = manifest.sample(
        min(settings["n_targets"], len(manifest)), random_state=settings["seed"]
    )
    destination.mkdir(parents=True)
    manifest.to_csv(destination / "selected_raw_curves.csv", index=False)
    write_json(
        destination / "protocol.json",
        dict(
            config=cfg,
            injection_settings=settings,
            note="Synthetic trapezoids in observed real noise, not astrophysically validated candidates",
        ),
    )
    rows, controls = [], []
    rng = np.random.default_rng(settings["seed"])
    for source in manifest.to_dict("records"):
        path = root / source["raw_path"]
        original_hash = digest(path)
        with np.load(path) as archive:
            raw = dict(archive)
        control_curves = {}
        for method in settings["methods"]:
            try:
                prep = dict(cfg["preprocessing"], detrend_method=method)
                control = preprocess(raw, prep)
                result, _ = search_bls(control, cfg["bls"])
                control_curves[method] = control
                controls.append(
                    dict(
                        tic_id=source["tic_id"],
                        sector=source["sector"],
                        method=method,
                        **result,
                        status="ok",
                    )
                )
            except Exception as exc:
                controls.append(
                    dict(
                        tic_id=source["tic_id"],
                        sector=source["sector"],
                        method=method,
                        status="failed",
                        error=str(exc),
                    )
                )
        grid = itertools.product(
            settings["periods_days"],
            settings["depths"],
            settings["durations_hours"],
            range(settings["phases_per_case"]),
        )
        for period, depth, hours, replicate in grid:
            duration = hours / 24
            epoch = np.nanmin(raw["time"]) + rng.uniform(0, period)
            augmented = inject(raw, period, epoch, duration, depth)
            for method in settings["methods"]:
                row = dict(
                    tic_id=source["tic_id"],
                    sector=source["sector"],
                    method=method,
                    injected_period=period,
                    injected_depth=depth,
                    injected_duration=duration,
                    epoch=epoch,
                    replicate=replicate,
                    original_sha256=original_hash,
                )
                try:
                    curve = preprocess(augmented, dict(cfg["preprocessing"], detrend_method=method))
                    result, _ = search_bls(curve, cfg["bls"])
                    matches = period_match(result["best_period"], period)
                    control = control_curves[method]
                    shared, ii, jj = np.intersect1d(
                        curve["time"], control["time"], return_indices=True
                    )
                    shape = trapezoid(shared, period, epoch, duration)
                    # Paired attenuation against the un-injected processed control.
                    # Ratio removes the existing variability before estimating template amplitude.
                    ratio = curve["flux"][ii] / control["flux"][jj]
                    design = np.column_stack([np.ones(len(shape)), -shape])
                    recovered_amplitude = (
                        np.linalg.lstsq(design, ratio, rcond=None)[0][1]
                        if np.sum(shape > 0) >= 5
                        else np.nan
                    )
                    direct = matches["relative_period_error"] <= settings["period_tolerance"]
                    alias = matches["harmonic_relative_error"] <= settings["period_tolerance"]
                    cap = min(
                        cfg["bls"]["max_period_days"],
                        np.ptp(curve["time"]) / cfg["bls"]["min_transits"],
                    )
                    inside = shape > 0
                    observed_events = len(np.unique(np.rint((shared[inside] - epoch) / period)))
                    row.update(
                        status="ok",
                        recovered_period=result["best_period"],
                        blind_bls_depth=result["best_depth"],
                        depth_snr=result["depth_snr"],
                        direct_period_recovered=bool(direct),
                        harmonic_period_recovered=bool(alias),
                        paired_template_depth=recovered_amplitude,
                        paired_depth_relative_bias=recovered_amplitude / depth - 1,
                        grid_eligible=cfg["bls"]["min_period_days"] <= period <= cap,
                        sampled_injected_events=observed_events,
                        **matches,
                    )
                except Exception as exc:
                    row.update(status="failed", error=str(exc))
                rows.append(row)
        if digest(path) != original_hash:
            raise RuntimeError("Raw data changed during injection validation")
        LOG.info("Completed injections for TIC %s (%s trials so far)", source["tic_id"], len(rows))
        pd.DataFrame(rows).to_csv(destination / "injection_trials.csv", index=False)
        pd.DataFrame(controls).to_csv(destination / "uninjected_controls.csv", index=False)
    trials = pd.DataFrame(rows)
    successes = trials[trials.status.eq("ok")].copy()
    if len(successes):
        summary = (
            successes.groupby(["method", "injected_period", "injected_depth", "injected_duration"])
            .agg(
                successful_trials=("status", "size"),
                direct_recovery=("direct_period_recovered", "mean"),
                harmonic_recovery=("harmonic_period_recovered", "mean"),
                median_paired_depth_bias=("paired_depth_relative_bias", "median"),
            )
            .reset_index()
        )
        summary.to_csv(destination / "injection_summary.csv", index=False)
    (destination / "README.md").write_text(
        "# Real-noise injection validation\n\n"
        f"Attempted {len(trials)} trials; {int(trials.status.eq('failed').sum())} failed. "
        "Failures remain explicit in injection_trials.csv; summary recovery rates condition on successful processing.\n\n"
        "Identical trapezoid signals and phases are added multiplicatively before preprocessing for both detrenders. "
        "Original flux errors and observed noise are retained; photon noise is not re-simulated. "
        "Raw files are never overwritten and their hashes are checked. Uninjected controls may contain real variability "
        "or transits, so their peaks are not automatically false alarms.\n\n"
        "Period recovery uses the blind strongest BLS peak, with direct and harmonic matches separate. "
        "This is period retrieval, not detection at a calibrated false-alarm rate. Paired template-depth bias "
        "compares detrended injected/control flux ratios at the known injected ephemeris. "
        "Grid eligibility and sampled event counts are recorded. Trapezoids approximate transit morphology; "
        "this experiment does not establish real-planet purity or limb-darkened transit completeness.\n",
        encoding="utf-8",
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="config/default.yaml")
    parser.add_argument("--settings", default="config/real_injections.yaml")
    parser.add_argument("--output", type=Path, default=Path("experiments/research_v2/injections"))
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    run_injections(
        load_config(args.config), yaml.safe_load(Path(args.settings).read_text()), args.output
    )


if __name__ == "__main__":
    main()
