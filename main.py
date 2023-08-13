import re
from time import sleep
from pprint import pprint
import requests
from bs4 import BeautifulSoup


URL = "https://rezka.ag/films"
HOST = "https://rezka.ag/"
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)"
}
FILMS_GENRE = ['триллеры', 'драмы', 'ужасы', "комедии", "мелодрамы", "боевики", "документальны", "приключения",
               "фэнтези", "фантастика", "стендап", "вестерны"]
FILMS_COUNTRY = ['сша', 'великобритания', "германия", "казахстан", "индия", "австралия", "канада", "кения", "франция",
                 "тайвань", "нидерланды", "новая зеландия", "норвегия", "италия", "португалия", "корея южная",
                 "япония", "швеция", "россия", "украина", "индонезия", "польша", ]


class NotFoundCountry(Exception): pass
class NotFoundGenre(Exception): pass


def get_html(url, params=''):
    return requests.get(url, headers=HEADERS, params=params)

def get_content(html):
    page = 1
    while True:
        soup = BeautifulSoup(html.text, "lxml")
        cards = soup.find_all("div", class_="b-content__inline_item")

        for card in cards:
            dct = {
                'title': card.find('div', class_="b-content__inline_item-link").find('a').text,
                'country': re.split('[ ,]', card.find('div', class_="b-content__inline_item-link").find('div').text)[2],
                'year': re.split('[ ,]', card.find('div', class_="b-content__inline_item-link").find('div').text)[0],
                'genre': re.split('[ ,]', card.find('div', class_="b-content__inline_item-link").find('div').text)[4],
                'link': card.find('div', class_='b-content__inline_item-cover').find('a').get('href'),
                'img_link': card.find('div', class_='b-content__inline_item-cover').find('img').get('src')
            }
            yield dct

        page += 1
        html = get_html(URL + f"page/{page}")
        sleep(1)


if __name__ == "__main__":
    films_genre = input("Какой жанр фильмов вы хотите - ").lower()
    films_country = input("Фильмы какой страны вы хотите - ").lower()
    films_number = int(input("Напишите количество фильмов - "))
    print()

    if films_genre not in FILMS_GENRE:
        raise NotFoundGenre("Такого жанра не существует, убедитесь что вы всё правильно написали!")
    if films_country not in FILMS_COUNTRY:
        raise NotFoundCountry("Такой страны не существует, убедитесь что вы всё правильно написали!")

    html = get_html(URL)
    films_count = 0
    for film in get_content(html):
        if films_count == films_number:
            print("Конец парсера!")
            break

        if films_genre == film["genre"].lower() and films_country == film["country"].lower():
            print(f'Название фильма - {film["title"]}')
            print(f'Жанр фильма - {film["genre"]}')
            print(f'Год выпуска - {film["year"]}')
            print(f'Страна выпуска - {film["country"]}')
            print(f'Ссылка на картинку - {film["img_link"]}')
            print(f'Ссылка на фильм - {film["link"]}')
            print(f"Позиция - {films_count+1}\n")
            films_count += 1
