"""Export verified research outputs into a self-contained editable poster package."""

import hashlib
import json
import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch

from tess_anomaly.bls import phase

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "poster/overleaf"
BLUE, ORANGE, GREEN = "#0072B2", "#D55E00", "#009E73"


def save(fig, name):
    fig.savefig(OUT / f"figures/{name}.pdf", bbox_inches="tight")
    fig.savefig(OUT / f"figures/{name}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def main():
    for name in ["figures", "data", "text"]:
        (OUT / name).mkdir(parents=True, exist_ok=True)
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 13,
            "axes.labelsize": 13,
            "axes.titlesize": 14,
            "legend.fontsize": 11,
            "pdf.fonttype": 42,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )
    sources = {
        "recovery_curves.csv": "experiments/independent_v3/evaluation/recovery_curves.csv",
        "paired_uncertainty.csv": "experiments/independent_v3/evaluation/paired_uncertainty.csv",
        "inspection_budgets.csv": "experiments/independent_v3/evaluation/inspection_budgets.csv",
        "reference_groups.csv": "experiments/abstract_evidence/final_summary/ranking_reference_groups.csv",
        "all_method_discrimination.csv": "experiments/abstract_evidence/final_summary/labelled_reference_discrimination.csv",
        "complementarity.csv": "experiments/independent_v3/evaluation/complementarity.csv",
        "injection_overall.csv": "experiments/abstract_evidence/final_summary/injection_overall.csv",
        "injection_by_noise.csv": "experiments/research_v3/injections/noise_stratified_recovery.csv",
        "significance_summary.json": "experiments/abstract_evidence/significance/summary.json",
        "diagnostic_cases.csv": "experiments/abstract_evidence/diagnostic_review/selected_cases.csv",
    }
    for dest, source in sources.items():
        shutil.copy2(ROOT / source, OUT / "data" / dest)
    fig, ax = plt.subplots(figsize=(8.5, 4.6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    steps = [
        ("01  PUBLIC TESS PHOTOMETRY", "SPOC light curves; original quality flags"),
        ("02  PREPROCESSING", "Quality filtering, normalisation, gap segmentation, detrending"),
        ("03  CONVENTIONAL SEARCH", "BLS period, epoch, depth and duration"),
        ("04  ASTROPHYSICAL FEATURES", "Transit coherence, morphology and local variability"),
        ("05  FROZEN MODELS", "Unsupervised IF/LOF + semi-supervised label spreading"),
        ("06  CANDIDATE PRIORITISATION", "Rankings, ephemeris checks and score diagnostics"),
    ]
    for i, (title, detail) in enumerate(steps):
        y = 0.94 - i * 0.158
        ax.add_patch(
            FancyBboxPatch(
                (0.025, y - 0.112),
                0.95,
                0.115,
                boxstyle="round,pad=0.009",
                facecolor="#EFF5F8",
                edgecolor=BLUE,
                linewidth=1,
            )
        )
        ax.text(
            0.055, y - 0.03, title, fontsize=13, fontweight="bold", va="center", color="#153044"
        )
        ax.text(0.055, y - 0.078, detail, fontsize=11.5, va="center")
        if i < 5:
            ax.annotate(
                "",
                xy=(0.5, y - 0.151),
                xytext=(0.5, y - 0.119),
                arrowprops={"arrowstyle": "->", "color": BLUE},
            )
    save(fig, "pipeline")

    f = pd.read_csv(OUT / "data/recovery_curves.csv")
    fig, ax = plt.subplots(figsize=(9.4, 5.5))
    labels = {
        "bls": ("BLS", BLUE, "-"),
        "unsupervised_hybrid": ("Unsupervised hybrid", GREEN, "--"),
        "semi_hybrid": ("Primary semi-supervised hybrid", ORANGE, "-"),
    }
    for method, (label, color, style) in labels.items():
        p = f[f.exposure.eq("all_sectors") & f.method.eq(method) & f.k.le(250)]
        ax.step(p.k, 100 * p.recall, where="post", label=label, color=color, ls=style, lw=2.4)
    ax.axvline(100, color="#777777", ls=":", lw=1.2)
    ax.axhline(10, color="#777777", ls=":", lw=1.2)
    ax.text(103, 2, "K = 100", fontsize=11, color="#555555")
    ax.text(246, 10.5, "10% recovery", ha="right", fontsize=11, color="#555555")
    for y, label, color, offset in [
        (32 / 3, "BLS: 32/300", BLUE, 26),
        (8, "Hybrid: 24/300", ORANGE, -29),
    ]:
        ax.scatter([100], [y], color=color, zorder=4, s=40)
        ax.annotate(
            label,
            (100, y),
            xytext=(-125 if color == BLUE else 16, offset),
            textcoords="offset points",
            color=color,
            fontsize=12,
            fontweight="bold",
            arrowprops={"arrowstyle": "-", "color": color},
        )
    ax.set(
        xlabel="Targets inspected",
        ylabel="Catalogue-positive recovery (%)",
        xlim=(0, 250),
        ylim=(0, 35),
    )
    ax.legend(loc="upper left", frameon=False)
    ax.grid(axis="y", alpha=0.15)
    fig.tight_layout()
    save(fig, "recovery_budget")

    cases = pd.read_csv(OUT / "data/diagnostic_cases.csv").set_index("tic_id")
    manifest = pd.read_csv(
        ROOT / "experiments/independent_v3/data/processed/manifest.csv"
    ).set_index(["tic_id", "sector"])
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.3))
    examples = [
        (160708862, "BLS-only recovery", BLUE),
        (201248411, "Hybrid-only recovery", ORANGE),
        (146520491, "High-ranked background", "#777777"),
    ]
    for ax, (tic, title, color) in zip(axes, examples):
        row = cases.loc[tic]
        meta = manifest.loc[(tic, int(row.sector))]
        source = ROOT / "experiments/independent_v3" / meta.processed_path
        with np.load(source) as archive:
            t, flux = archive["time"], archive["flux"]
        hours = 24 * phase(t, row.best_period, row.transit_epoch)
        width = 48 * row.best_duration
        mask = abs(hours) <= width
        pd.DataFrame({"hours_from_fitted_centre": hours[mask], "relative_flux": flux[mask]}).to_csv(
            OUT / f"data/phase_tic{tic}.csv", index=False
        )
        ax.scatter(hours[mask], flux[mask], s=2, alpha=0.18, color=color, rasterized=True)
        bins = np.linspace(-width, width, 41)
        which = np.digitize(hours, bins)
        med = [
            np.median(flux[which == i]) if (which == i).any() else np.nan
            for i in range(1, len(bins))
        ]
        ax.plot((bins[:-1] + bins[1:]) / 2, med, color="#111111", lw=1.8)
        ax.set_title(f"{title}\nTIC {tic}", fontsize=12)
        ax.set_xlabel("Hours from fitted centre", fontsize=11)
        ax.tick_params(labelsize=10)
        ax.text(
            0.97,
            0.04,
            f"P = {row.best_period:.3f} d\n{row.disposition}",
            ha="right",
            transform=ax.transAxes,
            fontsize=10,
        )
    axes[0].set_ylabel("Relative flux", fontsize=12)
    fig.tight_layout(w_pad=1)
    save(fig, "contrasting_light_curves")

    noise = pd.read_csv(OUT / "data/injection_by_noise.csv")
    fig, axes = plt.subplots(1, 2, figsize=(9.4, 3.25))
    x = np.arange(3)
    for method, label, color, offset in [
        ("savgol", "Savitzky-Golay", BLUE, -0.19),
        ("rolling_median", "Rolling median", ORANGE, 0.19),
    ]:
        p = noise[noise.method.eq(method)].set_index("noise_stratum").loc[["low", "medium", "high"]]
        axes[0].bar(
            x + offset, 100 * p.recovery_including_failures, width=0.36, color=color, label=label
        )
        axes[1].bar(x + offset, 100 * p.median_depth_bias, width=0.36, color=color)
    for ax in axes:
        ax.set_xticks(x, ["Low", "Medium", "High"])
        ax.set_xlabel("Raw-noise stratum")
        ax.tick_params(labelsize=11)
    axes[0].set(ylabel="Period retrieval (%)", ylim=(0, 100))
    axes[0].legend(fontsize=9.5, frameon=False, loc="upper right")
    axes[1].set_ylabel("Median depth bias (%)")
    fig.tight_layout(w_pad=2)
    save(fig, "injection_validation")

    for source, dest in [
        ("paper/v3/completed_evidence.md", "FULL_RESULTS.md"),
        ("paper/v3/submitted_abstract.md", "SUBMITTED_ABSTRACT.md"),
    ]:
        shutil.copy2(ROOT / source, OUT / dest)
    guide = (ROOT / "RESEARCH_GUIDE.md").read_text(encoding="utf-8")
    protocol = guide.split("<!-- BEGIN abstract_evidence_plan -->", 1)[1].split(
        "<!-- END abstract_evidence_plan -->", 1
    )[0].strip()
    (OUT / "EVIDENCE_PROTOCOL.md").write_text(protocol + "\n", encoding="utf-8")
    provenance = {
        source: hashlib.sha256((ROOT / source).read_bytes()).hexdigest()
        for source in sources.values()
    }
    (OUT / "data/source_hashes.json").write_text(json.dumps(provenance, indent=2), encoding="utf-8")
    print("Exported poster figures, numerical tables and supporting evidence:", OUT)


if __name__ == "__main__":
    main()
