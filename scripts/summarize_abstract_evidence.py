"""Reproducible supplementary tables and figures; no model fitting or selection."""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import research_v3 as v3
from sklearn.metrics import average_precision_score, roc_auc_score


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("Refusing to overwrite evidence summary")
    root = Path(__file__).resolve().parents[1]
    out = args.output
    out.mkdir(parents=True)
    injection = root / "experiments/research_v3/injections/results/injection_trials.csv"
    intervention = root / "experiments/abstract_evidence/interventions/interventions.csv"
    f = pd.read_csv(injection)
    f["retrieved"] = f.direct_period_recovered.fillna(False).astype(bool)
    table = f.groupby("method").agg(
        attempted=("status", "size"),
        processed=("status", lambda x: x.eq("ok").sum()),
        retrieved=("retrieved", "sum"),
        retrieval_fraction=("retrieved", "mean"),
        finite_depth_estimates=("paired_depth_relative_bias", "count"),
        median_depth_bias=("paired_depth_relative_bias", "median"),
    )
    table.to_csv(out / "injection_overall.csv")
    f.groupby(["method", "grid_eligible"]).agg(
        attempted=("status", "size"),
        retrieved=("retrieved", "sum"),
        retrieval_fraction=("retrieved", "mean"),
    ).to_csv(out / "injection_grid_eligibility.csv")
    # Resample whole stars, retaining all paired injected cases/methods.
    by_target = f.groupby(["tic_id", "method"]).retrieved.mean().unstack()
    difference = (by_target.savgol - by_target.rolling_median).to_numpy()
    rng = np.random.default_rng(20261006)
    draws = difference[rng.integers(len(difference), size=(5000, len(difference)))].mean(axis=1)
    v3.write_json(
        out / "injection_paired_uncertainty.json",
        dict(
            savgol_minus_rolling_median=float(difference.mean()),
            low=float(np.quantile(draws, 0.025)),
            high=float(np.quantile(draws, 0.975)),
            independent_units=len(difference),
            repeats=5000,
            scope="Paired whole-target bootstrap; conditional on this injection grid and selected stars",
        ),
    )
    selection = pd.read_csv(
        root / "experiments/research_v3/injections/noise_stratified_selection.csv"
    )
    f = f.merge(selection[["tic_id", "noise_stratum"]], on="tic_id", validate="many_to_one")
    strata = (
        f.groupby(["noise_stratum", "method"])
        .retrieved.mean()
        .unstack()
        .reindex(["low", "medium", "high"])
    )
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    strata.plot.bar(ax=axes[0], rot=0, color=["#E69F00", "#0072B2"])
    axes[0].set(xlabel="Raw-noise stratum", ylabel="Direct period retrieval fraction", ylim=(0, 1))
    axes[0].legend(title=None, fontsize=8)
    depth = (
        f.groupby(["noise_stratum", "method"])
        .paired_depth_relative_bias.median()
        .unstack()
        .reindex(["low", "medium", "high"])
    )
    (100 * depth).plot.bar(ax=axes[1], rot=0, color=["#E69F00", "#0072B2"], legend=False)
    axes[1].set(xlabel="Raw-noise stratum", ylabel="Median paired depth bias (%)")
    fig.suptitle("Synthetic signals in 30 real development stars; 14,400 method-trials")
    fig.tight_layout()
    for extension in ["png", "pdf"]:
        fig.savefig(out / f"injection_validation.{extension}", dpi=180)
    plt.close(fig)
    cases = pd.read_csv(intervention)
    changes = cases[cases.parameter.ne("base")].copy()
    changes["case"] = changes.apply(
        lambda r: f"{r.parameter}={r['injected_' + r.parameter]:.4g}", axis=1
    )
    grouped = changes.groupby(["tic_id", "case"]).semi_hybrid_delta_base.mean().unstack()
    grouped.to_csv(out / "intervention_target_phase_means.csv")
    fig, ax = plt.subplots(figsize=(9, 4))
    for tic, row in grouped.iterrows():
        ax.plot(range(len(row)), row.to_numpy(), marker="o", label=f"TIC {tic}")
    ax.set_xticks(range(len(grouped.columns)), grouped.columns, rotation=15)
    ax.axhline(0, color="grey", linewidth=0.8)
    ax.set(
        ylabel="Change in semi-hybrid score",
        title="Controlled input changes: mean over three paired phases",
    )
    ax.legend(fontsize=8)
    fig.tight_layout()
    for extension in ["png", "pdf"]:
        fig.savefig(out / f"controlled_interventions.{extension}", dpi=180)
    plt.close(fig)
    evaluation = root / "experiments/independent_v3/evaluation"
    inputs = {str(p.relative_to(root)): v3.sha(p) for p in [injection, intervention]}
    if evaluation.exists():
        v3.verify(evaluation)
        scores = pd.read_csv(evaluation / "candidates.csv")
        rows, discrimination = [], []
        for exposure, data in [("all_sectors", scores), ("one_sector", v3.one_sector(scores))]:
            for method in v3.METHODS:
                ranked = v3.ranked(data, method)
                known = (
                    ranked.disposition.fillna("")
                    .str.split(";")
                    .map(lambda d: bool(set(d) & {"CP", "KP"}))
                )
                positive = ranked.label.eq("planet")
                negative = ranked.label.eq("false_positive") & ranked.disposition.fillna(
                    ""
                ).str.split(";").map(lambda d: bool(set(d) & {"FP", "FA"}))
                reference = (known & positive) | negative
                truth = (known & positive)[reference]
                values = ranked.loc[reference, method]
                discrimination.append(
                    dict(
                        exposure=exposure,
                        method=method,
                        confirmed_known=int(truth.sum()),
                        labelled_false_positive=int((~truth).sum()),
                        roc_auc=float(roc_auc_score(truth, values))
                        if truth.nunique() == 2
                        else None,
                        average_precision=float(average_precision_score(truth, values))
                        if truth.nunique() == 2
                        else None,
                    )
                )
                rows.append(
                    dict(
                        exposure=exposure,
                        method=method,
                        k=100,
                        catalogue_positive_total=int(positive.sum()),
                        catalogue_positive_at_100=int(positive.head(100).sum()),
                        confirmed_known_total=int((known & positive).sum()),
                        confirmed_known_at_100=int((known & positive).head(100).sum()),
                        candidate_only_total=int((positive & ~known).sum()),
                        candidate_only_at_100=int((positive & ~known).head(100).sum()),
                        matched_positive_signals_at_100=int(
                            (positive & ranked.signal_match).head(100).sum()
                        ),
                        ephemeris_testable_positive_total=int(
                            (positive & ranked.epoch_testable).sum()
                        ),
                    )
                )
        pd.DataFrame(rows).to_csv(out / "ranking_reference_groups.csv", index=False)
        pd.DataFrame(discrimination).to_csv(
            out / "labelled_reference_discrimination.csv", index=False
        )
        inputs[str((evaluation / "manifest.json").relative_to(root))] = v3.sha(
            evaluation / "manifest.json"
        )
    v3.write_json(out / "provenance.json", dict(inputs=inputs, script_sha256=v3.sha(__file__)))
    (out / "README.md").write_text(
        "# Supplementary evidence\n\n"
        "Injection retrieval and depth distortion are synthetic-signal sensitivity measures, "
        "not planetary purity. The bootstrap resamples 30 whole stars; repeated phases are not "
        "independent stars. Intervention changes concern deterministic software output, not "
        "astrophysical causation. Duration values in the intervention figure are days.\n\n"
        "Ranking labels called planet by the pipeline include PC-only candidates. The separate "
        "reference-group table distinguishes these from CP/KP systems. The predefined primary "
        "comparison retains its original combined reference group; the CP/KP breakdown is "
        "supplementary. Signal matches require explicit ephemeris/time-system checks and do "
        "not constitute new planet validation.\n",
        encoding="utf-8",
    )
    v3.seal(out)


if __name__ == "__main__":
    main()
