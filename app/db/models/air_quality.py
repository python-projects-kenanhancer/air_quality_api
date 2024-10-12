from sqlalchemy import Column, Integer, Float
from app.db.database_manager import Base


class AirQualityData(Base):
    __tablename__ = "air_quality_data"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, index=True, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    pm25_level = Column(Float, nullable=True)

    def __repr__(self):
        return (
            f"<AirQualityData(id={self.id}, year={self.year}, "
            f"latitude={self.latitude}, longitude={self.longitude}, "
            f"pm25_level={self.pm25_level})>"
        )
