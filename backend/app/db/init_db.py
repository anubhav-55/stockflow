from app.db.base import Base
from app.db.session import engine
from app import models

def init_db() -> None:
    # Importing the models registers their tables with Base.metadata.
    # create_all() then creates any tables that don't alredy exist.
    Base.metadata.create_all(bind=engine)