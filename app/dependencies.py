import logging
from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.db.database_manager import DatabaseManager
from app.schemas.settings import Settings
from app.services.air_quality_service import AirQualityService
from app.repositories.air_quality_repository import AirQualityRepository

# Configure logger (ensure consistency with your main logger configuration)
logger = logging.getLogger("data_processing_pipeline_development")


def get_settings(request: Request) -> Settings:
    settings: Settings = getattr(request.app.state, "settings", None)
    if not settings:
        logger.error("Settings instance not found in app state.")
        raise RuntimeError("Settings not initialized.")
    return settings


def get_db_manager(request: Request) -> DatabaseManager:
    db_manager: DatabaseManager = getattr(request.app.state, "db_manager", None)
    if not db_manager:
        logger.error("DatabaseManager instance not found in app state.")
        raise RuntimeError("DatabaseManager not initialized.")
    return db_manager


def get_db_session(db_manager: DatabaseManager = Depends(get_db_manager)) -> Session:
    with db_manager.get_db() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Error during database session: {e}")
            raise
        finally:
            pass  # Session is automatically closed by the context manager


def get_air_quality_repository(
    db: Session = Depends(get_db_session),
) -> AirQualityRepository:
    return AirQualityRepository(db)


def get_air_quality_service(
    repository: AirQualityRepository = Depends(get_air_quality_repository),
) -> AirQualityService:
    return AirQualityService(repository)
