import numpy as np
import pandas as pd

from tess_anomaly.evaluation import ranking_metrics, target_scores


def test_unknown_exclusion_and_target_aggregation():
    frame = pd.DataFrame(
        dict(
            tic_id=[1, 1, 2, 3, 4],
            sector=[1, 2, 1, 1, 1],
            label=["planet", "planet", "false_positive", "background", "planet"],
            disposition=["CP", "CP", "FP", "UNLABELLED", "PC"],
            depth_snr=[5, 6, 1, 10, 8],
        )
    )
    targets = target_scores(frame)
    assert len(targets) == 4
    metrics = ranking_metrics(targets, dict(top_k=[1, 2, 10], top_fractions=[0.1]))
    first = metrics.iloc[0]
    assert first.precision_at_k == 0  # Unlabelled highest-ranked object is not a known recovery.
    assert first.binary_n == 2  # PC and unlabelled excluded from binary accuracy.
    assert first.roc_auc == 1
    assert metrics.iloc[-1].k == 4


def test_single_class_auc_unavailable():
    frame = pd.DataFrame(dict(tic_id=[1], label=["planet"], disposition=["CP"], depth_snr=[3.0]))
    row = ranking_metrics(frame, dict(top_k=[5], top_fractions=[0.1])).iloc[0]
    assert np.isnan(row.roc_auc)
    assert "Not calculated because" in row.metric_note
