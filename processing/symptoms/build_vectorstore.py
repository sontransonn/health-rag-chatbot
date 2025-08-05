import os, json
from glob import glob
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

data_dir = "data/symptoms/processed"
all_json_files = sorted(glob(os.path.join(data_dir, "processed_*.json")))

print(f"📂 Found {len(all_json_files)} files.")

docs = []
for file_path in all_json_files:
    with open(file_path, "r", encoding="utf-8") as f:
        raw_chunks = json.load(f)

    for chunk in raw_chunks:
        content = chunk["content"]
        metadata = chunk["metadata"]
        docs.append(Document(page_content=content, metadata=metadata))

print(f"📄 Total chunks loaded: {len(docs)}")

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.from_documents(docs, embedding_model)

save_path = "data/symptoms/vectorstore"
vectorstore.save_local(save_path)
print(f"✅ Vectorstore saved to: {save_path}")
