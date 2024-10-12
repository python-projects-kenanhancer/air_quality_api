from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.db.models.air_quality import AirQualityData


class AirQualityRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[AirQualityData]:
        return self.db.query(AirQualityData).offset(skip).limit(limit).all()

    def get_by_id(self, record_id: int) -> Optional[AirQualityData]:
        return (
            self.db.query(AirQualityData).filter(AirQualityData.id == record_id).first()
        )

    def create(self, data: AirQualityData) -> AirQualityData:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    def update(self, record: AirQualityData, updates: dict) -> AirQualityData:
        for key, value in updates.items():
            setattr(record, key, value)
        self.db.commit()
        self.db.refresh(record)
        return record

    def delete(self, record: AirQualityData) -> None:
        self.db.delete(record)
        self.db.commit()

    def filter(
        self,
        year: Optional[int] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
    ) -> list[AirQualityData]:
        query = self.db.query(AirQualityData)
        if year is not None:
            query = query.filter(AirQualityData.year == year)
        if latitude is not None:
            query = query.filter(AirQualityData.latitude == latitude)
        if longitude is not None:
            query = query.filter(AirQualityData.longitude == longitude)
        return query.all()

    def get_stats(self) -> dict:
        stats = self.db.query(
            func.count(AirQualityData.id),
            func.avg(AirQualityData.pm25_level),
            func.min(AirQualityData.pm25_level),
            func.max(AirQualityData.pm25_level),
        ).first()
        return {
            "count": stats[0],
            "average_pm25": float(stats[1]) if stats[1] is not None else 0.0,
            "min_pm25": float(stats[2]) if stats[2] is not None else 0.0,
            "max_pm25": float(stats[3]) if stats[3] is not None else 0.0,
        }

    def get_data_within_region(
        self, lat_min: float, lat_max: float, long_min: float, long_max: float
    ) -> list[AirQualityData]:
        return (
            self.db.query(AirQualityData)
            .filter(
                AirQualityData.latitude.between(lat_min, lat_max),
                AirQualityData.longitude.between(long_min, long_max),
            )
            .all()
        )

    def get_top_polluted_locations(
        self, year: int, top_n: int = 10
    ) -> list[AirQualityData]:
        return (
            self.db.query(AirQualityData)
            .filter(AirQualityData.year == year)
            .order_by(desc(AirQualityData.pm25_level))
            .limit(top_n)
            .all()
        )

    def get_pm25_normalized(self) -> list[AirQualityData]:
        # To normalize PM2.5 levels between 0 and 1
        min_pm25 = self.db.query(func.min(AirQualityData.pm25_level)).scalar()
        max_pm25 = self.db.query(func.max(AirQualityData.pm25_level)).scalar()
        if min_pm25 is None or max_pm25 is None or max_pm25 == min_pm25:
            return []
        normalized_data = self.db.query(
            AirQualityData.id,
            AirQualityData.year,
            AirQualityData.latitude,
            AirQualityData.longitude,
            ((AirQualityData.pm25_level - min_pm25) / (max_pm25 - min_pm25)).label(
                "pm25_level_normalized"
            ),
        ).all()
        return normalized_data
