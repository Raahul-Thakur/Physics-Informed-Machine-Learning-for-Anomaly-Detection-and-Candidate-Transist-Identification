import copy
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from tess_anomaly.config import load_config, prepare
from tess_anomaly.features import FAMILIES
from tess_anomaly.pipeline import curve_stages, evaluate, figures, report, train
from tess_anomaly.utils import synthetic_curve


def test_ablation_reproduces_primary_with_subsampling(tmp_path):
    cfg = load_config(Path(__file__).parents[1] / "config/small_test.yaml")
    cfg["root"] = str(tmp_path)
    cfg["models"]["isolation_forest"]["n_estimators"] = 25
    root = prepare(cfg)
    rng = np.random.default_rng(12)
    features = pd.DataFrame(
        {
            "tic_id": rng.permutation(300),
            "sector": 1,
            "label": ["planet", "false_positive", "background"] * 100,
            "disposition": ["CP", "FP", "UNKNOWN"] * 100,
            "std_flux": rng.lognormal(size=300),
            "best_period": rng.uniform(0.5, 12, 300),
            "depth_snr": rng.lognormal(size=300),
            "bls_max_power": rng.lognormal(size=300),
            "measured_depth": rng.uniform(0, 0.1, 300),
        }
    )
    for column in FAMILIES["all"]:
        if column not in features:
            features[column] = np.nan
    features.to_csv(root / "data/features/features.csv", index=False)
    train(root, cfg)
    evaluate(root, cfg)
    main = pd.read_csv(root / "outputs/tables/model_performance.csv")
    ablation = pd.read_csv(root / "outputs/tables/ablation_results.csv")
    pd.testing.assert_frame_equal(
        main,
        ablation[ablation.feature_family.eq("all")]
        .drop(columns="feature_family")
        .reset_index(drop=True),
    )


def test_offline_pipeline(tmp_path):
    cfg = copy.deepcopy(load_config(Path(__file__).parents[1] / "config/small_test.yaml"))
    cfg["root"] = str(tmp_path)
    cfg["models"]["isolation_forest"]["n_estimators"] = 25
    cfg["evaluation"]["candidate_reports"] = 1
    root = prepare(cfg)
    (root / "outputs/config_used.yaml").write_text(yaml.safe_dump(cfg))
    rows = []
    for i in range(8):
        raw, _ = synthetic_curve(seed=i, period=2 + 0.2 * i, depth=0.001 * (i + 1))
        path = f"data/raw/synthetic_validation_{i}.npz"
        np.savez_compressed(root / path, **raw)
        rows.append(
            dict(
                tic_id=i,
                sector=1,
                raw_path=path,
                label="background",
                disposition="SYNTHETIC_VALIDATION",
                catalog_period=np.nan,
            )
        )
    pd.DataFrame(rows).to_csv(root / "data/raw/manifest.csv", index=False)
    pd.DataFrame(rows).to_csv(root / "data/catalog/sample.csv", index=False)
    curve_stages(root, cfg, "features", False)
    train(root, cfg)
    evaluate(root, cfg)
    main = pd.read_csv(root / "outputs/tables/model_performance.csv")
    ablation = pd.read_csv(root / "outputs/tables/ablation_results.csv")
    pd.testing.assert_frame_equal(
        main,
        ablation[ablation.feature_family.eq("all")]
        .drop(columns="feature_family")
        .reset_index(drop=True),
    )
    figures(root, cfg)
    report(root)
    assert (root / "outputs/research_summary.md").exists()
    assert len(pd.read_csv(root / "outputs/rankings/ranked_targets.csv")) == 8
    assert len(list((root / "outputs/figures").glob("*.pdf"))) >= 10
    summary = (root / "outputs/research_summary.md").read_text(encoding="utf-8")
    assert "1 of the top 1" in summary
    assert "Sector coverage differs" in summary
