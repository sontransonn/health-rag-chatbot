import os, json
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

data_path = "data/processed/youmed_symptom_processed_001.json"

with open(data_path, "r", encoding="utf-8") as f:
    raw_chunks = json.load(f)

docs = []
for chunk in raw_chunks:
    content = chunk["content"]
    metadata = chunk["metadata"]
    docs.append(Document(page_content=content, metadata=metadata))

print(docs)