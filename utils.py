import requests
from bs4 import BeautifulSoup

from db import DataBase
from models import VacancyInfo

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
    'accept': '*/*'}


class Creator:

    @staticmethod
    def get_page_from_requests(link, params=None):
        return requests.get(url=link, headers=HEADERS, params=params)

    @staticmethod
    def make_soup(page):
        return BeautifulSoup(page.text, 'html.parser')


class DataHandler:

    @staticmethod
    def get_links(soup, url, params):
        max_page = int(soup.find_all('a', attrs={'class': "bloko-button"})[-2].find_next().text)
        links = []
        counter = 0
        params['page'] = counter
        while counter < max_page:
            next_page = Creator.get_page_from_requests(url, params)
            next_soup = Creator.make_soup(next_page)
            [links.append(link.get('href')) for link in next_soup.find_all(attrs={'class': 'serp-item__title'})]
            counter += 1
        return links

    @staticmethod
    def get_info_from_links(links, session):
        for link in links:
            vacancy_page = Creator.get_page_from_requests(link, HEADERS)
            vacancy_soup = Creator.make_soup(vacancy_page)
            data = vacancy_soup.find_all(
                attrs={'data-qa': ["vacancy-title", "vacancy-salary", "vacancy-description", 'bloko-tag__text']})

            clear_info = {
                'salary': data[1].text,
                'vacancy_name': data[0].text,
                'description': data[2].text,
                'needed_skills': ', '.join(map(lambda x: x.text, data[3:]))
            }
            vacancy = VacancyInfo(**clear_info)
            DataBase.create_note(vacancy, session)
