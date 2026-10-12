"""Compare all calibration-target sectors with coverage-selected single sectors."""

import argparse
import json
from pathlib import Path

import pandas as pd

from tess_anomaly.research import digest, evaluate_scores, load_frozen, score_bundle


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frozen", type=Path, default=Path("experiments/research_v2/frozen"))
    parser.add_argument(
        "--output", type=Path, default=Path("experiments/research_v2/development_exposure")
    )
    args = parser.parse_args()
    bundle = load_frozen(args.frozen)
    contract = json.loads((args.frozen / "protocol.json").read_text())
    path = args.frozen / "development_features.csv"
    if digest(path) != contract["development_feature_sha256"]:
        raise ValueError("Frozen development features changed")
    frame = pd.read_csv(path, float_precision="round_trip")
    frame = frame[frame.tic_id.isin(bundle["calibration_ids"])]
    evaluate_scores(
        score_bundle(bundle, frame, independent=False),
        bundle,
        args.output,
        "Development calibration targets, all sectors — not independent",
    )
    print(f"Compared {len(frame)} curves from {frame.tic_id.nunique()} development targets")


if __name__ == "__main__":
    main()
