"""Content-validated stage receipts for inexpensive, safe --resume runs."""

import csv
import hashlib
import json
from pathlib import Path

from .config import fingerprint
from .utils import write_json

INPUTS = {
    "download": ["data/catalog/toi_snapshot.csv", "data/catalog/tesscurl_sector_*_lc.sh"],
    "preprocess": ["data/raw/manifest.csv", "data/raw/*.npz"],
    "bls": ["data/raw/manifest.csv", "data/raw/*.npz"],
    "features": ["data/raw/manifest.csv", "data/raw/*.npz"],
    "train": ["data/features/features.csv"],
    "evaluate": [
        "outputs/rankings/ranked_light_curves.csv",
        "data/catalog/normalized_catalog.csv",
        "data/features/features.csv",
    ],
    "figures": [
        "outputs/rankings/ranked_light_curves.csv",
        "outputs/models/preprocessing.joblib",
        "outputs/tables/model_performance.csv",
        "outputs/tables/top_candidates.csv",
    ],
    "report": [
        "outputs/config_used.yaml",
        "outputs/rankings/ranked_light_curves.csv",
        "data/catalog/sample.csv",
        "outputs/tables/*.csv",
    ],
}
OUTPUTS = {
    "download": [
        "data/catalog/sample.csv",
        "data/catalog/normalized_catalog.csv",
        "data/raw/manifest.csv",
        "data/raw/*.npz",
        "outputs/logs/download_failures.csv",
    ],
    "preprocess": ["data/processed/*.npz", "outputs/logs/preprocess_failures.csv"],
    "bls": ["data/cache/*_bls.json", "data/cache/*_power.npz", "outputs/logs/bls_failures.csv"],
    "features": ["data/features/features.csv", "outputs/logs/features_failures.csv"],
    "train": [
        "outputs/rankings/*.csv",
        "outputs/models/*",
        "outputs/tables/missing_data.csv",
        "outputs/tables/summary_statistics.csv",
    ],
    "evaluate": [
        f"outputs/tables/{name}.csv"
        for name in [
            "model_performance",
            "group_statistics",
            "correlations",
            "feature_score_correlations",
            "top_candidates",
            "period_sanity",
            "ablation_results",
        ]
    ],
    "figures": [
        "outputs/figures/*.png",
        "outputs/figures/*.pdf",
        "outputs/figures/candidates/*",
        "outputs/tables/pca_loadings.csv",
        "outputs/tables/pca_coordinates.csv",
    ],
    "report": [
        "outputs/research_summary.md",
        "outputs/abstract_results.txt",
        "outputs/tables/sector_coverage.csv",
    ],
}


def checksums(root: Path, patterns: list[str]) -> dict:
    return {
        str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
        for pattern in patterns
        for p in sorted(root.glob(pattern))
        if p.is_file() and not p.name.startswith("stage_")
    }


def signature(root: Path, cfg: dict, stage: str, source_hash: str) -> str:
    files = checksums(root, INPUTS.get(stage, []))
    for key in ["catalog_csv", "background_csv", "exclude_tics_csv"]:
        if cfg["data"].get(key):
            p = root / cfg["data"][key]
            files[str(p)] = hashlib.sha256(p.read_bytes()).hexdigest()
    return fingerprint([cfg, stage, source_hash, files])


def valid(root: Path, cfg: dict, stage: str, source_hash: str) -> bool:
    receipt = root / f"data/cache/stage_{stage}.json"
    if not receipt.exists() or stage not in OUTPUTS:
        return False
    failure_file = root / f"outputs/logs/{stage}_failures.csv"
    if failure_file.exists():
        with failure_file.open(newline="", encoding="utf-8") as handle:
            if next(csv.DictReader(handle), None) is not None:
                return False  # Retry failed targets instead of freezing a partial download.
    try:
        saved = json.loads(receipt.read_text())
        outputs = saved["outputs"]
        return (
            saved["signature"] == signature(root, cfg, stage, source_hash)
            and bool(outputs)
            and all(
                (root / p).exists()
                and hashlib.sha256((root / p).read_bytes()).hexdigest() == digest
                for p, digest in outputs.items()
            )
        )
    except (ValueError, KeyError, OSError):
        return False


def record(root: Path, cfg: dict, stage: str, source_hash: str) -> None:
    if stage in OUTPUTS:
        write_json(
            root / f"data/cache/stage_{stage}.json",
            {
                "signature": signature(root, cfg, stage, source_hash),
                "outputs": checksums(root, OUTPUTS[stage]),
            },
        )
