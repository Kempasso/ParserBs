from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

DeclarativeBase = declarative_base()


class VacancyInfo(DeclarativeBase):
    __tablename__ = 'vacancy_info'

    id = Column(Integer, primary_key=True)
    salary = Column('salary', String)
    vacancy_name = Column('vacancy_name', String)
    description = Column('description', String)
    needed_skills = Column('needed_skills', String)
