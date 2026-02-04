from __future__ import annotations

from datetime import date
from pydantic import BaseModel, Field


class PriceRecord(BaseModel):
    date: date
    region: str
    commodity: str
    price: float
    unit: str


class PriceSeries(BaseModel):
    region: str
    commodity: str
    unit: str
    records: list[PriceRecord]


class AnomalyPoint(BaseModel):
    date: date
    price: float
    z_score: float = Field(..., description="Standard deviation from rolling mean")


class AnomalyResponse(BaseModel):
    region: str
    commodity: str
    window: int
    threshold: float
    points: list[AnomalyPoint]


class SummaryCard(BaseModel):
    label: str
    value: str


class DashboardSummary(BaseModel):
    cards: list[SummaryCard]


class CommodityList(BaseModel):
    items: list[str]


class RegionList(BaseModel):
    items: list[str]
