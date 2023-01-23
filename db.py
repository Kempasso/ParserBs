from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


class DataBase:
    @staticmethod
    def create_db_engine(path_to_db):
        engine = create_engine(path_to_db)
        return engine

    @staticmethod
    def create_session(engine):
        Session = sessionmaker(engine)
        session = Session()
        return session

    @staticmethod
    def create_note(obj, session):
        with session as db:
            db.add(obj)
            db.commit()
