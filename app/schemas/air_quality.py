import math
from typing import Optional
from pydantic import BaseModel, Field, PositiveInt, model_validator


class AirQualityBase(BaseModel):
    """
    Base schema for air quality data.
    Used for:
    - Common data fields in various requests and responses.
    """

    year: PositiveInt = Field(..., example=2023)
    latitude: float = Field(..., example=37.7749)
    longitude: float = Field(..., example=-122.4194)
    pm25_level: Optional[float] = Field(None, example=12.5)

    @model_validator(mode="before")
    def check_nan_values(cls, values):
        # Check if pm25_level is NaN and replace it with None
        pm25_level = values.pm25_level
        if pm25_level is not None and math.isnan(pm25_level):
            values.pm25_level = None
        return values


class AirQualityCreate(BaseModel):
    """
    Schema for creating a new air quality data entry.
    Used for:
    - POST /data
    """

    year: PositiveInt = Field(..., example=2023)
    latitude: float = Field(..., example=37.7749)
    longitude: float = Field(..., example=-122.4194)
    pm25_level: Optional[float] = Field(None, example=12.5)

    @model_validator(mode="before")
    def check_nan_values(cls, values):
        # Check if pm25_level is NaN and replace it with None
        pm25_level = values["pm25_level"]
        if pm25_level is not None and math.isnan(pm25_level):
            values["pm25_level"] = None
        return values

    class Config:
        from_attributes = True


class AirQualityUpdate(BaseModel):
    """
    Schema for updating an existing air quality data entry.
    Used for:
    - PUT /data/:id
    """

    year: Optional[PositiveInt] = Field(None, example=2023)
    latitude: Optional[float] = Field(None, example=37.7749)
    longitude: Optional[float] = Field(None, example=-122.4194)
    pm25_level: Optional[float] = Field(None, example=12.5)

    @model_validator(mode="before")
    def check_nan_values(cls, values):
        # Check if pm25_level is NaN and replace it with None
        pm25_level = values["pm25_level"]
        if pm25_level is not None and math.isnan(pm25_level):
            values["pm25_level"] = None
        return values

    class Config:
        from_attributes = True


class AirQualityResponse(AirQualityBase):
    """
    Schema for the response model when retrieving air quality data.
    Used for:
    - GET /data
    - GET /data/:id
    """

    id: int

    class Config:
        from_attributes = True


class AirQualityStats(BaseModel):
    """
    Schema for representing statistics of air quality data.
    Used for:
    - GET /data/stats
    """

    count: int
    average_pm25: Optional[float] = Field(None)
    min_pm25: Optional[float] = Field(None)
    max_pm25: Optional[float] = Field(None)

    @model_validator(mode="before")
    def check_nan_values(cls, values):
        # Check if pm25_level is NaN and replace it with None
        average_pm25 = values["average_pm25"]
        min_pm25 = values["min_pm25"]
        max_pm25 = values["max_pm25"]
        if average_pm25 is not None and math.isnan(average_pm25):
            values["average_pm25"] = None
        if min_pm25 is not None and math.isnan(min_pm25):
            values["min_pm25"] = None
        if max_pm25 is not None and math.isnan(max_pm25):
            values["max_pm25"] = None
        return values

    class Config:
        from_attributes = True


class AirQualityNormalized(BaseModel):
    """
    Schema for representing normalized air quality data.
    Used for:
    - (To be used for a future endpoint handling normalization of PM2.5 data)
    """

    id: int
    year: int
    latitude: float
    longitude: float
    pm25_level_normalized: Optional[float] = Field(None)

    @model_validator(mode="before")
    def check_nan_values(cls, values):
        # Check if pm25_level is NaN and replace it with None
        pm25_level_normalized = values["pm25_level_normalized"]
        if pm25_level_normalized is not None and math.isnan(pm25_level_normalized):
            values["pm25_level_normalized"] = None
        return values


class TopPollutedLocation(AirQualityBase):
    """
    Schema for representing the top polluted locations.
    Used for:
    - GET /data/top-polluted?year=:year
    """

    class Config:
        from_attributes = True
