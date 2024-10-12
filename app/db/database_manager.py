import logging
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DatabaseManager:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    @contextmanager
    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)
        logging.info("All tables created successfully.")

    def drop_tables(self):
        Base.metadata.drop_all(bind=self.engine)
        logging.info("All tables dropped successfully.")

    def recreate_tables(self):
        self.drop_tables()
        self.create_tables()
        logging.info("All tables have been dropped and recreated successfully.")
