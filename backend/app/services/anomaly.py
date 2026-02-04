from __future__ import annotations

import pandas as pd


def detect_anomalies(
    df: pd.DataFrame,
    window: int = 12,
    z_threshold: float = 2.0,
) -> pd.DataFrame:
    """Return rows where rolling z-score exceeds threshold.

    Expects columns: date, price.
    """
    if df.empty:
        return df

    df = df.sort_values("date").copy()
    rolling_mean = df["price"].rolling(window=window, min_periods=max(3, window // 2)).mean()
    rolling_std = df["price"].rolling(window=window, min_periods=max(3, window // 2)).std()

    df["z_score"] = (df["price"] - rolling_mean) / rolling_std
    df = df[df["z_score"].abs() >= z_threshold]
    return df
