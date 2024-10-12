class NoDataFoundError(Exception):
    def __init__(self, year, message=None):
        if message is None:
            message = f"No data found in the netCDF file for year {year}."
        super().__init__(message)
        self.year = year
