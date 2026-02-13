from __future__ import annotations

import pandas as pd
from app.services.rosstat_ingestion import fetch_with_fallback


def load_prices_from_csv(path: str) -> pd.DataFrame:
    """
    Load pre-filtered price data from CSV.
    
    CSV contains data fetched from Rosstat API and filtered to:
    - Selected food commodities from Rosstat database
    - 5 cities (Moscow, St Petersburg, Novosibirsk, Yekaterinburg, Kazan)
    
    See rosstat_ingestion.py for data fetching and filtering logic.
    """
    df = fetch_with_fallback(path)
    df["price"] = df["price"].astype(float)
    return df
