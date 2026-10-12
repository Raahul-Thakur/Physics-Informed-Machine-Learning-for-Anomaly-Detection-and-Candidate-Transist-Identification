"""Matplotlib-only publication and manual-vetting figures."""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

from .bls import phase
from .evaluation import score_columns, target_scores

plt.rcParams.update(
    {
        "font.size": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "savefig.dpi": 250,
        "pdf.fonttype": 42,
    }
)


def save(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    for extension in ("png", "pdf"):
        fig.savefig(path.with_suffix(f".{extension}"), bbox_inches="tight")
    plt.close(fig)


def diagnostic(curve: dict, periodogram: dict, row: dict, path: Path) -> None:
    fig, axes = plt.subplots(3, 2, figsize=(12, 10))
    t, f = curve["time"], curve["flux"]
    axes[0, 0].plot(t, curve["raw_flux"], ".", ms=1, rasterized=True)
    axes[0, 0].set(
        xlabel="Time [BTJD]",
        ylabel="PDCSAP flux [electron/s]",
        title="Original retained photometry",
    )
    axes[0, 1].plot(t, f, ".", ms=1, rasterized=True)
    axes[0, 1].set(xlabel="Time [BTJD]", ylabel="Relative flux", title="Detrended photometry")
    axes[1, 0].plot(periodogram["period"], periodogram["power"], lw=0.8)
    axes[1, 0].set(
        xlabel="Trial period [days]",
        ylabel="BLS power (configured objective)",
        title="Transit search",
    )
    ph = phase(t, row["best_period"], row["transit_epoch"])
    for ax, zoom in [(axes[1, 1], False), (axes[2, 0], True)]:
        select = np.abs(ph) < 2 * row["best_duration"] if zoom else np.ones(len(t), bool)
        ax.scatter(ph[select] * 24, f[select], s=2, alpha=0.25, rasterized=True)
        if select.sum() > 10:
            bins = np.linspace(ph[select].min(), ph[select].max(), 65)
            groups = np.digitize(ph[select], bins)
            bx, by = [], []
            for i in range(1, len(bins)):
                values = f[select][groups == i]
                if len(values):
                    bx.append((bins[i - 1] + bins[i]) * 12)
                    by.append(np.median(values))
            ax.plot(bx, by, "o", ms=3, color="darkorange", label="Binned median")
            ax.legend()
        ax.set(
            xlabel="Time from transit centre [hours]",
            ylabel="Relative flux",
            title="Transit window" if zoom else "Phase folded",
        )
    axes[2, 1].axis("off")
    fields = [
        "tic_id",
        "sector",
        "disposition",
        "best_period",
        "best_duration",
        "best_depth",
        "depth_snr",
        "odd_even_difference",
        "secondary_depth_proxy",
        "mad",
        "isolation_forest_score",
        "lof_score",
        "ensemble_score",
    ]
    lines = []
    for key in fields:
        value = row.get(key, "unavailable")
        lines.append(f"{key}: {value:.6g}" if isinstance(value, float) else f"{key}: {value}")
    axes[2, 1].text(0, 1, "\n".join(lines), va="top", family="monospace", fontsize=9)
    fig.suptitle(
        f"TIC {int(row['tic_id'])}, sector {int(row['sector'])} — inspection candidate, not validation"
    )
    save(fig, path)


def example_figures(curve: dict, periodogram: dict, row: dict, out: Path) -> None:
    """Separate exportable examples, selected for illustration rather than inference."""
    fig, axes = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
    axes[0].plot(curve["time"], curve["normalized_flux"], ".", ms=1, rasterized=True)
    axes[0].plot(curve["time"], curve["trend"], lw=0.7, color="darkorange", label="Estimated trend")
    axes[0].set(ylabel="Normalized PDCSAP flux")
    axes[0].legend()
    axes[1].plot(curve["time"], curve["flux"], ".", ms=1, rasterized=True)
    axes[1].set(xlabel="Time [BTJD]", ylabel="Detrended relative flux")
    fig.suptitle(f"Illustrative TIC {int(row['tic_id'])}, sector {int(row['sector'])}")
    save(fig, out / "example_raw_vs_detrended")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(periodogram["period"], periodogram["power"], lw=0.8)
    ax.axvline(
        row["best_period"], color="darkorange", ls="--", label=f"Best P={row['best_period']:.5f} d"
    )
    ax.set(xlabel="Trial period [days]", ylabel="BLS power (configured objective)")
    ax.legend()
    save(fig, out / "example_bls_periodogram")
    fig, ax = plt.subplots(figsize=(8, 4))
    ph = phase(curve["time"], row["best_period"], row["transit_epoch"])
    select = np.abs(ph) < 2 * row["best_duration"]
    ax.scatter(ph[select] * 24, curve["flux"][select], s=2, alpha=0.3, rasterized=True)
    ax.set(
        xlabel="Time from transit centre [hours]",
        ylabel="Relative flux",
        title=f"Folded TIC {int(row['tic_id'])}: illustrative highest-SNR catalogue-positive target",
    )
    save(fig, out / "example_phase_folded")


def make_figures(
    frame: pd.DataFrame, matrix: np.ndarray, columns: list[str], metrics: pd.DataFrame, root: Path
) -> None:
    out = root / "outputs/figures"
    correlation = frame[columns].corr(method="spearman")
    fig, ax = plt.subplots(figsize=(12, 10))
    im = ax.imshow(correlation, vmin=-1, vmax=1, cmap="RdBu_r")
    ax.set_xticks(range(len(columns)), columns, rotation=90, fontsize=6)
    ax.set_yticks(range(len(columns)), columns, fontsize=6)
    fig.colorbar(im, ax=ax, label="Spearman correlation")
    save(fig, out / "feature_correlations")
    pca = PCA(n_components=min(len(matrix), matrix.shape[1], 10))
    components = pca.fit_transform(matrix)
    coordinates = pd.DataFrame(
        components, columns=[f"PC{i + 1}" for i in range(components.shape[1])]
    )
    coordinates.insert(0, "sector", frame.sector.to_numpy())
    coordinates.insert(0, "tic_id", frame.tic_id.to_numpy())
    coordinates.to_csv(root / "outputs/tables/pca_coordinates.csv", index=False)
    pd.DataFrame(pca.components_, columns=columns).to_csv(
        root / "outputs/tables/pca_loadings.csv", index=False
    )
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(
        np.arange(1, len(pca.explained_variance_ratio_) + 1), pca.explained_variance_ratio_, "o-"
    )
    ax.set(xlabel="Principal component", ylabel="Explained variance fraction", ylim=(0, 1))
    save(fig, out / "pca_explained_variance")
    if components.shape[1] >= 2:
        fig, ax = plt.subplots(figsize=(7, 5))
        markers = {"planet": "o", "false_positive": "x", "background": "^", "ambiguous": "s"}
        colors = frame.ensemble_score if "ensemble_score" in frame else frame.depth_snr
        for label, indices in frame.groupby("label").groups.items():
            idx = frame.index.get_indexer(indices)
            im = ax.scatter(
                components[idx, 0],
                components[idx, 1],
                c=colors.iloc[idx],
                vmin=colors.min(),
                vmax=colors.max(),
                marker=markers.get(label, "s"),
                cmap="viridis",
                label=label,
                alpha=0.8,
            )
        fig.colorbar(im, ax=ax, label="Ensemble anomaly percentile")
        ax.set(xlabel="PC1 [scaled feature units]", ylabel="PC2 [scaled feature units]")
        ax.legend()
        save(fig, out / "pca_projection")
    for score in score_columns(frame):
        fig, ax = plt.subplots(figsize=(7, 4))
        for label, group in frame.groupby("label"):
            ax.hist(group[score].dropna(), bins="auto", histtype="step", linewidth=1.5, label=label)
        ax.set(xlabel=score.replace("_", " "), ylabel="Target-sector count")
        ax.legend()
        save(fig, out / f"distribution_{score}")
    if "ensemble_score" in frame:
        fig, ax = plt.subplots(figsize=(6, 5))
        for label, group in frame.groupby("label"):
            ax.scatter(group.depth_snr, group.ensemble_score, s=15, label=label, alpha=0.7)
        ax.set(xlabel="BLS depth SNR", ylabel="Ensemble anomaly percentile")
        ax.legend()
        save(fig, out / "bls_vs_anomaly")
        targets = target_scores(frame)
        fig, ax = plt.subplots(figsize=(6, 5))
        x = targets.depth_snr.rank(ascending=False)
        for method in ["ensemble_score", "hybrid_score"]:
            ax.scatter(x, targets[method].rank(ascending=False), s=12, alpha=0.6, label=method)
        ax.plot([1, len(targets)], [1, len(targets)], color="grey", ls="--", lw=0.8)
        ax.set(
            xlabel="BLS depth-SNR target rank (1 = highest)",
            ylabel="Alternative target rank (1 = highest)",
        )
        ax.legend()
        save(fig, out / "bls_anomaly_hybrid_rank_comparison")
    for metric in ["precision_at_k", "recall_at_k"]:
        fig, ax = plt.subplots(figsize=(8, 5))
        for method, group in metrics.groupby("method"):
            group = group.drop_duplicates("k").sort_values("k")
            ax.plot(group.k, group[metric], "o-", label=method)
        ax.set(xlabel="Top K unique targets", ylabel=metric.replace("_", " "), ylim=(0, 1.02))
        ax.legend(fontsize=8)
        save(fig, out / metric)
