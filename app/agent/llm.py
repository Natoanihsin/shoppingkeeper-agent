from langchain_openai import ChatOpenAI

from app.core.config import get_settings

settings = get_settings()

if not settings.llm_api_key:
    raise RuntimeError("没有配置 LLM_API_KEY")


llm = ChatOpenAI(
    model=settings.llm_model,
    api_key=settings.llm_api_key,
    base_url=settings.llm_base_url,
    temperature=0,
)