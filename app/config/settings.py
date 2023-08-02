# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=too-few-public-methods
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Setting(BaseSettings):
    domain_front: str = os.getenv("DOMAIN_FRONT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
