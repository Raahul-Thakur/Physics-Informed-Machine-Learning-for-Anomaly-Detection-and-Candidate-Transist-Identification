import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("injections_v3", ROOT / "scripts/injections_v3.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_noise_strata_selection_unique_repeatable_and_readonly(tmp_path):
    (tmp_path / "data/raw").mkdir(parents=True)
    rows = []
    rng = np.random.default_rng(3)
    for tic in range(1, 10):
        path = tmp_path / f"data/raw/{tic}.npz"
        np.savez(path, flux=1 + rng.normal(0, 0.0001 * tic, 100))
        rows.append(dict(tic_id=tic, sector=1, raw_path=f"data/raw/{tic}.npz"))
    pd.DataFrame(rows).to_csv(tmp_path / "data/raw/manifest.csv", index=False)
    before = {p: p.read_bytes() for p in tmp_path.rglob("*.npz")}
    a, failures = module.select_curves(tmp_path, 6, 42)
    b, _ = module.select_curves(tmp_path, 6, 42)
    pd.testing.assert_frame_equal(a, b)
    assert failures.empty
    assert a.tic_id.nunique() == 6
    assert a.groupby("noise_stratum", observed=True).size().tolist() == [2, 2, 2]
    assert all(p.read_bytes() == data for p, data in before.items())
    with pytest.raises(ValueError, match="only 9 usable"):
        module.select_curves(tmp_path, 10, 42)
