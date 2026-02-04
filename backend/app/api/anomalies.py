from __future__ import annotations

from fastapi import APIRouter, Query

from app.models.schemas import AnomalyResponse
from app.services.anomaly import detect_anomalies
from app.services.storage import store

router = APIRouter(prefix="/anomalies")


@router.get("", response_model=AnomalyResponse)
def get_anomalies(
    commodity: str = Query(...),
    region: str = Query(...),
    window: int = Query(12, ge=3, le=52),
    z: float = Query(2.0, ge=1.0, le=5.0),
) -> AnomalyResponse:
    if store.prices is None:
        return AnomalyResponse(
            region=region,
            commodity=commodity,
            window=window,
            threshold=z,
            points=[],
        )

    df = store.prices
    filtered = df[(df["commodity"] == commodity) & (df["region"] == region)]
    anomalies = detect_anomalies(filtered[["date", "price"]], window=window, z_threshold=z)

    points = [
        {
            "date": row.date.date(),
            "price": float(row.price),
            "z_score": float(row.z_score),
        }
        for row in anomalies.itertuples()
    ]

    return AnomalyResponse(
        region=region,
        commodity=commodity,
        window=window,
        threshold=z,
        points=points,
    )
