from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from app.schemas.air_quality import (
    AirQualityCreate,
    AirQualityResponse,
    AirQualityUpdate,
    AirQualityStats,
    TopPollutedLocation,
)
from app.dependencies import get_air_quality_service
from app.db.models.air_quality import AirQualityData
from app.services.air_quality_service import AirQualityService

router = APIRouter(
    prefix="/data",
    tags=["Air Quality Data"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[AirQualityResponse])
def read_all_data(
    skip: int = 0,
    limit: int = 100,
    service: AirQualityService = Depends(get_air_quality_service),
):
    """
    Retrieve all available air quality data.
    """
    data: list[AirQualityData] = service.get_all_data(skip=skip, limit=limit)

    return data


@router.post("/", response_model=AirQualityResponse, status_code=201)
def create_data(
    record: AirQualityCreate,
    service: AirQualityService = Depends(get_air_quality_service),
):
    """
    Add a new air quality data entry.
    """
    db_record = AirQualityData(**record.model_dump())
    created_record: AirQualityData = service.create_data(db_record)
    return created_record


@router.put("/{record_id}", response_model=AirQualityResponse)
def update_data(
    record_id: int,
    updates: AirQualityUpdate,
    service: AirQualityService = Depends(get_air_quality_service),
):
    """
    Update an existing air quality data entry.
    """
    updated_data = updates.model_dump(exclude_unset=True)
    updated_record = service.update_data(record_id, updated_data)
    if not updated_record:
        raise HTTPException(status_code=404, detail="Record not found")
    return updated_record


@router.delete("/{record_id}", response_model=dict)
def delete_data(
    record_id: int, service: AirQualityService = Depends(get_air_quality_service)
):
    """
    Delete an air quality data entry.
    """
    success = service.delete_data(record_id)
    if not success:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"detail": "Record deleted successfully"}


@router.get("/stats", response_model=AirQualityStats)
def get_statistics(service: AirQualityService = Depends(get_air_quality_service)):
    """
    Provide basic statistics (count, average PM2.5, min, max) across the dataset.
    """
    stats = service.get_statistics()
    return stats


@router.get("/region", response_model=list[AirQualityResponse])
def get_data_in_region(
    lat_min: float = Query(..., ge=-90, le=90, description="Minimum latitude"),
    lat_max: float = Query(..., ge=-90, le=90, description="Maximum latitude"),
    long_min: float = Query(..., ge=-180, le=180, description="Minimum longitude"),
    long_max: float = Query(..., ge=-180, le=180, description="Maximum longitude"),
    service: AirQualityService = Depends(get_air_quality_service),
):
    """
    Retrieve data within a bounding box (defined by latitude/longitude).
    """
    if lat_min > lat_max:
        raise HTTPException(
            status_code=400, detail="lat_min cannot be greater than lat_max"
        )
    if long_min > long_max:
        raise HTTPException(
            status_code=400, detail="long_min cannot be greater than long_max"
        )

    data = service.get_data_in_region(
        lat_min=lat_min, lat_max=lat_max, long_min=long_min, long_max=long_max
    )
    return data


@router.get("/top10", response_model=list[TopPollutedLocation])
def get_top_polluted_locations(
    year: int = Query(..., ge=1900, le=2100, description="Year to filter data"),
    service: AirQualityService = Depends(get_air_quality_service),
):
    """
    Return the top 10 most polluted locations in the dataset for a given year.
    """
    top_locations = service.get_top_polluted_locations(year=year, top_n=10)
    if not top_locations:
        raise HTTPException(
            status_code=404, detail="No records found for the specified year"
        )
    return top_locations


@router.get("/filter", response_model=list[AirQualityResponse])
def filter_data(
    year: Optional[int] = Query(None, ge=1900, le=2100, description="Filter by year"),
    lat: Optional[float] = Query(None, ge=-90, le=90, description="Filter by latitude"),
    long: Optional[float] = Query(
        None, ge=-180, le=180, description="Filter by longitude"
    ),
    service: AirQualityService = Depends(get_air_quality_service),
):
    """
    Filter the dataset based on year, latitude, and longitude.
    """
    data = service.filter_data(year=year, latitude=lat, longitude=long)
    return data


@router.get("/{record_id}", response_model=AirQualityResponse)
def read_data_by_id(
    record_id: int, service: AirQualityService = Depends(get_air_quality_service)
):
    """
    Fetch a specific data entry by ID.
    """
    data: AirQualityData | None = service.get_data_by_id(record_id)
    if not data:
        raise HTTPException(status_code=404, detail="Record not found")
    return data
