import requests
from bs4 import BeautifulSoup


def make_soup(page):
    return BeautifulSoup(page.text, 'html.parser')


def get_page(url, headers, params=None):
    return requests.get(url, headers=headers, params=params)



class Controller:

    @classmethod
    def get_page_from_requests(cls, url, headers, params=None):
        return requests.get(url, headers=headers, params=params)

    @classmethod
    def make_soup(cls, page):
        return BeautifulSoup(page.text, 'html.parser')
