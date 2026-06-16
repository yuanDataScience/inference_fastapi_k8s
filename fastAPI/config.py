from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    DB_URL: str
    DB_NAME: str
    TOKEN_SECRET: str
    AWS_DEFAULT_REGION: str
    MLFLOW_S3_ENDPOINT_URL: str
    MLFLOW_BOTO_CLIENT_ADDRESSING_STYLE: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    mlflow_tracking_uri: str
    

    """Loads the dotenv file. Including this is necessary to get
    pydantic to load a .env file."""
    # model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    model_config = SettingsConfigDict(extra="ignore")