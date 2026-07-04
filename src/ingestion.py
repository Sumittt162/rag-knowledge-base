from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path


def load_and_split(file_path: str) -> list:
    loader = PyPDFLoader(file_path)
    raw_docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
    )
    chunks = splitter.split_documents(raw_docs)

    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i
        chunk.metadata["source_file"] = Path(file_path).name

    print(f"Loaded {len(raw_docs)} pages → {len(chunks)} chunks")
    return chunks