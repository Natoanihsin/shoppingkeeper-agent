from threading import Lock

from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI

from app.core.config import get_settings

settings = get_settings()


class LazyChatModel:
    def __init__(self) -> None:
        self._model: ChatOpenAI | None = None
        self._model_lock = Lock()

    def _get_model(self) -> ChatOpenAI:
        if self._model is not None:
            return self._model

        with self._model_lock:
            if self._model is None:
                if not settings.llm_api_key:
                    raise RuntimeError(
                        "没有配置 LLM_API_KEY"
                    )

                self._model = ChatOpenAI(
                    model=settings.llm_model,
                    api_key=settings.llm_api_key,
                    base_url=settings.llm_base_url,
                    temperature=0,
                )

        return self._model

    def invoke(self, prompt: str) -> BaseMessage:
        return self._get_model().invoke(prompt)


llm = LazyChatModel()