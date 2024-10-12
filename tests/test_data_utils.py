import pytest
import pandas as pd
from pathlib import Path

from notebooks.data_utils import get_netcdf_file, process_netcdf_file


def test_get_netcdf_file_valid():
    data_dir = Path("./data")
    year = 1998
    expected_path = (
        data_dir
        / "sdei-global-annual-gwr-pm2-5-modis-misr-seawifs-viirs-aod-v5-gl-04-1998-netcdf"
        / "sdei-global-annual-gwr-pm2-5-modis-misr-seawifs-viirs-aod-v5-gl-04-1998-netcdf.nc"
    )

    result = get_netcdf_file(data_dir, year)
    assert result == expected_path


def test_get_netcdf_file_invalid_year():
    data_dir = Path("./data")
    year = 2050

    result = get_netcdf_file(data_dir, year)
    assert result is None


def test_process_netcdf_file_valid():
    file_path = Path(
        "./data/sdei-global-annual-gwr-pm2-5-modis-misr-seawifs-viirs-aod-v5-gl-04-1998-netcdf/sdei-global-annual-gwr-pm2-5-modis-misr-seawifs-viirs-aod-v5-gl-04-1998-netcdf.nc"
    )
    year = 1998

    df = process_netcdf_file(str(file_path), year)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "year" in df.columns
    assert "latitude" in df.columns
    assert "longitude" in df.columns
    assert "pm25_level" in df.columns


def test_process_netcdf_file_missing_variable():
    file_path = Path("./data/missing_pm25.nc")
    year = 1999

    df = process_netcdf_file(str(file_path), year)
    assert df is None
