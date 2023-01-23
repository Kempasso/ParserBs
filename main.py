from db import DataBase

from models import DeclarativeBase, VacancyInfo
from utils import DataHandler, Creator

engine = DataBase.create_db_engine('sqlite:///mydatabase.db')
session = DataBase.create_session(engine)
DeclarativeBase.metadata.create_all(engine)

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
    'accept': '*/*'}

url = 'https://spb.hh.ru/search/vacancy'
params = {'text': 'Python'}
main_page = Creator.get_page_from_requests(url, params)
main_soup = Creator.make_soup(main_page)
count_of_page = int(main_soup.find_all('a', attrs={'class': "bloko-button"})[-2].find_next().text)
links = DataHandler.get_links(main_soup, url, params)

DataHandler.get_info_from_links(links, session)
