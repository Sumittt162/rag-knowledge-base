from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

DB_PATH = "data/faiss_db"
INDEX_FILE = "data/faiss_db/index.faiss"
_vectorstore_instance = None


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def db_exists() -> bool:
    """Check the actual index file exists, not just the folder."""
    return os.path.exists(INDEX_FILE)


def get_vectorstore():
    global _vectorstore_instance
    if not db_exists():
        return None
    embeddings = get_embeddings()
    _vectorstore_instance = FAISS.load_local(
        DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
    return _vectorstore_instance


def release_vectorstore():
    """Release the FAISS file handle so Windows can delete the folder."""
    global _vectorstore_instance
    _vectorstore_instance = None


def add_documents(chunks: list) -> None:
    embeddings = get_embeddings()
    if db_exists():
        vs = FAISS.load_local(
            DB_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )
        vs.add_documents(chunks)
    else:
        os.makedirs(DB_PATH, exist_ok=True)
        vs = FAISS.from_documents(chunks, embeddings)
    vs.save_local(DB_PATH)
    print(f"Stored {len(chunks)} chunks in FAISS")


def similarity_search(query: str, k: int = 4) -> list:
    vs = get_vectorstore()
    if vs is None:
        return []
    return vs.similarity_search_with_score(query, k=k)