import pandas as pd

from tess_anomaly.catalog import select_sample
from tess_anomaly.config import prepare


def test_catalog_labels_no_background_fabrication(tmp_path):
    cfg = {
        "root": str(tmp_path),
        "random_seed": 42,
        "data": {
            "catalog_csv": "catalog.csv",
            "background_csv": "background.csv",
            "sectors": None,
            "sample_size_planets": 10,
            "sample_size_false_positive": 10,
            "sample_size_background": 10,
        },
    }
    root = prepare(cfg)
    pd.DataFrame(
        {"tic_id": [1, 2, 3, 3, 4], "disposition": ["CP", "FP", "PC", "FP", "APC"]}
    ).to_csv(root / "catalog.csv", index=False)
    pd.DataFrame({"tic_id": [1, 2, 5, 6]}).to_csv(root / "background.csv", index=False)
    sample = select_sample(root, cfg)
    assert set(sample.tic_id) == {1, 2, 5, 6}
    assert sample.set_index("tic_id").loc[5, "label"] == "background"
    assert len(sample) == 4  # Never fill unavailable class quotas with invented IDs.
    pd.DataFrame({"tic_id": [1, 5]}).to_csv(root / "excluded.csv", index=False)
    cfg["data"]["exclude_tics_csv"] = "excluded.csv"
    excluded_sample = select_sample(root, cfg)
    assert set(excluded_sample.tic_id) == {2, 6}


def test_automatic_background_uses_observing_pool_not_label_pool(tmp_path, monkeypatch):
    from tess_anomaly import catalog

    cfg = {
        "root": str(tmp_path),
        "random_seed": 42,
        "data": {
            "catalog_csv": "catalog.csv",
            "background_csv": None,
            "sectors": [1],
            "sample_size_planets": 1,
            "sample_size_false_positive": 1,
            "sample_size_background": 2,
        },
    }
    root = prepare(cfg)
    pd.DataFrame({"tic_id": [1, 2], "disposition": ["CP", "FP"]}).to_csv(
        root / "catalog.csv", index=False
    )
    monkeypatch.setattr(
        catalog, "sector_target_pool", lambda *args: pd.DataFrame({"tic_id": [1, 2, 3, 4]})
    )
    sample = select_sample(root, cfg)
    assert sample.label.value_counts().to_dict() == {
        "background": 2,
        "planet": 1,
        "false_positive": 1,
    }
