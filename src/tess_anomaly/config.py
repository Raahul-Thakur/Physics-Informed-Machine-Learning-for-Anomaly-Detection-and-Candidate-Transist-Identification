"""YAML configuration and experiment paths."""

import hashlib
import json
from pathlib import Path

import yaml


def load_config(path: str | Path) -> dict:
    """Resolve paths relative to the repository, independent of current directory."""
    path = Path(path).resolve()
    config = yaml.safe_load(path.read_text(encoding="utf-8"))
    config["root"] = str((path.parent.parent / config.get("workspace", ".")).resolve())
    if config["bls"]["min_period_days"] <= 0:
        raise ValueError("Minimum period must be positive")
    if config["models"]["scaler"] not in {"robust", "standard"}:
        raise ValueError("models.scaler must be robust or standard")
    if config["preprocessing"]["window_days"] <= 0 or config["preprocessing"]["gap_days"] <= 0:
        raise ValueError("Detrending window and gap threshold must be positive")
    if not 0 <= config["models"]["max_missing_fraction"] < 1:
        raise ValueError("max_missing_fraction must be in [0,1)")
    if config["bls"]["frequency_factor"] <= 0 or config["bls"]["oversample"] < 1:
        raise ValueError("BLS frequency factor and oversampling must be positive")
    if config["bls"]["objective"] not in {"snr", "likelihood"}:
        raise ValueError("BLS objective must be snr or likelihood")
    return config


def fingerprint(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode()).hexdigest()[:16]


def prepare(config: dict) -> Path:
    root = Path(config["root"])
    for directory in (
        "data/raw",
        "data/processed",
        "data/catalog",
        "data/features",
        "data/cache",
        "outputs/figures/candidates",
        "outputs/tables",
        "outputs/models",
        "outputs/rankings",
        "outputs/logs",
    ):
        (root / directory).mkdir(parents=True, exist_ok=True)
    return root
