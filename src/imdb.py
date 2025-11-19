from bs4 import BeautifulSoup
import requests


def selecting_something():
    with open("src/r.html", encoding="utf-8") as f:
        soup = BeautifulSoup(f, features="html.parser")

    d = soup.select("div.ipc-chip-list__scroller > a > span")
    for g in d:
        print(g.text)


class DownloaderBase:
    def __init__(self, url: str) -> None:
        self.url = url
        self.response = self.grab_page()

    def __repr__(self):
        return f"{self.__class__.__name__}({url}) brings status code {self.response.status_code}."

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


if __name__ == "__main__":
    url = "https://www.imdb.com/title/tt0120815/"
    d = DownloadTitle(url)
    print(d)
