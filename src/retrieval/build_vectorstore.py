import os, json
from glob import glob
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

data_dir = "datasets/symptoms_diseases/processed"
save_path = "datasets/symptoms_diseases/chroma"

all_json_files = sorted(glob(os.path.join(data_dir, "processed_*.json")))
print(f"📂 Found {len(all_json_files)} files in {data_dir}")

docs = []
for file_path in all_json_files:
    with open(file_path, "r", encoding="utf-8") as f:
        raw_chunks = json.load(f)

    for chunk in raw_chunks:
        content = chunk["content"]
        metadata = chunk["metadata"]
        docs.append(Document(page_content=content, metadata=metadata))

print(f"📄 Total chunks loaded: {len(docs)}")

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embedding_model,
    persist_directory=save_path
)

vectorstore.persist()
print(f"✅ Chroma vectorstore saved to: {save_path}")
