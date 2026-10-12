import numpy as np
import pandas as pd

from tess_anomaly.anomaly import isolation_forest, lof
from tess_anomaly.anomaly.ensemble import rank_normalize
from tess_anomaly.dataset import fit_transform


def test_score_orientation():
    rng = np.random.default_rng(42)
    matrix = np.r_[rng.normal(0, 0.3, (100, 3)), [[8, 8, 8]]]
    _, a = isolation_forest.fit(matrix, dict(n_estimators=100, contamination="auto"), 42)
    _, b = lof.fit(matrix, dict(n_neighbors=15, contamination="auto", metric="minkowski"))
    assert a[-1] > np.quantile(a[:-1], 0.95)
    assert b[-1] > np.quantile(b[:-1], 0.95)
    novelty = lof.fit_novelty(matrix[:-1], dict(n_neighbors=15))
    assert lof.score_unseen(novelty, matrix[-1:])[0] > 2


def test_feature_contract_and_training_only_imputation():
    frame = pd.DataFrame(
        dict(
            mean_flux=[1.0, 2.0, np.nan, 4.0],
            std_flux=[1.0, 2.0, 3.0, 4.0],
            tic_id=[10, 20, 30, 40],
            sector=[1, 2, 3, 4],
            label=["a"] * 4,
        )
    )
    transform, _ = fit_transform(frame, dict(max_missing_fraction=0.6, scaler="robust"))
    assert set(transform.columns) == {"mean_flux", "std_flux"}
    before = transform.pipeline["imputer"].statistics_.copy()
    transform.transform(pd.DataFrame(dict(mean_flux=[10000], std_flux=[10000])))
    assert np.array_equal(before, transform.pipeline["imputer"].statistics_)
    assert rank_normalize(pd.Series([1.0, 1.0, 2.0])).tolist() == [0.5, 0.5, 1.0]


def test_catalogue_conditioned_proxies_are_opt_in():
    frame = pd.DataFrame({"mean_flux": [1.0, 2.0, 3.0], "radius_earth_proxy": [2.0, 4.0, 8.0]})
    cfg = dict(max_missing_fraction=0.6, scaler="robust")
    default, _ = fit_transform(frame, cfg)
    opted_in, _ = fit_transform(frame, dict(cfg, use_stellar_catalog_features=True))
    assert "radius_earth_proxy" not in default.columns
    assert "radius_earth_proxy" in opted_in.columns
