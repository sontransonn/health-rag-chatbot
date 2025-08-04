import os, json, glob
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

# Lấy file đầu tiên để test
file_path = glob.glob("data/preprocessed/*.json")[0]

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Tạo Document
docs = [
    Document(
        page_content=item.get("content", ""),
        metadata=item.get("metadata", {})
    )
    for item in data
]

print(f"✅ Số lượng documents: {len(docs)}")

# Tạo embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Tạo vectorstore
vectorstore = FAISS.from_documents(docs, embeddings)

# Thử truy vấn
query = "bệnh béo phì là gì"
docs_with_scores = vectorstore.similarity_search_with_score(query, k=20)

for doc, score in docs_with_scores:
    print("\n🔍 Kết quả tìm kiếm:")
    print(f"Score: {score:.4f}")
    print(f"Nội dung: {doc.page_content[:200]}...")
    print(f"Metadata: {doc.metadata}")
