import requests
from bs4 import BeautifulSoup

BASE_URL = "https://youmed.vn/tin-tuc/trieu-chung-benh/"

def crawl_wikipedia(topic: str):
    url = f"https://example.com/"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Không thể truy cập {url}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup)

if __name__ == "__main__":
    crawl_wikipedia("Ung_thư") 