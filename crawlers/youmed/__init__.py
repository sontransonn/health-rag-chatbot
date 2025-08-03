import json, time 
import os, hashlib
from symptoms_list import crawl_symptoms_list
from symptom_detail import crawl_symptom_detail

OUTPUT_DIR = "data/raw"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "youmed_raw_data.json")

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

if __name__ == "__main__":
    print("Loading symptom list...")
    symptoms_list = crawl_symptoms_list()
    print(f"Found {len(symptoms_list)} symptoms.")

    existing_data = load_existing_data(OUTPUT_FILE)
    crawled_urls = {item["article_url"] for item in existing_data}
    print(f"Resuming from backup, already crawled {len(existing_data)} items.")

    data = existing_data
    counter_since_last_save = 0

    for i, item in enumerate(symptoms_list[:10]):
        name = item["name"]
        url = item["url"]

        if url in crawled_urls:
            print(f"[{i+1}/{len(symptoms_list)}] Skipped: {name}")
            continue

        try:
            article = crawl_with_retry(url)
            data.append({
                "id": generate_id(name + url),
                "symptom": name,
                "article_url": url,
                "article": article
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
