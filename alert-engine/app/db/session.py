from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.settings import AlertEngineSettings
from app.db.models import Base


def create_session_factory(settings: AlertEngineSettings) -> sessionmaker:
    engine = create_engine(settings.database_url, pool_pre_ping=True, pool_size=5, max_overflow=10)
    Base.metadata.create_all(bind=engine)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)

