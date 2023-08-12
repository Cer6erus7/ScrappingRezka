import re
from pprint import pprint
import requests
from bs4 import BeautifulSoup


URL = "https://rezka.ag/films/"
HOST = "https://rezka.ag/"
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)"
}


def get_html(url, params=''):
    return requests.get(url, headers=HEADERS, params=params)

def get_content(html):
    soup = BeautifulSoup(html.text, "lxml")
    cards = soup.find_all("div", class_="b-content__inline_item")

    for card in cards:
        dct = {
            'title': card.find('div', class_="b-content__inline_item-link").find('a').text,
            'country': re.split('[ ,]', card.find('div', class_="b-content__inline_item-link").find('div').text)[2],
            'year': re.split('[ ,]', card.find('div', class_="b-content__inline_item-link").find('div').text)[0],
            'genre': re.split('[ ,]', card.find('div', class_="b-content__inline_item-link").find('div').text)[4],
            'link': card.find('div', class_='b-content__inline_item-cover').find('a').get('href'),
            'img_link': HOST +  card.find('div', class_='b-content__inline_item-cover').find('img').get('src')
        }
        yield dct


if __name__ == "__main__":
    html = get_html(URL)
    number = 0

    for i in get_content(html):
        if number == 3:
            print("Конец")
            break
        number += 1
        pprint(i)