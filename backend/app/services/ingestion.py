from __future__ import annotations

import pandas as pd
from app.services.rosstat_ingestion import fetch_with_fallback


def load_prices_from_csv(path: str) -> pd.DataFrame:
    """Load prices, attempting Rosstat API first, falling back to CSV."""
    df = fetch_with_fallback(path)
    df["price"] = df["price"].astype(float)
    return df
