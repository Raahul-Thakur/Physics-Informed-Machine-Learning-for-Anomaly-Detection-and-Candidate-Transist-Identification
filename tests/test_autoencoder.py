import numpy as np
import pytest


def test_optional_autoencoder_determinism_and_group_separation():
    pytest.importorskip("torch")
    from tess_anomaly.anomaly.autoencoder import fit

    matrix = np.random.default_rng(42).normal(size=(20, 4))
    groups = np.repeat(np.arange(10), 2)
    cfg = dict(epochs=5, patience=2, learning_rate=0.001)
    model, scores = fit(matrix, groups, cfg, 42)
    _, again = fit(matrix, groups, cfg, 42)
    assert np.isfinite(scores).all() and np.all(scores >= 0)
    assert np.array_equal(scores, again)
    assert not set(groups[model["train_indices"]]) & set(groups[model["validation_indices"]])
