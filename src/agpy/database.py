from sqlalchemy import Engine
from sqlmodel import create_engine
from agpy.config import get_database_settings

def get_engine() -> Engine:
    global _engine
    if _engine is None:
        _engine = create_engine(get_database_settings().url)
    return _engine
engine: Engine | None = get_engine()