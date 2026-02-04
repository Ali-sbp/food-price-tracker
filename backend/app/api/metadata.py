from __future__ import annotations

from fastapi import APIRouter

from app.models.schemas import CommodityList, RegionList, DashboardSummary
from app.services.storage import store

router = APIRouter()


@router.get("/commodities", response_model=CommodityList)
def list_commodities() -> CommodityList:
    if store.prices is None:
        return CommodityList(items=[])
    items = sorted(store.prices["commodity"].unique().tolist())
    return CommodityList(items=items)


@router.get("/regions", response_model=RegionList)
def list_regions() -> RegionList:
    if store.prices is None:
        return RegionList(items=[])
    items = sorted(store.prices["region"].unique().tolist())
    return RegionList(items=items)


@router.get("/summary", response_model=DashboardSummary)
def dashboard_summary() -> DashboardSummary:
    if store.prices is None or store.prices.empty:
        return DashboardSummary(cards=[])

    latest_date = store.prices["date"].max().date()
    commodity_count = store.prices["commodity"].nunique()
    region_count = store.prices["region"].nunique()
    return DashboardSummary(
        cards=[
            {"label": "Latest data", "value": str(latest_date)},
            {"label": "Commodities", "value": str(commodity_count)},
            {"label": "Regions", "value": str(region_count)},
        ]
    )
