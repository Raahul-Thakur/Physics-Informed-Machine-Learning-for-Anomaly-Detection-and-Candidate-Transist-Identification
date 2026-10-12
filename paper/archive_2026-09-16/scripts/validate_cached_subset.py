"""Run a separate real-data probe from already downloaded, catalogue-labelled products.

This never substitutes for the complete configured experiment. It uses up to
three available targets per class, and writes to experiments/cached_probe.
"""

import argparse
import copy
import shutil
from pathlib import Path

import pandas as pd

from tess_anomaly.config import load_config, prepare
from tess_anomaly.pipeline import curve_stages, evaluate, figures, report, train
from tess_anomaly.utils import provenance


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="config/small_test.yaml")
    args = parser.parse_args()
    cfg = load_config(args.config)
    source = Path(cfg["root"])
    sample = pd.read_csv(source / "data/catalog/sample.csv")
    cached = pd.concat([pd.read_csv(p) for p in (source / "data/cache").glob("download_*.csv")])
    cached = cached[cached.tic_id.isin(sample.tic_id)].drop_duplicates("tic_id")
    selected = cached.groupby("label", group_keys=False).head(3)
    if selected.label.nunique() < 3:
        raise ValueError("Wait until all three real catalogue groups have cached downloads")
    cfg = copy.deepcopy(cfg)
    cfg["root"] = str(source / "experiments/cached_probe")
    cfg["evaluation"]["candidate_reports"] = 1
    root = prepare(cfg)
    for row in selected.to_dict("records"):
        shutil.copy2(source / row["raw_path"], root / row["raw_path"])
    selected.to_csv(root / "data/raw/manifest.csv", index=False)
    sample[sample.tic_id.isin(selected.tic_id)].to_csv(
        root / "data/catalog/sample.csv", index=False
    )
    shutil.copy2(
        source / "data/catalog/normalized_catalog.csv", root / "data/catalog/normalized_catalog.csv"
    )
    curve_stages(root, cfg, "features", False)
    train(root, cfg)
    evaluate(root, cfg)
    figures(root, cfg)
    report(root)
    provenance(root, cfg, selected.tic_id.tolist(), "completed:separate_real_cached_probe")
    print(f"Real cached probe completed: {len(selected)} light curves at {root}")


if __name__ == "__main__":
    main()
