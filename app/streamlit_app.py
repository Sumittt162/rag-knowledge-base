import streamlit as st
import tempfile, os, sys, shutil, glob, time

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.ingestion import load_and_split
from src.vectorstore import add_documents, release_vectorstore, db_exists
from src.rag_chain import build_rag_chain, ask


st.set_page_config(page_title="My Knowledge Base", page_icon="📚")
st.title("📚 My AI Knowledge Base")
st.caption("Upload PDFs and ask questions about them!")


def safe_clear_db():
    """Release file handles first then delete — fixes Windows permission error."""
    release_vectorstore()
    st.session_state.chain = None
    time.sleep(0.3)
    if os.path.exists("data/faiss_db"):
        try:
            shutil.rmtree("data/faiss_db")
        except PermissionError:
            for f in glob.glob("data/faiss_db/*"):
                try:
                    os.remove(f)
                except Exception:
                    pass


with st.sidebar:
    st.header("Step 1: Upload your PDFs")

    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:
        if st.button("Process Documents", type="primary"):
            safe_clear_db()
            st.session_state.messages = []
            with st.spinner("Reading your documents..."):
                for f in uploaded_files:
    # Save with the REAL filename so metadata shows correct name
                   tmp_path = os.path.join(tempfile.gettempdir(), f.name)
                with open(tmp_path, "wb") as tmp:
                 tmp.write(f.read())
                 chunks = load_and_split(tmp_path)
                add_documents(chunks)
                os.unlink(tmp_path)
                st.session_state.chain = build_rag_chain()
            st.success(f"Done! Processed {len(uploaded_files)} file(s)")

    st.divider()

    st.caption("Currently loaded:")
    if db_exists():
        st.success("Documents ready to query")
    else:
        st.warning("No documents loaded yet")

    st.divider()

    if st.button("Clear all documents", type="secondary"):
        safe_clear_db()
        st.session_state.messages = []
        st.success("Cleared! Upload new PDFs to start fresh.")
        st.rerun()

    st.divider()
    st.markdown("**Step 2:** Ask questions below ↓")


if "chain" not in st.session_state:
    st.session_state.chain = None
if "messages" not in st.session_state:
    st.session_state.messages = []

if st.session_state.chain is None and db_exists():
    st.session_state.chain = build_rag_chain()

if st.session_state.chain is None:
    st.info("👈 Upload a PDF from the sidebar first, then ask questions!")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander(f"Sources ({len(msg['sources'])})"):
                for src in msg["sources"]:
                    st.markdown(f"**{src['file']}** — Page {src['page']}")
                    st.caption(src["snippet"])

if question := st.chat_input("Ask anything about your documents..."):
    if st.session_state.chain is None:
        st.warning("Please upload and process a PDF first!")
    else:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching your documents..."):
                result = ask(st.session_state.chain, question)
            st.markdown(result["answer"])
            if result["sources"]:
                with st.expander(f"Sources ({len(result['sources'])})"):
                    for src in result["sources"]:
                        st.markdown(f"**{src['file']}** — Page {src['page']}")
                        st.caption(src["snippet"])

        st.session_state.messages.append({
            "role": "assistant",
            "content": result["answer"],
            "sources": result["sources"],
        })