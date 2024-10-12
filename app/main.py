import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routers import air_quality
from app.schemas.settings import Settings
from app.db.database_manager import DatabaseManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Settings
    settings = Settings()
    logging.info("Settings loaded successfully.")

    # Initialize DatabaseManager and store in app state
    db_manager = DatabaseManager(database_url=settings.db_url)
    logging.info("DatabaseManager initialized.")

    # Store Settings and DatabaseManager in app state for global access
    app.state.settings = settings
    app.state.db_manager = db_manager

    try:
        yield
    finally:
        # Clean up resources here
        logging.info("Additional resources cleaned up.")


app = FastAPI(
    title="PM2.5 Air Quality API",
    description="An API to serve PM2.5 air quality data.",
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(air_quality.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Air Quality API"}


@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "API is running"}
