"""
Document retriever for RAG pipeline.

Handles semantic search over indexed documents.
"""

from typing import Any, cast

from src.agent.config import config
from src.rag.embeddings import BedrockEmbeddings


class DocumentRetriever:
    """Retrieves relevant documents from ChromaDB using semantic search."""

    def __init__(self, collection_name: str = "sow_documents") -> None:
        """
        Initialize document retriever.

        Args:
            collection_name: Name of the ChromaDB collection
        """
        self.collection_name = collection_name
        self.embeddings = BedrockEmbeddings()
        self.chroma_client = config.chroma_client

        # Get collection
        self.collection = self.chroma_client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "SOW documents and knowledge base"},
        )

    def search(
        self,
        query: str,
        n_results: int = 5,
        filters: dict[str, str] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Search for relevant documents.

        Args:
            query: Search query
            n_results: Number of results to return
            filters: Optional metadata filters (e.g., {"client_id": "CLIENT-001"})

        Returns:
            List of result dictionaries with 'content', 'metadata', and 'score'
        """
        from typing import Any

        # Generate query embedding
        query_embedding = self.embeddings.embed_query(query)

        # Build where clause from filters
        where: dict[str, Any] | None = None
        if filters:
            if len(filters) > 1:
                # Wrap multiple filters in $and operator
                where = {"$and": [{k: v} for k, v in filters.items()]}
            else:
                where = cast(dict[str, Any], filters)

        # Query ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where,
        )

        # Format results
        formatted_results = []
        if results["documents"] and len(results["documents"]) > 0:
            for i in range(len(results["documents"][0])):
                formatted_results.append(
                    {
                        "content": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i],
                        "score": results["distances"][0][i] if results["distances"] else 0.0,
                    }
                )

        return formatted_results

    def search_by_client(self, query: str, client_id: str, n_results: int = 5) -> list[dict]:
        """
        Search for documents related to a specific client.

        Args:
            query: Search query
            client_id: Client ID filter
            n_results: Number of results

        Returns:
            List of search results
        """
        return self.search(query, n_results, filters={"client_id": client_id})

    def search_by_product(self, query: str, product: str, n_results: int = 5) -> list[dict]:
        """
        Search for documents related to a specific product.

        Args:
            query: Search query
            product: Product name filter
            n_results: Number of results

        Returns:
            List of search results
        """
        return self.search(query, n_results, filters={"product": product})
