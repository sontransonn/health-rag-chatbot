import json, re, os, unicodedata

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

def normalize_field(value):
    if not isinstance(value, str):
        return ""
    value = unicodedata.normalize("NFKC", value)
    value = re.sub(r"\s+", " ", value.strip())
    return value.lower()

if __name__ == "__main__":
    input_path = "data/raw/youmed_symptom_raw.json"
    output_dir = "data/processed/"
    os.makedirs(output_dir, exist_ok=True)

    with open(input_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    all_chunks = []
    file_count = 1
    symptom_count = 0

    for idx, symptom in enumerate(raw_data):
        information = symptom.get("information", "")
        if not information.strip():
            continue

        metadata = {
            "symptom_id": normalize_field(symptom.get("symptom_id", "")),
            "symptom_name": normalize_field(symptom.get("symptom_name", "")),
            "source": normalize_field(symptom.get("source", ""))
        }

        chunks = chunk_text(clean_text(information), max_words=200, overlap=1)
        for i, chunk in enumerate(chunks, start=1):
            all_chunks.append({
                "chunk_id": f"{symptom.get("symptom_id", f"symptom_{idx}")}_{i}",
                "content": chunk,
                "metadata": metadata
            })

        symptom_count += 1
        if symptom_count % 50 == 0:
            output_path = os.path.join(output_dir, f"youmed_symptom_processed_{file_count:03}.json")
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(all_chunks, f, ensure_ascii=False, indent=2)
            print(f"✅ Đã ghi {len(all_chunks)} chunk vào {output_path}")
            file_count += 1
            all_chunks = []

    if all_chunks:
        output_path = os.path.join(output_dir, f"youmed_symptom_processed_{file_count:03}.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(all_chunks, f, ensure_ascii=False, indent=2)
        print(f"✅ Đã ghi {len(all_chunks)} chunk cuối vào {output_path}")
