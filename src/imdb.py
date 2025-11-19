from dataclasses import dataclass
import json
from bs4 import BeautifulSoup
import requests
import re

@dataclass
class ImdbVariant:
    id: int
    name: str
    url: str
    premiere_date: str

class DownloaderBase:
    def __init__(self, url: str) -> None:
        self.url = url
        self.response = self.grab_page()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.url}) brings status code {self.response.status_code}."

    def grab_page(self) -> requests.Response:
        headers = {
            "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5",
            "priority": "i",
            "referer": "https://www.imdb.com/",
            "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "image",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-site": "cross-site",
            "sec-fetch-storage-access": "active",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        }
        response = requests.get(self.url, headers=headers)
        assert response.status_code == 200
        return response


class DownloadTitle(DownloaderBase):
    def __init__(self, url: str) -> None:
        super().__init__(url)

    def strip_page_details(self):
        # Необходимо собрать со страницы следующие данные:
        # - оригинальное название
        # - русское название
        # - тип полный метр или сериал
        # - если полный метр, то продолжительность
        # - дата премьеры
        pass


def grab_page(url: str) -> requests.Response:
    headers = {
        "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5",
        "priority": "i",
        "referer": "https://www.imdb.com/",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "image",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-site": "cross-site",
        "sec-fetch-storage-access": "active",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    return response


def strip_page_details(response: requests.Response) -> dict:
    def href_releaseinfo(href):
        return href and re.compile("releaseinfo").search(href)

    soup = BeautifulSoup(response.text, features="html.parser")
    movie_tags = [
        span.text for span in soup.select("div.ipc-chip-list__scroller > a > span")
    ]
    scrit_json = soup.find_all(type="application/ld+json")
    json_dict = json.loads(scrit_json[0].text)
    premiere_link = soup.find(href=href_releaseinfo)

    if "duration" in json_dict.keys():
        duration = json_dict["duration"]
    else:
        duration = None

    movie = {
        "name_original": json_dict["name"],
        "name_russian": json_dict["alternateName"],
        "duration": duration,
        "premiere_date": premiere_link.text,
        "imdb_link": json_dict["url"],
        "type": json_dict["@type"],
        "genres": movie_tags,
    }
    return movie

def make_search_string(movie_name: str) -> str:
    search_str: str = "https://www.imdb.com/find/?q="
    search_str += movie_name
    return search_str

    # Обращение к IMDb и получение страницы с результатами поиска
    # Оформление результатов в список и демонстрация списка на экране
    # Получение ID для поиска конкретной страницы от вида и контроллера
    # Загрузка страницы с IMDb и получение деталей фильма 
    # Возвращение в контроллер деталей фильма
    # Контроллер обновляет данные в БД и в отображении дерева в виде
def initial_search_imdb(movie_name: str) -> list:
    search_url = make_search_string(movie_name)
    response = grab_page(search_url)
    soup = BeautifulSoup(response.text, features="html.parser")
    movies = soup.select("ul.ipc-metadata-list--base > li > div > div > div > div > div.cli-children")
    searched = []
    for i, movie in enumerate(movies):
        lil_soup = BeautifulSoup(str(movie), "html.parser")
        name = lil_soup.select("div.ipc-title--title > a")
        year = lil_soup.select("div.cli-title-metadata > span")
        searched.append(
            ImdbVariant(
                id=i,
                name=name[0].text,
                url=lil_soup.a["href"],
                premiere_date=year[0].text,
            )
        )
    return searched


if __name__ == "__main__":
    # url = "https://www.imdb.com/title/tt0120815/"
    url = "https://www.imdb.com/title/tt0211192/"
    page = grab_page(url)
    movie = strip_page_details(page)
    print(movie)
    # selecting_something()
