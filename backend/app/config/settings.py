import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR.parent / ".env")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    MSSQL_SA_PASSWORD = os.getenv("MSSQL_SA_PASSWORD")

    SQLALCHEMY_DATABASE_URI = (
        "mssql+pyodbc://sa:"
        f"{MSSQL_SA_PASSWORD}"
        "@127.0.0.1:1433/Aegis360"
        "?driver=ODBC+Driver+18+for+SQL+Server"
        "&TrustServerCertificate=yes"
        "&Encrypt=yes"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "aegis360-development-secret-change-this"
)
    JWT_ALGORITHM = "HS256"

    JWT_EXPIRATION_MINUTES = 60
