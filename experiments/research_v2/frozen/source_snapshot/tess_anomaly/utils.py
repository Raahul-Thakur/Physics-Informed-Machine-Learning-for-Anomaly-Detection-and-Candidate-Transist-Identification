"""Atomic artifacts, provenance, and explicitly synthetic validation inputs."""

import importlib.metadata
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from .bls import phase


def write_json(path: Path, value: object) -> None:
    def clean(obj):
        if isinstance(obj, dict):
            return {str(k): clean(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple, np.ndarray)):
            return [clean(v) for v in obj]
        if isinstance(obj, (float, np.floating)):
            return float(obj) if np.isfinite(obj) else None
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.bool_):
            return bool(obj)
        return obj

    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(clean(value), indent=2, default=str), encoding="utf-8")
    temp.replace(path)


def provenance(root: Path, cfg: dict, ids: list, status: str) -> None:
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, stderr=subprocess.DEVNULL, text=True
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        commit = None
    packages = {dist.metadata["Name"]: dist.version for dist in importlib.metadata.distributions()}
    write_json(
        root / "outputs/run_metadata.json",
        dict(
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            config=cfg,
            package_versions=packages,
            git_commit=commit,
            sample_ids=ids,
            status=status,
            analysis_mode="Descriptive transductive ranking; not held-out predictive validation",
        ),
    )


def synthetic_curve(
    seed: int = 42,
    period: float = 3.2,
    depth: float = 0.008,
    duration: float = 0.12,
    noise: float = 0.001,
) -> tuple[dict, dict]:
    """Box injection for validation only; never used as a data-access fallback."""
    rng = np.random.default_rng(seed)
    t = np.arange(0, 26, 0.01)
    t = t[(t < 12) | (t > 13)]
    y = 1 + 0.002 * np.sin(2 * np.pi * t / 9) + rng.normal(0, noise, len(t))
    y[np.abs(phase(t, period, 0.8)) < duration / 2] -= depth
    return dict(
        time=t, flux=y, flux_err=np.full(len(t), noise), quality=np.zeros(len(t), dtype=int)
    ), dict(
        period=period,
        depth=depth,
        duration=duration,
        noise=noise,
        epoch=0.8,
        seed=seed,
        data_kind="synthetic_validation_only",
    )
