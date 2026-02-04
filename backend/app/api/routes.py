from fastapi import APIRouter

from app.api.health import router as health_router
from app.api.metadata import router as metadata_router
from app.api.prices import router as prices_router
from app.api.anomalies import router as anomalies_router


def get_api_router() -> APIRouter:
    router = APIRouter()
    router.include_router(health_router)
    router.include_router(metadata_router)
    router.include_router(prices_router)
    router.include_router(anomalies_router)
    return router
