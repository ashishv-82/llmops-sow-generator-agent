"""RAG module initialization."""

# Note: Import from submodules directly to avoid circular dependencies
# from src.rag.embeddings import BedrockEmbeddings
# from src.rag.indexer import DocumentIndexer
# from src.rag.retriever import DocumentRetriever

__all__ = ["BedrockEmbeddings", "DocumentIndexer", "DocumentRetriever"]
