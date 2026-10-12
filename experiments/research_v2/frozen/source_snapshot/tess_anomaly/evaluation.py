"""Descriptive ranking evaluation; unknown background is not a binary negative."""

import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, spearmanr
from sklearn.metrics import average_precision_score, roc_auc_score


def score_columns(frame: pd.DataFrame) -> list[str]:
    return [
        c
        for c in [
            "bls_max_power",
            "depth_snr",
            "isolation_forest_score",
            "lof_score",
            "autoencoder_score",
            "ensemble_score",
            "hybrid_score",
        ]
        if c in frame
    ]


def target_scores(frame: pd.DataFrame) -> pd.DataFrame:
    """Max score per TIC avoids counting repeated sectors as independent targets.

    Different methods may choose different sectors. More observed sectors increase
    opportunities for high scores; sector counts must be checked as a confounder.
    """
    cols = score_columns(frame)
    metadata = frame.groupby("tic_id").agg(
        label=("label", "first"),
        disposition=("disposition", "first"),
        n_sectors=("sector", "nunique"),
    )
    return metadata.join(frame.groupby("tic_id")[cols].max()).reset_index()


def ranking_metrics(frame: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """Precision is catalogue-positive yield, not true planet purity."""
    rows = []
    for method in score_columns(frame):
        valid = frame[np.isfinite(frame[method])].copy()
        valid = valid.sort_values([method, "tic_id"], ascending=[False, True], kind="stable")
        n = len(valid)
        positive = valid.label.eq("planet").to_numpy()
        total = int(positive.sum())
        ks = sorted(set(cfg["top_k"] + [max(1, int(np.ceil(n * f))) for f in cfg["top_fractions"]]))
        ranks = np.flatnonzero(positive) + 1
        reliable = valid.label.eq("false_positive") | (
            valid.label.eq("planet")
            & valid.disposition.str.split(";").apply(lambda ds: bool(set(ds) & {"CP", "KP"}))
        )
        binary = valid[reliable]
        y = binary.label.eq("planet").astype(int)
        auc = roc_auc_score(y, binary[method]) if y.nunique() == 2 else np.nan
        ap = average_precision_score(y, binary[method]) if y.nunique() == 2 else np.nan
        reason = (
            ""
            if y.nunique() == 2
            else "Not calculated because confirmed/known planets and false positives are not both present"
        )
        for requested in ks:
            k = min(requested, n)
            recovered = int(positive[:k].sum())
            rows.append(
                dict(
                    method=method,
                    requested_k=requested,
                    k=k,
                    n=n,
                    positive_total=total,
                    recovered=recovered,
                    precision_at_k=recovered / k if k else np.nan,
                    recall_at_k=recovered / total if total else np.nan,
                    mean_positive_rank=float(np.mean(ranks)) if total else np.nan,
                    median_positive_rank=float(np.median(ranks)) if total else np.nan,
                    roc_auc=auc,
                    average_precision=ap,
                    binary_n=len(binary),
                    metric_note=reason or "Confirmed/known planets versus catalogue FP/FA only",
                    recall_note=""
                    if total
                    else "Not calculated because no catalogue-positive targets are present",
                )
            )
    return pd.DataFrame(rows)


def correlations(frame: pd.DataFrame, columns: list[str], scores: list[str]) -> pd.DataFrame:
    rows = []
    for feature in columns:
        for score in scores:
            pair = (
                frame[[feature, score]].replace([np.inf, -np.inf], np.nan).dropna()
                if feature != score
                else None
            )
            if pair is not None and len(pair) >= 3 and (pair.nunique() > 1).all():
                rho, p = spearmanr(pair.iloc[:, 0], pair.iloc[:, 1])
                rows.append(
                    dict(feature=feature, score=score, n=len(pair), spearman_rho=rho, p_value=p)
                )
    return pd.DataFrame(rows, columns=["feature", "score", "n", "spearman_rho", "p_value"])


def group_statistics(frame: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for score in score_columns(frame):
        for group, subset in frame.groupby("label"):
            values = subset[score].dropna()
            other = frame.loc[frame.label != group, score].dropna()
            p = (
                mannwhitneyu(values, other, alternative="two-sided").pvalue
                if len(values) and len(other)
                else np.nan
            )
            rows.append(
                dict(
                    method=score,
                    label=group,
                    n=len(values),
                    median=values.median(),
                    q25=values.quantile(0.25),
                    q75=values.quantile(0.75),
                    mann_whitney_p_vs_rest=p,
                )
            )
    return pd.DataFrame(rows)
