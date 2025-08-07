import json, time 
import os, hashlib, requests
from bs4 import BeautifulSoup

BASE_URL= "https://youmed.vn/tin-tuc/trieu-chung-benh/"
OUTPUT_DIR = "datasets/symptoms_diseases"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "raw.json")

def save_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_existing_data(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def generate_id(text):
    return hashlib.md5(text.encode()).hexdigest()[:8]

def crawl_with_retry(url, retries=2, delay=2):
    for attempt in range(retries + 1):
        try:
            return crawl_symptom_detail(url)
        except Exception as e:
            if attempt < retries:
                print(f"Retrying ({attempt+1}) for {url} due to error: {e}")
                time.sleep(delay)
            else:
                raise e

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

def crawl_symptom_detail(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    article = soup.select_one("section.article-content article")
    content_block = article.find("div", class_="prose max-w-none my-4 prose-a:text-primary") if article else None

    if not content_block:
        return ""
    
    toc = content_block.find("div", class_="ez-toc-v2_0_72 counter-flat ez-toc-counter ez-toc-custom ez-toc-container-direction")
    if toc:
        toc.decompose()
    for tag in content_block(["figure", "figcaption", "img", "picture"]):
        tag.decompose()
    paragraphs = content_block.find_all(["p", "li"])
    content = "\n\n".join(" ".join(p.stripped_strings)
        for p in paragraphs
            if p.get_text(strip=True)
        )

    return content

if __name__ == "__main__":
    print("Loading disease list...")
    symptoms_list = crawl_symptoms_list()
    print(f"Found {len(symptoms_list)} diseases.")

    existing_data = load_existing_data(OUTPUT_FILE)
    crawled_urls = {item["source"] for item in existing_data}
    print(f"Resuming from backup, already crawled {len(existing_data)} items.")

    data = existing_data
    counter_since_last_save = 0

    for i, item in enumerate(symptoms_list[:20]):
        name = item["name"]
        url = item["url"]

        if url in crawled_urls:
            print(f"[{i+1}/{len(symptoms_list)}] Skipped: {name}")
            continue

        try:
            text = crawl_with_retry(url)
            data.append({
                "id": generate_id(name + url),
                "name": name,
                "information": text,
                "source": url,
            })
            counter_since_last_save += 1

            print(f"[{i+1}/{len(symptoms_list)}] Done: {name}")
            time.sleep(1)

            if counter_since_last_save >= 10:
                save_json(data, OUTPUT_FILE)
                counter_since_last_save = 0

        except Exception as e:
            print(f"[{i+1}/{len(symptoms_list)}] Error at {name}: {e}")

    save_json(data, OUTPUT_FILE)
    print("Crawling completed.")