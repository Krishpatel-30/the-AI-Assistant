import faiss
import numpy as np

from embeddings import EmbeddingModel


class RAG:

    def __init__(self):

        self.embedding_model = EmbeddingModel()

        self.index = None

        self.chunks = []

    # ----------------------------------------
    # Split PDF into chunks
    # ----------------------------------------

    def chunk_text(
        self,
        text,
        chunk_size=500
    ):

        words = text.split()

        chunks = []

        for i in range(
            0,
            len(words),
            chunk_size
        ):

            chunk = " ".join(
                words[i:i + chunk_size]
            )

            chunks.append(chunk)

        return chunks

    # ----------------------------------------
    # Build Vector Database
    # ----------------------------------------

    def build(self, pdf_text):

        self.chunks = self.chunk_text(pdf_text)

        embeddings = self.embedding_model.embed_batch(
            self.chunks
        )

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(
            dimension
        )

        self.index.add(embeddings)

    # ----------------------------------------
    # Search
    # ----------------------------------------

    def search(
        self,
        query,
        k=5
    ):

        if self.index is None:
            return []

        query_embedding = self.embedding_model.embed(
            query
        )

        query_embedding = np.array(
            [query_embedding]
        )

        scores, indices = self.index.search(
            query_embedding,
            k
        )

        results = []

        for idx in indices[0]:

            if idx != -1:

                results.append(
                    self.chunks[idx]
                )

        return results