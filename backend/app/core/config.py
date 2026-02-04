from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = "Food Price Anomaly Tracker"
    api_prefix: str = "/api"
    data_path: str = os.getenv("DATA_PATH", "app/data/sample_prices.csv")
    allow_origins: tuple[str, ...] = ("*",)


def get_settings() -> Settings:
    return Settings()
