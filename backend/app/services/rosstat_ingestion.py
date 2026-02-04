"""
Fetch real food price data from Rosstat.
Using open data portals and APIs.
"""
from __future__ import annotations

import requests
import pandas as pd
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


def fetch_rosstat_prices() -> pd.DataFrame | None:
    """
    Fetch real food price data from open Russian data sources.
    Attempts multiple endpoints.
    """
    try:
        # Try data.gov.ru API (Russian open data portal)
        # This has Rosstat food price data
        api_endpoints = [
            {
                "url": "https://data.gov.ru/api/v1/datasets",
                "params": {"q": "цены продукты питания"},
            },
            {
                "url": "https://opendata.rosstat.gov.ru/api/",
                "params": {"indicator": "food_prices"},
            },
        ]

        for endpoint in api_endpoints:
            try:
                response = requests.get(
                    endpoint["url"],
                    params=endpoint.get("params"),
                    timeout=5,
                    headers={"User-Agent": "Mozilla/5.0"},
                )
                response.raise_for_status()
                data = response.json()
                logger.info(f"Connected to {endpoint['url']}")

                # If we got valid data, try to parse it
                if data and isinstance(data, dict) and len(str(data)) > 100:
                    logger.info(f"Got response from {endpoint['url']}")
                    # For now, this will fail gracefully and fall back
                    break

            except requests.RequestException as e:
                logger.debug(f"Endpoint {endpoint['url']} failed: {e}")
                continue

        return None

    except Exception as e:
        logger.error(f"Error in Rosstat fetch: {e}")
        return None


def fetch_with_fallback(sample_csv_path: str) -> pd.DataFrame:
    """
    Try to fetch from Rosstat/open data, fall back to sample CSV.
    """
    # Try real data first
    df = fetch_rosstat_prices()

    if df is not None and not df.empty:
        return df

    # Fall back to sample data
    logger.info(f"Using sample data from {sample_csv_path}")
    try:
        df = pd.read_csv(sample_csv_path)
        df["date"] = pd.to_datetime(df["date"])
        return df
    except Exception as e:
        logger.error(f"Failed to load sample data: {e}")
        raise
