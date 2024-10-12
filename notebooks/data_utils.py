import logging
from pathlib import Path
import pandas as pd
import numpy as np
from netCDF4 import Dataset

logger = logging.getLogger(__name__)


# @log_operation_decorator("Locate netCDF File")
def get_netcdf_file(data_dir: Path, year: int):
    logger.debug(
        f"Searching for directories matching pattern '*-{year}-netcdf' in {data_dir}"
    )

    # Define the pattern to match directories for the given year
    pattern = f"*-{year}-netcdf"

    # Search for directories matching the pattern
    matched_dirs = list(data_dir.glob(pattern))

    if not matched_dirs:
        logger.error(f"No directory found for year {year} ending with '-netcdf'.")
        return None

    # Handle multiple matched directories (if any)
    if len(matched_dirs) > 1:
        logger.warning(
            f"Multiple directories found for year {year} ending with '-netcdf'. "
            f"Using the first match: {matched_dirs[0]}"
        )

    # Select the first matched directory
    netcdf_dir = matched_dirs[0]
    logger.debug(f"Selected directory: {netcdf_dir}")

    # Search for .nc files within the matched directory
    nc_files = list(netcdf_dir.glob("*.nc"))

    if not nc_files:
        logger.error(f"No .nc file found in directory {netcdf_dir}.")
        return None

    # Handle multiple .nc files (if any)
    if len(nc_files) > 1:
        logger.warning(
            f"Multiple .nc files found in directory {netcdf_dir}. "
            f"Using the first file: {nc_files[0]}"
        )

    # Return the first .nc file found
    netcdf_file = nc_files[0]
    logger.info(f"NetCDF file for year {year} located at: {netcdf_file}")
    return netcdf_file


# @log_operation_decorator("Process netCDF File")
def process_netcdf_file(file_path: str, year: int):
    logger.debug(f"Opening netCDF file: {file_path}")

    try:
        with Dataset(file_path, "r") as ds:
            # Correct variable name for PM2.5 data
            pm25_var = "GWRPM25"
            if pm25_var not in ds.variables:
                logger.error(f"Variable '{pm25_var}' not found in {file_path}.")
                logger.debug(f"Available variables: {list(ds.variables.keys())}")
                return None

            # Correct variable names for coordinates
            lat_var = "lat"
            lon_var = "lon"

            if lat_var not in ds.variables:
                logger.error(f"Variable '{lat_var}' not found in {file_path}.")
                logger.debug(f"Available variables: {list(ds.variables.keys())}")
                return None

            if lon_var not in ds.variables:
                logger.error(f"Variable '{lon_var}' not found in {file_path}.")
                logger.debug(f"Available variables: {list(ds.variables.keys())}")
                return None

            # Extract data
            pm25 = ds.variables[pm25_var][:]
            lat = ds.variables[lat_var][:]
            lon = ds.variables[lon_var][:]

            logger.debug(f"PM2.5 data shape: {pm25.shape}")
            logger.debug(f"Latitude data shape: {lat.shape}")
            logger.debug(f"Longitude data shape: {lon.shape}")

            # Create meshgrid for latitude and longitude
            lon_grid, lat_grid = np.meshgrid(lon, lat)

            # Flatten the arrays
            lat_flat = lat_grid.flatten()
            lon_flat = lon_grid.flatten()
            pm25_flat = pm25.flatten()

            logger.debug(
                f"Flattened data lengths - Latitude: {len(lat_flat)}, Longitude: {len(lon_flat)}, PM2.5: {len(pm25_flat)}"
            )

            # Create DataFrame
            df = pd.DataFrame(
                {
                    "year": year,
                    "latitude": lat_flat,
                    "longitude": lon_flat,
                    "pm25_level": pm25_flat,
                }
            )

            logger.info(f"DataFrame created with {df.shape[0]} records.")
            return df

    except Exception as e:
        logger.exception(f"Error processing file {file_path}: {e}")
        return None


def save_processed_data_to_parquet(df: pd.DataFrame, output_dir: Path, year: int):
    output_file = output_dir / f"pm25_processed_{year}.parquet"

    # Check if the file already exists
    if output_file.exists():
        logger.warning(f"File already exists: {output_file}. Aborting save operation.")
        return  # Avoid overwriting

    logger.info(f"Saving DataFrame to Parguet: {output_file}")

    with open(output_file, "wb") as f:
        df.to_parquet(f, engine="fastparquet")

    logger.info(f"Data for year {year} saved to {output_file}")
