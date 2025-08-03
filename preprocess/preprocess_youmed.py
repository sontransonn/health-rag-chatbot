import json, re
import unicodedata, os

def clean_text(text):
    text = unicodedata.normalize("NFKC", text)
    paragraphs = text.split("\n\n")
    cleaned_paragraphs = []
    for para in paragraphs:
        para = para.strip().lower()
        para = re.sub(r"[^\w\s.,!?%–/-]", "", para)
        para = re.sub(r"\s+", " ", para)
        if para:
            cleaned_paragraphs.append(para)
    return "\n\n".join(cleaned_paragraphs)

def chunk_text(text, max_words=200, overlap=1):
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = []
    current_len = 0

    for para in paragraphs:
        word_count = len(para.split())
        if current_len + word_count > max_words:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
            overlap_chunk = current_chunk[-overlap:] if overlap else []
            current_chunk = overlap_chunk + [para]
            current_len = sum(len(p.split()) for p in current_chunk)
        else:
            current_chunk.append(para)
            current_len += word_count
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

if __name__ == "__main__":
    input_path="data/raw/youmed_raw_data.json"
    output_path="data/processed/youmed_articles_chunks.json"

    with open(input_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    processed = []

    cleaned_text = clean_text(raw_data[0]["article"]["content"])
    chunks = chunk_text(cleaned_text, max_words=200, overlap=1)
    for i, chunk in enumerate(chunks):
        print(f"\n--- Chunk {i+1} ---\n{chunk}\n")