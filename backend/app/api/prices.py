from __future__ import annotations

from datetime import datetime, timedelta
from fastapi import APIRouter, Query
import pandas as pd

from app.models.schemas import PriceSeries
from app.services.storage import store

router = APIRouter(prefix="/prices")


@router.get("", response_model=PriceSeries)
def get_prices(
    commodity: str = Query(...),
    region: str = Query(...),
    window: int = Query(None, description="Last N months to retrieve (None = all)"),
) -> PriceSeries:
    if store.prices is None:
        return PriceSeries(region=region, commodity=commodity, unit="", records=[])

    df = store.prices
    filtered = df[(df["commodity"] == commodity) & (df["region"] == region)]
    
    # Apply time window filter if specified
    if window is not None and window > 0 and not filtered.empty:
        # Convert to datetime if needed
        filtered_copy = filtered.copy()
        filtered_copy["date"] = pd.to_datetime(filtered_copy["date"])
        
        # Get the max date in data and calculate cutoff from there
        max_date = filtered_copy["date"].max()
        cutoff_date = max_date - timedelta(days=window * 30)
        filtered = filtered_copy[filtered_copy["date"] >= cutoff_date]
    
    if filtered.empty:
        return PriceSeries(region=region, commodity=commodity, unit="", records=[])

    unit = filtered["unit"].iloc[0]
    records = [
        {
            "date": row.date.date() if hasattr(row.date, 'date') else row.date,
            "region": row.region,
            "commodity": row.commodity,
            "price": float(row.price),
            "unit": row.unit,
        }
        for row in filtered.itertuples()
    ]

    return PriceSeries(region=region, commodity=commodity, unit=unit, records=records)
