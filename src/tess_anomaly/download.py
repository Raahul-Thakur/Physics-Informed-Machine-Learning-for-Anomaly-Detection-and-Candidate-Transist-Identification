"""Conservative serial Lightkurve downloads, preserving unfiltered cadences."""

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from .config import fingerprint

LOG = logging.getLogger(__name__)


def download_sample(
    root: Path, sample: pd.DataFrame, cfg: dict, force: bool = False
) -> pd.DataFrame:
    import lightkurve as lk
    from astroquery.mast import Observations

    Observations.TIMEOUT = cfg["timeout_seconds"]
    rows, failures = [], []
    key = fingerprint(
        {k: cfg.get(k) for k in ("sectors", "cadence_seconds", "max_sectors_per_target")}
    )
    for target in sample.to_dict("records"):
        tic = int(target["tic_id"])
        manifest = root / f"data/cache/download_{tic}_{key}.csv"
        if manifest.exists() and not force:
            cached = pd.read_csv(manifest)
            if all((root / p).exists() for p in cached.raw_path):
                rows.extend({**old, **target} for old in cached.to_dict("records"))
                continue
        target_rows = []
        try:
            search = lk.search_lightcurve(
                f"TIC {tic}",
                mission="TESS",
                author="SPOC",
                sector=cfg.get("sectors"),
                exptime=cfg.get("cadence_seconds"),
            )
            if not len(search):
                raise LookupError("No matching SPOC light curves")
            seen = set()
            for i in range(len(search)):
                sector = int(search.table["sequence_number"][i])
                if sector in seen:
                    continue
                seen.add(sector)
                if len(seen) > cfg["max_sectors_per_target"]:
                    break
                try:
                    lc = search[i].download(
                        quality_bitmask="none", download_dir=str(root / "data/raw/mast")
                    )
                    if lc is None:
                        raise RuntimeError("MAST returned no light curve")
                    if int(lc.meta.get("TARGETID", tic)) != tic:
                        raise ValueError("Downloaded target ID mismatch")
                    path = Path(f"data/raw/tic{tic}_s{sector}_{key}.npz")
                    np.savez_compressed(
                        root / path,
                        time=np.asarray(lc.time.value, float),
                        flux=np.asarray(lc.flux.value, float),
                        flux_err=np.asarray(lc.flux_err.value, float),
                        quality=np.asarray(lc.quality, np.int64),
                    )
                    row = dict(
                        target,
                        sector=sector,
                        raw_path=path.as_posix(),
                        cadence_seconds=float(search.table["exptime"][i]),
                        mission="TESS",
                        author="SPOC",
                        flux_column="PDCSAP_FLUX",
                        time_system="BTJD (BJD_TDB - 2457000)",
                        product=str(search.table["productFilename"][i]),
                    )
                    target_rows.append(row)
                    LOG.info("Downloaded TIC %d sector %d: %d cadences", tic, sector, len(lc))
                except Exception as exc:
                    LOG.exception("Download failed TIC %d sector %d", tic, sector)
                    failures.append(
                        dict(tic_id=tic, sector=sector, stage="download", error=str(exc))
                    )
        except Exception as exc:
            LOG.exception("Search failed TIC %d", tic)
            failures.append(dict(tic_id=tic, sector=None, stage="search", error=str(exc)))
        if target_rows:
            pd.DataFrame(target_rows).to_csv(manifest, index=False)
            rows.extend(target_rows)
    pd.DataFrame(failures, columns=["tic_id", "sector", "stage", "error"]).to_csv(
        root / "outputs/logs/download_failures.csv", index=False
    )
    result = pd.DataFrame(rows)
    result.to_csv(root / "data/raw/manifest.csv", index=False)
    if result.empty:
        raise RuntimeError("No real light curves downloaded; inspect download_failures.csv")
    return result
