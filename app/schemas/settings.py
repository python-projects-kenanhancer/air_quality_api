from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application Stage
    stage: str = Field(..., env="STAGE")

    # Database Configuration
    db_user: str = Field(..., env="DB_USER")
    db_password: str = Field(..., env="DB_PASSWORD")
    db_host: str = Field(..., env="DB_HOST")
    db_port: int = Field(..., env="DB_PORT")
    db_name: str = Field(..., env="DB_NAME")
    db_url: str = Field(..., env="DB_URL")

    # Logging Configuration
    log_group_name: str = Field(..., env="LOG_GROUP_NAME")

    class Config:
        env_file = ".env"  # Specify the .env file
        env_file_encoding = "utf-8"  # File encoding
        case_sensitive = False  # Environment variables are case-insensitive
