"""Configuration settings"""

from pathlib import Path

from pydantic import BaseSettings

ROOT_DIR = Path(__file__).parent
CARRIERS_FILENAME = "carriers.json"
CARRIERS_FILEPATH = ROOT_DIR / CARRIERS_FILENAME


class EmailServerSettings(BaseSettings):
    email: str
    password: str
    smtp_host: str
    smtp_port: int

    class Config:
        env_file = ".env"


settings = EmailServerSettings()
