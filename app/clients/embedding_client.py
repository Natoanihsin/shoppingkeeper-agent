from threading import Lock

from sentence_transformers import SentenceTransformer

from app.core.config import get_settings

settings = get_settings()


class LocalEmbeddingClient:
    def __init__(self) -> None:
        self._model: SentenceTransformer | None = None
        self._model_lock = Lock()

    def _get_model(self) -> SentenceTransformer:
        if self._model is not None:
            return self._model

        with self._model_lock:
            if self._model is None:
                self._model = SentenceTransformer(
                    settings.embedding_model,
                    device="cpu",
                )

        return self._model

    def embed_query(self, text: str) -> list[float]:
        model = self._get_model()

        vector = model.encode(
            text,
            normalize_embeddings=True,
        )

        return vector.tolist()

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        model = self._get_model()

        vectors = model.encode(
            texts,
            normalize_embeddings=True,
        )

        return vectors.tolist()


embedding_client = LocalEmbeddingClient()