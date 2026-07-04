from langchain_groq import ChatGroq
from src.config import settings

def get_llm(streaming: bool = False):
    return ChatGroq(
        groq_api_key=settings.groq_api_key,
        model_name=settings.llm_model,
        temperature=0.1,
        max_tokens=1024,
        streaming=streaming,
    )