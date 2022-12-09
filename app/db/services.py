from .database import database


def create_database():
    return database.Base.metadata.create_all(bind=database.engine)
