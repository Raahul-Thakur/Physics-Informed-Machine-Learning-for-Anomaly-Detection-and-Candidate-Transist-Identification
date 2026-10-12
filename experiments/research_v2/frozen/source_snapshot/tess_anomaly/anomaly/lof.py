"""LOF fit-time scores; novelty scoring is deliberately separate."""

import numpy as np
from sklearn.neighbors import LocalOutlierFactor


def fit(matrix: np.ndarray, cfg: dict) -> tuple[LocalOutlierFactor, np.ndarray]:
    if len(matrix) < 3:
        raise ValueError("LOF needs at least three reference samples")
    options = {k: v for k, v in cfg.items() if k not in {"enabled", "n_neighbors"}}
    model = LocalOutlierFactor(
        n_neighbors=min(cfg["n_neighbors"], len(matrix) - 1), novelty=False, **options
    )
    model.fit_predict(matrix)
    return model, -model.negative_outlier_factor_


def fit_novelty(reference: np.ndarray, cfg: dict) -> LocalOutlierFactor:
    """Use score_unseen only on points excluded from this reference set."""
    options = {k: v for k, v in cfg.items() if k not in {"enabled", "n_neighbors"}}
    return LocalOutlierFactor(
        n_neighbors=min(cfg["n_neighbors"], len(reference) - 1), novelty=True, **options
    ).fit(reference)


def score_unseen(model: LocalOutlierFactor, matrix: np.ndarray) -> np.ndarray:
    if not model.novelty:
        raise ValueError("Fit-time LOF model cannot score new points; use fit_novelty")
    return -model.score_samples(matrix)
