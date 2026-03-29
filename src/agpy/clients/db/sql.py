from sqlalchemy import Engine
from sqlmodel import create_engine
from agpy.clients.db.config import get_database_settings

def get_engine() -> Engine:
    return create_engine(get_database_settings().url)

engine: Engine | None = get_engine()