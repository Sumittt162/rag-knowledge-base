from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from src.llm import get_llm

TEMPLATE = (
    "You are a helpful assistant. Use the context below to answer the question.\n\n"
    "Rules:\n"
    "1. Answer only from the context provided.\n"
    "2. If the answer is not in the context, say clearly: "
    "'I could not find this in your documents.'\n"
    "3. Keep answers clear and to the point.\n"
    "4. Mention the source file at the end like: [Source: filename.pdf]\n\n"
    "Context:\n{context}\n\n"
    "Previous conversation:\n{chat_history}\n\n"
    "Question: {question}\n\n"
    "Answer:"
)

RAG_PROMPT = PromptTemplate(
    input_variables=["context", "question", "chat_history"],
    template=TEMPLATE
)


def build_rag_chain():
    from src.vectorstore import get_vectorstore
    vectorstore = get_vectorstore()
    if vectorstore is None:
        return None

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 4, "fetch_k": 20},
    )

    memory = ConversationBufferWindowMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer",
        k=5,
    )

    return ConversationalRetrievalChain.from_llm(
        llm=get_llm(),
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": RAG_PROMPT},
        return_source_documents=True,
    )


def ask(chain, question: str) -> dict:
    result = chain({"question": question})
    return {
        "answer": result["answer"],
        "sources": [
            {
                "file": doc.metadata.get("source_file", "unknown"),
                "page": doc.metadata.get("page", "?"),
                "snippet": doc.page_content[:200] + "...",
            }
            for doc in result["source_documents"]
        ],
    }