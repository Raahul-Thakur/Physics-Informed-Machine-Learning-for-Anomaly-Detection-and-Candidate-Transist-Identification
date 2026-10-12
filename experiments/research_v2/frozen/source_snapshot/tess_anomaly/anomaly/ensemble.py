"""Equal-weight percentile ranks, fixed without evaluation-label tuning."""

import pandas as pd


def rank_normalize(values: pd.Series) -> pd.Series:
    """Average ties; finite sample ranks in (0, 1]."""
    return values.rank(method="average", pct=True)


def ensemble(scores: pd.DataFrame) -> pd.Series:
    return scores.apply(rank_normalize).mean(axis=1, skipna=False)
