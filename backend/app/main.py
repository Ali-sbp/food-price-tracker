from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import get_api_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.services.ingestion import load_prices_from_csv
from app.services.normalization import normalize_prices
from app.services.storage import store


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging()

    application = FastAPI(title=settings.app_name)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.allow_origins),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(get_api_router(), prefix=settings.api_prefix)

    # Serve built frontend
    frontend_build = Path(__file__).parent.parent.parent / "frontend" / "dist"
    if frontend_build.exists():
        application.mount(
            "/",
            StaticFiles(directory=str(frontend_build), html=True),
            name="frontend"
        )

    @application.on_event("startup")
    def load_data() -> None:
        df = load_prices_from_csv(settings.data_path)
        store.prices = normalize_prices(df)

    return application


app = create_app()
application = app  # For uvicorn compatibility
