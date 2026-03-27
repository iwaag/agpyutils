from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DatabaseSettings:
    sql_type: str
    sql_user: str
    sql_password: str
    sql_host: str
    sql_port: str
    sql_db: str

    @property
    def url(self) -> str:
        return (
            f"{self.sql_type}://{self.sql_user}:{self.sql_password}"
            f"@{self.sql_host}:{self.sql_port}/{self.sql_db}"
        )

def get_database_settings() -> DatabaseSettings:
    return DatabaseSettings(
        sql_type=os.getenv("SQL_TYPE", ""),
        sql_user=os.getenv("SQL_USER", ""),
        sql_password=os.getenv("SQL_PASSWORD", ""),
        sql_host=os.getenv("SQL_HOST", ""),
        sql_port=os.getenv("SQL_PORT", ""),
        sql_db=os.getenv("SQL_DB", ""),
    )
database_setting = get_database_settings()