from typing import Optional

from app.db.models.air_quality import AirQualityData
from app.schemas.air_quality import AirQualityNormalized
from app.repositories.air_quality_repository import AirQualityRepository


class AirQualityService:
    def __init__(self, repository: AirQualityRepository):
        self.repository = repository

    def get_all_data(self, skip: int = 0, limit: int = 100) -> list[AirQualityData]:
        return self.repository.get_all(skip=skip, limit=limit)

    def get_data_by_id(self, record_id: int) -> Optional[AirQualityData]:
        return self.repository.get_by_id(record_id)

    def create_data(self, data: AirQualityData) -> AirQualityData:
        return self.repository.create(data)

    def update_data(self, record_id: int, updates: dict) -> Optional[AirQualityData]:
        record = self.repository.get_by_id(record_id)
        return self.repository.update(record, updates) if record else None

    def delete_data(self, record_id: int) -> bool:
        record = self.repository.get_by_id(record_id)
        if not record:
            return False
        self.repository.delete(record)
        return True

    def filter_data(
        self,
        year: Optional[int] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
    ) -> list[AirQualityData]:
        return self.repository.filter(year=year, latitude=latitude, longitude=longitude)

    def get_statistics(self) -> dict:
        return self.repository.get_stats()

    def get_data_in_region(
        self, lat_min: float, lat_max: float, long_min: float, long_max: float
    ) -> list[AirQualityData]:
        return self.repository.get_data_within_region(
            lat_min=lat_min, lat_max=lat_max, long_min=long_min, long_max=long_max
        )

    def get_pm25_normalized(self) -> list[AirQualityNormalized]:
        normalized_data = self.repository.get_pm25_normalized()
        return [AirQualityNormalized(**record._mapping) for record in normalized_data]

    def get_top_polluted_locations(
        self, year: int, top_n: int = 10
    ) -> list[AirQualityData]:
        return self.repository.get_top_polluted_locations(year=year, top_n=top_n)
