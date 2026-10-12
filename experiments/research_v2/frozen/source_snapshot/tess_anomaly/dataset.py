"""Training-only missingness selection, imputation and scaling."""

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler, StandardScaler

from .features import FAMILIES


@dataclass
class FeatureTransform:
    """Serializable feature contract for training and subsequent scoring."""

    columns: list[str]
    pipeline: Pipeline
    missingness: pd.DataFrame

    def transform(self, frame: pd.DataFrame) -> np.ndarray:
        return self.pipeline.transform(
            frame.reindex(columns=self.columns).replace([np.inf, -np.inf], np.nan)
        )


def fit_transform(
    frame: pd.DataFrame, cfg: dict, family: str = "all", columns: list[str] | None = None
) -> tuple[FeatureTransform, np.ndarray]:
    """Identifiers, dispositions, catalogue periods and sector are never features."""
    values = frame.reindex(columns=FAMILIES[family] if columns is None else columns).replace(
        [np.inf, -np.inf], np.nan
    )
    missing = values.isna().mean()
    keep = (missing <= cfg["max_missing_fraction"]) & (values.nunique() > 1)
    catalogue_proxy = values.columns.isin(["radius_earth_proxy", "duration_ratio_proxy"])
    if not cfg.get("use_stellar_catalog_features", False):
        keep &= ~catalogue_proxy
    columns = values.columns[keep].tolist()
    redundant = {}
    threshold = cfg.get("correlation_threshold")
    if threshold is not None:
        if not 0 < threshold <= 1:
            raise ValueError("correlation_threshold must be in (0, 1]")
        corr = values[columns].corr(method="spearman", min_periods=20).abs()
        retained = []
        for column in columns:
            partners = [c for c in retained if corr.loc[c, column] >= threshold]
            if partners:
                redundant[column] = partners[0]
            else:
                retained.append(column)
        columns = retained
        keep &= values.columns.isin(columns)
    report = pd.DataFrame(
        {
            "feature": values.columns,
            "missing_fraction": missing.values,
            "selected": keep.values,
            "redundant_with": [redundant.get(c, "") for c in values.columns],
            "catalogue_proxy_disabled": catalogue_proxy
            & (not cfg.get("use_stellar_catalog_features", False)),
        }
    )
    if not columns:
        raise ValueError(f"No nonconstant, sufficiently measured features in {family}")
    scaler = RobustScaler() if cfg["scaler"] == "robust" else StandardScaler()
    pipe = Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", scaler)])
    matrix = pipe.fit_transform(values[columns])
    return FeatureTransform(columns, pipe, report), matrix
