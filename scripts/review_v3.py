"""Deterministically select contrasting ranking cases and plot measured morphology."""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import research_v3 as v3

from tess_anomaly.bls import phase


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path("experiments/independent_v3"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("Review output already exists")
    scores = pd.read_csv(args.workspace / "evaluation/candidates.csv")
    b = v3.ranked(scores, "bls")
    h = v3.ranked(scores, "semi_hybrid")
    ids_b, ids_h = set(b.tic_id.head(100)), set(h.tic_id.head(100))
    positive = set(scores.loc[scores.label.eq("planet"), "tic_id"])
    groups = {
        "both": positive & ids_b & ids_h,
        "bls_only": positive & (ids_b - ids_h),
        "hybrid_only": positive & (ids_h - ids_b),
        "false_positive": set(scores.loc[scores.label.eq("false_positive"), "tic_id"]),
        "background": set(scores.loc[scores.label.eq("background"), "tic_id"]),
    }
    manifest = pd.read_csv(args.workspace / "data/processed/manifest.csv").set_index(
        ["tic_id", "sector"]
    )
    args.output.mkdir(parents=True)
    rows = []
    for group, ids in groups.items():
        ranking = b if group == "bls_only" else h
        for row in ranking[ranking.tic_id.isin(ids)].head(2).to_dict("records"):
            row["review_group"] = group
            rows.append(row)
            meta = manifest.loc[(row["tic_id"], row["sector"])]
            with np.load(args.workspace / meta.processed_path) as archive:
                curve = dict(archive)
            fig, axes = plt.subplots(2, 2, figsize=(10, 7))
            axes[0, 0].plot(curve["time"], curve["flux"], ".", ms=1, rasterized=True)
            axes[0, 0].set(xlabel="Time (BTJD)", ylabel="Detrended relative flux")
            with np.load(args.workspace / meta.power_path) as power:
                axes[0, 1].plot(power["period"], power["power"], lw=0.7)
            axes[0, 1].set(xlabel="Period (days)", ylabel="BLS objective")
            folded = phase(curve["time"], row["best_period"], row["transit_epoch"]) * 24
            width = 2 * row["best_duration"] * 24
            inside = abs(folded) <= width
            axes[1, 0].scatter(
                folded[inside], curve["flux"][inside], s=2, alpha=0.3, rasterized=True
            )
            bins = np.linspace(-width, width, 41)
            which = np.digitize(folded, bins)
            mid = (bins[:-1] + bins[1:]) / 2
            med = [
                np.median(curve["flux"][which == i]) if (which == i).any() else np.nan
                for i in range(1, len(bins))
            ]
            axes[1, 0].plot(mid, med, "o", ms=3, color="#D55E00")
            axes[1, 0].set(xlabel="Hours from fitted transit centre", ylabel="Relative flux")
            axes[1, 1].axis("off")
            fields = [
                "disposition",
                "best_period",
                "best_duration",
                "best_depth",
                "depth_snr",
                "anomaly",
                "semi_hybrid",
                "number_observed_transits",
                "signal_match",
                "event_depth_relative_mad",
                "single_event_power_fraction_proxy",
            ]
            text = []
            for key in fields:
                value = row.get(key)
                text.append(
                    f"{key}: {value:.5g}" if isinstance(value, float) else f"{key}: {value}"
                )
            axes[1, 1].text(0, 1, "\n".join(text), va="top", fontsize=9)
            fig.suptitle(
                f"{group}: TIC {int(row['tic_id'])}, sector {int(row['sector'])}; unvalidated photometric signal"
            )
            fig.tight_layout()
            for ext in ["png", "pdf"]:
                fig.savefig(args.output / f"{group}_tic{int(row['tic_id'])}.{ext}", dpi=140)
            plt.close(fig)
    pd.DataFrame(rows).to_csv(args.output / "selected_cases.csv", index=False)
    v3.write_json(
        args.output / "selection_rule.json",
        dict(
            k=100,
            per_group=2,
            selection="Highest semi_hybrid target rank within group; BLS rank for BLS-only; TIC/sector tie breaks.",
            interpretation="Descriptive morphology review, not population prevalence, causal attribution or planet validation.",
            script_sha256=v3.sha(__file__),
            scores_sha256=v3.sha(args.workspace / "evaluation/candidates.csv"),
            group_available={k: len(ids) for k, ids in groups.items()},
        ),
    )
    v3.seal(args.output)


if __name__ == "__main__":
    main()
