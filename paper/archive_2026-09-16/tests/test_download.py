import numpy as np
import pandas as pd

from tess_anomaly.config import fingerprint, prepare
from tess_anomaly.download import download_sample


def test_cached_labels_refresh_and_one_failure_does_not_hide_success(tmp_path, monkeypatch):
    import lightkurve as lk

    root = prepare({"root": str(tmp_path)})
    cfg = {
        "sectors": [1],
        "cadence_seconds": 120,
        "max_sectors_per_target": 1,
        "timeout_seconds": 5,
    }
    key = fingerprint(
        {k: cfg.get(k) for k in ("sectors", "cadence_seconds", "max_sectors_per_target")}
    )
    np.savez(
        root / "data/raw/cached.npz",
        time=[1.0, 2.0],
        flux=[1.0, 1.0],
        flux_err=[0.1, 0.1],
        quality=[0, 0],
    )
    pd.DataFrame(
        [{"tic_id": 1, "sector": 1, "raw_path": "data/raw/cached.npz", "label": "old"}]
    ).to_csv(root / f"data/cache/download_1_{key}.csv", index=False)

    def unavailable(*args, **kwargs):
        raise ConnectionError("Explicit test-only archive failure")

    monkeypatch.setattr(lk, "search_lightcurve", unavailable)
    sample = pd.DataFrame({"tic_id": [1, 2], "label": ["planet", "background"]})
    result = download_sample(root, sample, cfg)
    assert len(result) == 1
    assert result.iloc[0].label == "planet"
    failures = pd.read_csv(root / "outputs/logs/download_failures.csv")
    assert failures.tic_id.tolist() == [2]
    assert "archive failure" in failures.iloc[0].error
