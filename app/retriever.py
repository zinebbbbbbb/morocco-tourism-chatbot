import pandas as pd
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def load_retriever(csv_path: str, k: int = 3):
    """
    Load CSV tourism data and build a retriever with FAISS + embeddings.
    """
    df = pd.read_csv(csv_path)

    def row_to_text(row):
        parts = [f"{col}: {val}" for col, val in row.items() if pd.notna(val)]
        return ". ".join(parts) + "."

    text_docs = [Document(page_content=row_to_text(row)) for _, row in df.iterrows()]

    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(text_docs, embedding_model)

    return vector_store.as_retriever(search_kwargs={"k": k})
