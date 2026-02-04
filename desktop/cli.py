#!/usr/bin/env python3
"""
Food Price Anomaly Tracker - Headless CLI Mode
(When running headless or testing; use gui.py for GUI mode)
"""

import requests
from datetime import datetime
from tabulate import tabulate

API_URL = "http://localhost:8000/api"


def fetch_commodities():
    """Fetch list of commodities."""
    try:
        resp = requests.get(f"{API_URL}/commodities", timeout=5)
        resp.raise_for_status()
        return resp.json().get("items", [])
    except Exception as e:
        print(f"Error fetching commodities: {e}")
        return []


def fetch_regions():
    """Fetch list of regions."""
    try:
        resp = requests.get(f"{API_URL}/regions", timeout=5)
        resp.raise_for_status()
        return resp.json().get("items", [])
    except Exception as e:
        print(f"Error fetching regions: {e}")
        return []


def fetch_prices(commodity, region):
    """Fetch prices for a commodity in a region."""
    try:
        resp = requests.get(
            f"{API_URL}/prices",
            params={"commodity": commodity, "region": region},
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json().get("records", [])
    except Exception as e:
        print(f"Error fetching prices: {e}")
        return []


def fetch_anomalies(commodity, region, window=12, z=2.0):
    """Fetch anomalies for a commodity in a region."""
    try:
        resp = requests.get(
            f"{API_URL}/anomalies",
            params={
                "commodity": commodity,
                "region": region,
                "window": window,
                "z": z,
            },
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json().get("points", [])
    except Exception as e:
        print(f"Error fetching anomalies: {e}")
        return []


def main():
    print("=" * 60)
    print("Food Price Anomaly Tracker - CLI")
    print("=" * 60)

    commodities = fetch_commodities()
    regions = fetch_regions()

    if not commodities or not regions:
        print("Error: Could not fetch commodities or regions.")
        print("Ensure backend is running at http://localhost:8000")
        return

    print(f"\nAvailable commodities: {', '.join(commodities)}")
    print(f"Available regions: {', '.join(regions)}")

    # Example: Show prices and anomalies for Moscow, Bread
    commodity = "Bread"
    region = "Moscow"

    print(f"\n--- {commodity} in {region} ---")

    prices = fetch_prices(commodity, region)
    if prices:
        print("\nPrice History:")
        print(tabulate(prices, headers="keys", tablefmt="grid"))

    anomalies = fetch_anomalies(commodity, region, window=12, z=2.0)
    if anomalies:
        print("\nDetected Anomalies (z > 2.0):")
        print(tabulate(anomalies, headers="keys", tablefmt="grid"))
    else:
        print("\nNo anomalies detected.")


if __name__ == "__main__":
    main()
