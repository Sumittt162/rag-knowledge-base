from reportlab.pdfgen import canvas
from src.ingestion import load_and_split

def test_pdf_gets_split_into_chunks(tmp_path):
    pdf_path = tmp_path / "test.pdf"
    c = canvas.Canvas(str(pdf_path))
    c.drawString(100, 750, "Machine learning is a subset of AI.")
    c.save()

    chunks = load_and_split(str(pdf_path))

    assert len(chunks) > 0
    assert chunks[0].metadata["source_file"] == "test.pdf" 

def test_chunks_have_id_numbers(tmp_path):
    from reportlab.pdfgen import canvas
    pdf_path = tmp_path / "test2.pdf"
    c = canvas.Canvas(str(pdf_path))
    c.drawString(100, 750, "RAG combines retrieval with generation.")
    c.save()

    chunks = load_and_split(str(pdf_path))
    # Every chunk should have a chunk_id, starting from 0
    assert chunks[0].metadata["chunk_id"] == 0

def test_config_loads_without_crashing():
    from src.config import settings
    # If this line runs without an error, the config is valid
    assert settings.llm_model == "llama-3.3-70b-versatile"