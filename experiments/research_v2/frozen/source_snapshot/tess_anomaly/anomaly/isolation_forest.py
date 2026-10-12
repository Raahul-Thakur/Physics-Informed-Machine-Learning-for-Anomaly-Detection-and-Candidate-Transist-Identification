"""Isolation Forest scoring."""

import numpy as np
from sklearn.ensemble import IsolationForest


def fit(matrix: np.ndarray, cfg: dict, seed: int) -> tuple[IsolationForest, np.ndarray]:
    model = IsolationForest(
        **{k: v for k, v in cfg.items() if k != "enabled"}, random_state=seed, n_jobs=1
    )
    model.fit(matrix)
    return model, -model.score_samples(matrix)
