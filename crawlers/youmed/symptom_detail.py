import requests, json, re
from bs4 import BeautifulSoup
from datetime import datetime

def crawl_symptom_detail(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    article = soup.select_one("section.article-content article")

    # Extract the article title from the <h1> tag
    title_tag = article.find("h1") if article else None
    title = title_tag.get_text(strip=True).strip() if title_tag else None

    # Extract author information block: name, specialty, and last updated date
    info_block = (tag := article.find("div", class_="flex gap-2 mt-4")) and tag.select_one("div.flex.flex-col")

    author_tag = info_block.select_one("a.font-bold.text-primary.text-sm") if info_block else None
    author = author_tag.get_text(strip=True) if author_tag else None

    specialty_tag = info_block.find("div", class_="text-sm") if info_block else None
    specialty = specialty_tag.get_text(strip=True).split(":", 1)[-1].strip() if specialty_tag else None
    
    updated_date = datetime.fromisoformat((tag := info_block.find("time", class_="text-sm")) and tag.get("datetime")).date().isoformat()

    # Extract content from the article (ignore images)
    content_block = article.find("div", class_="prose max-w-none my-4 prose-a:text-primary") if article else None
    for tag in content_block(["figure", "figcaption", "img", "picture"]):
        tag.decompose()
    content = re.sub(r"\n{2,}", "\n\n", content_block.get_text(separator="\n").strip())

    return {
        "title": title,
        "author": author,
        "specialty": specialty,
        "updated_date": updated_date,
        "content": content
    }

if __name__ == "__main__":
    url = "https://youmed.vn/tin-tuc/dai-thao-duong-tuyp-1/"
    detail = crawl_symptom_detail(url)
    print(json.dumps(detail, indent=2, ensure_ascii=False))

