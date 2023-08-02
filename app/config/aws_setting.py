# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=too-few-public-methods
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class AwsSettings(BaseSettings):
    region: str = os.getenv("AWS_REGION")
    access_key_id: str = os.getenv("AWS_ACCESS_KEY_ID")
    secret_access_key: str = os.getenv("AWS_SECRET_ACCESS_KEY")
    user_pool_id: str = os.getenv("AWS_USER_POOL_ID")
    app_client_id: str = os.getenv("AWS_APP_CLIENT_ID")
    bucket_name: str = os.getenv("AWS_STORAGE_BUCKET_NAME")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
