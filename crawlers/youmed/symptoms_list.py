import requests
from bs4 import BeautifulSoup

BASE_URL = "https://youmed.vn/tin-tuc/trieu-chung-benh/"

def crawl_symptoms_list():
    response = requests.get(BASE_URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    symptom_elements = soup.select(".letter-section ul.az-columns li a")

    symptoms = []
    for el in symptom_elements:
        name = el.text.strip()
        url = el["href"]
        symptoms.append({"name": name, "url": url})

    return symptoms

if __name__ == "__main__":
    symptoms = crawl_symptoms_list()
    for s in symptoms:
        print(f"{s['name']}: {s['url']}")
