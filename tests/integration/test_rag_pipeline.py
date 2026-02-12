import os
import pytest
from unittest.mock import MagicMock, patch
from src.rag.indexer import DocumentIndexer
from src.rag.retriever import DocumentRetriever
from src.agent.config import config

@pytest.fixture
def temp_chroma_db(tmp_path):
    # Override the chroma_persist_dir in config to use a temp dir
    original_dir = config.chroma_persist_dir
    config.chroma_persist_dir = str(tmp_path / "chroma_test")
    
    # Reset singleton client to force recreation with new path
    config._chroma_client = None
    
    yield
    
    # Cleanup
    config.chroma_persist_dir = original_dir
    config._chroma_client = None

def test_rag_pipeline_e2e(temp_chroma_db, tmp_path):
    # Mock Embeddings to return fixed vector
    mock_embedding_instance = MagicMock()
    mock_embedding_instance.embed_documents.return_value = [[0.1] * 1536]
    mock_embedding_instance.embed_query.return_value = [0.1] * 1536
    
    # We need to patch BedrockEmbeddings class in both modules where it is imported/used
    with patch("src.rag.indexer.BedrockEmbeddings", return_value=mock_embedding_instance), \
         patch("src.rag.retriever.BedrockEmbeddings", return_value=mock_embedding_instance):
        
        # 1. Setup Indexer
        indexer = DocumentIndexer(collection_name="test_collection")
        
        # Create a dummy markdown file
        doc_path = tmp_path / "test_doc.md"
        doc_path.write_text("# Test Title\n\nSection content here.", encoding="utf-8")
        
        # Index it
        indexer.index_markdown_file(doc_path, metadata={"source": "test"})
        
        # 2. Setup Retriever
        retriever = DocumentRetriever(collection_name="test_collection")
        
        # Search
        results = retriever.search("content")
        
        # 3. Assert
        assert len(results) > 0
        assert "Section content here" in results[0]["content"]
        assert results[0]["metadata"]["source"] == "test"
