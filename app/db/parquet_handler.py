import os
import pandas as pd

PROCESSED_DATA_DIR = "processed_data"


def load_parquet_files():
    data_frames = []
    for file_name in os.listdir(PROCESSED_DATA_DIR):
        if file_name.endswith(".parquet"):
            file_path = os.path.join(PROCESSED_DATA_DIR, file_name)
            data_frames.append(pd.read_parquet(file_path))
    return (
        pd.concat(data_frames, ignore_index=True)
        if data_frames
        else pd.DataFrame(columns=["year", "latitude", "longitude", "pm25_level"])
    )


def save_processed_data(df: pd.DataFrame, year: int):
    file_path = os.path.join(PROCESSED_DATA_DIR, f"pm25_processed_{year}.parquet")
    df.to_parquet(file_path, index=False)
