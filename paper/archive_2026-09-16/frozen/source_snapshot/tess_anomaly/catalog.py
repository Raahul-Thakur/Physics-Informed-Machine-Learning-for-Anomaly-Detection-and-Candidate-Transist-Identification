"""Authoritative catalogue snapshots and explicitly labelled reference populations."""

import logging
import re
from io import StringIO
from pathlib import Path

import pandas as pd
import requests

LOG = logging.getLogger(__name__)
TAP = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
EXOFOP = "https://exofop.ipac.caltech.edu/tess/download_toi.php?sort=toi&output=csv"


def sector_target_pool(root: Path, cfg: dict, force: bool = False) -> pd.DataFrame:
    """Parse filenames in official MAST manifests as data; never execute scripts."""
    frames = []
    for sector in cfg.get("sectors") or [1]:
        path = root / f"data/catalog/tesscurl_sector_{sector}_lc.sh"
        url = f"https://archive.stsci.edu/missions/tess/download_scripts/sector/tesscurl_sector_{sector}_lc.sh"
        if force or not path.exists():
            response = requests.get(url, timeout=cfg["timeout_seconds"])
            response.raise_for_status()
            path.write_text(response.text, encoding="utf-8")
        ids = sorted(
            {int(tic) for tic in re.findall(r"-s\d{4}-(\d{16})-\d+-s_lc\.fits", path.read_text())}
        )
        if not ids:
            raise ValueError(f"No TESS light-curve filenames parsed from {url}")
        frames.append(pd.DataFrame({"tic_id": ids, "available_sector": sector}))
    return pd.concat(frames, ignore_index=True).drop_duplicates("tic_id")


def fetch_csv(url: str, path: Path, timeout: int, params: dict | None = None) -> pd.DataFrame:
    response = requests.get(url, params=params, timeout=timeout)
    response.raise_for_status()
    table = pd.read_csv(StringIO(response.text))
    if table.empty or len(table.columns) < 2:
        raise ValueError(f"Empty or invalid CSV from {url}")
    table.to_csv(path, index=False)
    return table


def toi_catalog(root: Path, cfg: dict, force: bool = False) -> pd.DataFrame:
    """Keep all planet rows; resolve target labels conservatively during sampling."""
    local = cfg.get("catalog_csv")
    path = root / "data/catalog/toi_snapshot.csv"
    if local:
        table = pd.read_csv(root / local)
    elif path.exists() and not force:
        table = pd.read_csv(path)
    else:
        try:
            table = fetch_csv(
                TAP, path, cfg["timeout_seconds"], {"query": "select * from toi", "format": "csv"}
            )
            table["catalog_source"] = TAP
        except Exception:
            LOG.exception("NASA TOI request failed; trying ExoFOP downloadable CSV")
            table = fetch_csv(EXOFOP, path, cfg["timeout_seconds"])
            table["catalog_source"] = EXOFOP
        table.to_csv(path, index=False)
    table = table.rename(
        columns={
            "tid": "tic_id",
            "toi": "toi_id",
            "tfopwg_disp": "disposition",
            "pl_orbper": "catalog_period",
            "st_rad": "stellar_radius",
            "st_mass": "stellar_mass",
            "TIC ID": "tic_id",
            "TOI": "toi_id",
            "TFOPWG Disposition": "disposition",
            "Period (days)": "catalog_period",
            "Stellar Radius (R_Sun)": "stellar_radius",
        }
    )
    required = {"tic_id", "disposition"}
    if not required.issubset(table):
        raise ValueError(f"Catalogue requires {required}; got {list(table.columns)}")
    table["tic_id"] = pd.to_numeric(table.tic_id, errors="raise").astype("int64")
    table["disposition"] = table.disposition.fillna("UNKNOWN").str.strip()
    return table


def select_sample(root: Path, config: dict, force: bool = False) -> pd.DataFrame:
    """Seeded sample; background is unlabelled, never assumed planet-free."""
    cfg = config["data"]
    table = toi_catalog(root, cfg, force)
    table.to_csv(root / "data/catalog/normalized_catalog.csv", index=False)
    rows = []
    for tic, group in table.groupby("tic_id", sort=True):
        dispositions = set(group.disposition)
        positive = bool(dispositions & {"CP", "KP", "PC"})
        negative = bool(dispositions & {"FP", "FA"})
        label = (
            "ambiguous"
            if positive and negative
            else ("planet" if positive else "false_positive" if negative else "ambiguous")
        )
        row = (
            group.sort_values("toi_id").iloc[0].to_dict()
            if "toi_id" in group
            else group.iloc[0].to_dict()
        )
        row.update(tic_id=tic, label=label, disposition=";".join(sorted(dispositions)))
        rows.append(row)
    targets = pd.DataFrame(rows)
    excluded = set()
    if cfg.get("exclude_tics_csv"):
        excluded = set(pd.read_csv(root / cfg["exclude_tics_csv"]).tic_id.astype("int64"))
        targets = targets[~targets.tic_id.isin(excluded)]
    observing_pool = sector_target_pool(root, cfg, force) if cfg.get("sectors") else None
    if observing_pool is not None:
        targets = targets[targets.tic_id.isin(observing_pool.tic_id)]
    chosen = []
    for label, key in [
        ("planet", "sample_size_planets"),
        ("false_positive", "sample_size_false_positive"),
    ]:
        pool = targets[targets.label == label]
        n = min(cfg[key], len(pool))
        if n < cfg[key]:
            LOG.warning("Requested %d %s targets; catalogue has %d", cfg[key], label, n)
        chosen.append(pool.sample(n=n, random_state=config["random_seed"]))
    nbg = cfg["sample_size_background"]
    if nbg:
        if cfg.get("background_csv"):
            background = pd.read_csv(root / cfg["background_csv"])
        else:
            background = (
                observing_pool.copy()
                if observing_pool is not None
                else sector_target_pool(root, cfg, force)
            )
        background["tic_id"] = background.tic_id.astype("int64")
        background = background[~background.tic_id.isin(table.tic_id)]
        background = background[~background.tic_id.isin(excluded)]
        if len(background) < nbg:
            LOG.warning("Requested %d background targets; only %d available", nbg, len(background))
        background = background.sample(
            min(nbg, len(background)), random_state=config["random_seed"]
        )
        background["label"] = "background"
        background["disposition"] = "UNLABELLED"
        background["catalog_source"] = "MAST SPOC sector LC manifest or user-supplied control CSV"
        chosen.append(background)
    sample = pd.concat(chosen, ignore_index=True)
    if cfg.get("sanity_tics"):
        sample = targets[targets.tic_id.isin(cfg["sanity_tics"])].copy()
    if sample.empty:
        raise ValueError("No sample targets available")
    sample.to_csv(root / "data/catalog/sample.csv", index=False)
    LOG.info("Selected %d targets: %s", len(sample), sample.label.value_counts().to_dict())
    return sample
