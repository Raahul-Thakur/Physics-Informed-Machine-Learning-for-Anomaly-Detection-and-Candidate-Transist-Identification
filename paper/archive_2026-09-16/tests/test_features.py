import numpy as np
from test_bls import BLS, PRE

from tess_anomaly.bls import search_bls
from tess_anomaly.features import FAMILIES, extract_features
from tess_anomaly.preprocessing import preprocess
from tess_anomaly.utils import synthetic_curve


def test_physical_features_and_no_infinities():
    raw, _ = synthetic_curve()
    curve = preprocess(raw, PRE)
    summary, _ = search_bls(curve, BLS)
    features = extract_features(curve, summary, dict(stellar_radius=1.0, stellar_mass=1.0))
    assert set(FAMILIES["all"]) <= features.keys()
    assert not any(np.isinf(features[k]) for k in FAMILIES["all"])
    assert 0.05 < features["radius_ratio_proxy"] < 0.15
    assert features["radius_earth_proxy"] > 0
    assert features["duration_ratio_proxy"] > 0
    assert features["measured_depth"] > 0.004
    no_star = extract_features(curve, summary, {})
    assert np.isnan(no_star["duration_ratio_proxy"])
