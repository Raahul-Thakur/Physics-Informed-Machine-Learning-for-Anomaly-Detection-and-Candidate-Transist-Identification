import importlib.util
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("ephem", ROOT / "scripts/prepare_ephemerides.py")
ephem = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ephem)


def test_reject_unknown_time_ttv_missing_errors_and_unselected_targets():
    row = dict(
        pl_name="Example b",
        tic_id="TIC 1",
        pl_tsystemref="BJD-TDB",
        pl_orbper=3.0,
        pl_orbpererr1=0.001,
        pl_orbpererr2=-0.002,
        pl_tranmid=2459000.0,
        pl_tranmiderr1=0.003,
        pl_tranmiderr2=-0.004,
        ttv_flag=0,
        pl_orbperlim=0,
        pl_tranmidlim=0,
        pl_refname="paper",
        default_flag=1,
        pl_pubdate="2020",
        rowupdate="2020",
    )
    bad = [
        dict(row, pl_tsystemref="BJD"),
        dict(row, ttv_flag=1),
        dict(row, pl_orbpererr2=float("nan")),
        dict(row, tic_id="TIC 2"),
    ]
    result, audit = ephem.select(pd.DataFrame([row, *bad]), [1])
    assert len(result) == 1 and audit.eligible.sum() == 1
    assert result.period_error_days.iloc[0] == 0.002
    assert result.epoch_error_days.iloc[0] == 0.004


def test_choose_one_coherent_solution_without_mixing_parameters():
    row = dict(
        pl_name="Example b",
        tic_id="TIC 1",
        pl_tsystemref="BJD-TDB",
        pl_orbper=3.0,
        pl_orbpererr1=0.001,
        pl_orbpererr2=-0.002,
        pl_tranmid=2459000.0,
        pl_tranmiderr1=0.003,
        pl_tranmiderr2=-0.004,
        ttv_flag=0,
        pl_orbperlim=0,
        pl_tranmidlim=0,
        pl_refname="paper",
        default_flag=1,
        pl_pubdate="2020",
        rowupdate="2020",
    )
    newer = dict(row, default_flag=0, pl_pubdate="2025", pl_orbper=4.0, pl_tranmid=2460000.0)
    result, _ = ephem.select(pd.DataFrame([newer, row]), [1])
    assert len(result) == 1
    assert result.period_days.iloc[0] == 3.0
    assert result.epoch_bjd_tdb.iloc[0] == 2459000.0
