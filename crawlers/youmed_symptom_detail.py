import requests, json, re
from bs4 import BeautifulSoup
from datetime import datetime

def crawl_symptom_detail(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    article = soup.select_one("section.article-content article")

    # Extract content from the article (ignore images)
    content_block = article.find("div", class_="prose max-w-none my-4 prose-a:text-primary") if article else None
    if content_block:
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
    else:
        content = ""

    return content

if __name__ == "__main__":
    url = "https://youmed.vn/tin-tuc/dai-thao-duong-tuyp-1/"
    detail = crawl_symptom_detail(url)
    print(json.dumps(detail, indent=2, ensure_ascii=False))

