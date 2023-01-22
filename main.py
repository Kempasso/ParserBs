import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from utils import make_soup, get_page, Controller

DeclarativeBase = declarative_base()
engine = create_engine('sqlite:///mydatabase.db')
Session = sessionmaker(engine)
session = Session()


class VacancyInfo(DeclarativeBase):
    __tablename__ = 'vacancy_info'

    id = Column(Integer, primary_key=True)
    salary = Column('salary', String)
    vacancy_name = Column('vacancy_name', String)
    description = Column('description', String)
    needed_skills = Column('needed_skills', String)


DeclarativeBase.metadata.create_all(engine)

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
    'accept': '*/*'}

counter = 0
url = 'https://spb.hh.ru/search/vacancy'
params = {'text': 'Психолог', 'page': counter}
page = get_page(url, HEADERS, params)
soup = make_soup(page)

max_page = int(soup.find_all('a', attrs={'class': "bloko-button"})[-2].find_next().text)
links = []
while counter < 1:
    [links.append(link.get('href')) for link in soup.find_all(attrs={'class': 'serp-item__title'})]
    next_page = get_page(url, HEADERS, params)
    counter += 1

for link in links:
    vacancy_page = get_page(link, HEADERS)
    vacancy_soup = make_soup(vacancy_page)
    data = vacancy_soup.find_all(
        attrs={'data-qa': ["vacancy-title", "vacancy-salary", "vacancy-description", 'bloko-tag__text']})

    data = {
        'salary': data[1].text,
        'vacancy_name': data[0].text,
        'description': data[2].text,
        'needed_skills': ', '.join(map(lambda x: x.text, data[3:]))
    }
    vacancy = VacancyInfo(**data)

    with session as db:
        db.add(vacancy)
        db.commit()
