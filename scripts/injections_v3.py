"""Expanded injections in development curves, sampled across measured noise strata."""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from tess_anomaly.config import load_config
from tess_anomaly.real_injections import run_injections


def select_curves(root, n, seed):
    if n < 3:
        raise ValueError("At least three targets required for three noise strata")
    manifest = pd.read_csv(root / "data/raw/manifest.csv").sort_values(["tic_id", "sector"])
    manifest = manifest.drop_duplicates("tic_id").copy()
    noise, failures = [], []
    for row in manifest.itertuples():
        try:
            with np.load(root / row.raw_path) as raw:
                f = raw["flux"].astype(float)
                f = f[np.isfinite(f) & (f > 0)]
                if len(f) < 20:
                    raise ValueError("Too few finite positive raw observations")
                f = f / np.median(f)
                noise.append((int(row.tic_id), float(np.median(abs(np.diff(f))))))
        except (ValueError, OSError, KeyError) as exc:
            failures.append(dict(tic_id=row.tic_id, error=str(exc)))
    valid = manifest.merge(pd.DataFrame(noise, columns=["tic_id", "noise_proxy"]), on="tic_id")
    if len(valid) < n:
        raise ValueError(f"Requested {n} distinct targets; only {len(valid)} usable")
    valid["noise_stratum"] = pd.qcut(
        valid.noise_proxy.rank(method="first"), 3, labels=["low", "medium", "high"]
    )
    selected = []
    for i, (_, group) in enumerate(valid.groupby("noise_stratum", observed=True)):
        count = n // 3 + int(i < n % 3)
        selected.append(group.sample(n=count, random_state=seed + i))
    return pd.concat(selected).sort_values("tic_id"), pd.DataFrame(failures)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("config/default.yaml"))
    parser.add_argument("--settings", type=Path, default=Path("config/injections_v3.yaml"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    cfg = load_config(args.config)
    settings = yaml.safe_load(args.settings.read_text())
    root = Path(cfg["root"])
    allowed = {"experiments/default", "experiments/independent_v2"}
    repository = Path(__file__).resolve().parents[1]
    if root.relative_to(repository).as_posix() not in allowed:
        raise ValueError("V3 preprocessing selection must use inspected development workspaces")
    if args.output.exists():
        raise ValueError("Refusing to overwrite injection experiment")
    selected, failures = select_curves(root, settings["n_targets"], settings["seed"])
    args.output.mkdir(parents=True)
    selected.to_csv(args.output / "noise_stratified_selection.csv", index=False)
    failures.to_csv(args.output / "selection_failures.csv", index=False)
    staging = args.output / "inputs"
    (staging / "data/raw").mkdir(parents=True)
    selected["raw_path"] = selected.raw_path.map(lambda p: str((root / p).resolve()))
    selected.to_csv(staging / "data/raw/manifest.csv", index=False)
    cfg["root"] = str(staging.resolve())
    run_injections(cfg, settings, args.output / "results")
    trials = pd.read_csv(args.output / "results/injection_trials.csv")
    trials = trials.merge(
        selected[["tic_id", "noise_stratum"]], on="tic_id", validate="many_to_one"
    )
    trials["retrieved"] = (
        trials.get("direct_period_recovered", pd.Series(False, index=trials.index))
        .fillna(False)
        .astype(bool)
    )
    if "paired_depth_relative_bias" not in trials:
        trials["paired_depth_relative_bias"] = np.nan
    trials["processed"] = trials.status.eq("ok")
    trials.groupby(["method", "noise_stratum"], observed=True).agg(
        attempted=("status", "size"),
        completed=("processed", "sum"),
        recovered=("retrieved", "sum"),
        recovery_including_failures=("retrieved", "mean"),
        median_depth_bias=("paired_depth_relative_bias", "median"),
    ).to_csv(args.output / "noise_stratified_recovery.csv")


if __name__ == "__main__":
    main()
