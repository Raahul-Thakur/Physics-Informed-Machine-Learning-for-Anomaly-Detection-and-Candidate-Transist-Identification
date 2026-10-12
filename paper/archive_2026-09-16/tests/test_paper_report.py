import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

spec = importlib.util.spec_from_file_location(
    "paper_report", Path(__file__).parents[1] / "scripts/paper_report.py"
)
paper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(paper)


def test_paired_bootstrap_identical_scores_and_row_order():
    frame = pd.DataFrame(
        dict(
            tic_id=np.arange(30),
            label=["planet", "background"] * 15,
            depth_snr=np.arange(30),
            hybrid_score=np.arange(30),
        )
    )
    result, draws = paper.paired_bootstrap(frame, repeats=100, seed=9, k=10)
    assert result["difference"] == result["difference_ci_low"] == result["difference_ci_high"] == 0
    _, shuffled = paper.paired_bootstrap(
        frame.sample(frac=1, random_state=1), repeats=100, seed=9, k=10
    )
    pd.testing.assert_frame_equal(draws, shuffled)


def test_bootstrap_reranks_paired_target_copies():
    frame = pd.DataFrame(
        dict(
            tic_id=np.arange(30),
            label=["planet"] * 10 + ["background"] * 20,
            depth_snr=np.arange(30),
            hybrid_score=-np.arange(30),
        )
    )
    result, draws = paper.paired_bootstrap(frame, repeats=10, seed=4, k=10)
    assert result["difference"] == 10
    sample = np.random.default_rng(4).integers(0, 30, 30)
    expected = (
        frame.iloc[sample]
        .sort_values("hybrid_score", ascending=False)
        .head(10)
        .label.eq("planet")
        .sum()
    )
    assert draws.iloc[0].hybrid_recovered == expected
    with pytest.raises(ValueError):
        paper.paired_bootstrap(pd.concat([frame, frame]), repeats=10, k=10)


def test_review_categories_and_sector_choice():
    frame = pd.DataFrame(
        dict(
            tic_id=np.arange(8),
            sector=1,
            label=["planet"] * 4 + ["false_positive"] * 2 + ["background"] * 2,
            disposition="UNLABELLED",
            depth_snr=[9, 8, 7, 0, 2, 1, 3, 4],
            hybrid_score=[9, 0, 7, 8, 2, 1, 3, 4],
        )
    )
    selected = paper.review_selection(frame, k=3, per_group=1).set_index("review_group")
    assert selected.loc["both", "tic_id"] == 0
    assert selected.loc["bls_only", "tic_id"] == 1
    assert selected.loc["hybrid_only", "tic_id"] == 3
    assert selected.loc["false_positive", "tic_id"] == 4
    assert selected.loc["background", "tic_id"] == 7
