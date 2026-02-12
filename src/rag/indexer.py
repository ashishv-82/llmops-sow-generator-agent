"""
Document indexer for RAG pipeline.

Handles chunking and indexing documents to ChromaDB.
"""

import re
from pathlib import Path

from src.agent.config import config
from src.rag.embeddings import BedrockEmbeddings


class DocumentIndexer:
    """Indexes documents into ChromaDB with embeddings."""

    def __init__(self, collection_name: str = "sow_documents") -> None:
        """
        Initialize document indexer.

        Args:
            collection_name: Name of the ChromaDB collection
        """
        self.collection_name = collection_name
        self.embeddings = BedrockEmbeddings()
        self.chroma_client = config.chroma_client

        # Get or create collection
        self.collection = self.chroma_client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "SOW documents and knowledge base"},
        )

    def index_markdown_file(self, file_path: Path, metadata: dict[str, str] | None = None) -> None:
        """
        Index a markdown file with section-aware chunking.

        Args:
            file_path: Path to markdown file
            metadata: Optional metadata to attach to chunks
        """
        content = file_path.read_text(encoding="utf-8")
        chunks = self._chunk_markdown(content)

        # Prepare metadata
        base_metadata = metadata or {}
        base_metadata["source_file"] = str(file_path)
        base_metadata["file_name"] = file_path.name

        # Generate IDs and prepare data
        ids = []
        documents = []
        metadatas = []

        for i, (section, chunk_text) in enumerate(chunks):
            chunk_id = f"{file_path.stem}_{i}"
            ids.append(chunk_id)
            documents.append(chunk_text)

            chunk_metadata = base_metadata.copy()
            chunk_metadata["section"] = section
            chunk_metadata["chunk_index"] = str(i)
            metadatas.append(chunk_metadata)

        # Generate embeddings
        embeddings = self.embeddings.embed_documents(documents)

        # Add to collection
        self.collection.add(
            ids=ids, documents=documents, metadatas=metadatas, embeddings=embeddings
        )

    def _chunk_markdown(self, content: str, max_chunk_size: int = 1000) -> list[tuple[str, str]]:
        """
        Chunk markdown content by sections.

        Args:
            content: Markdown content
            max_chunk_size: Maximum characters per chunk

        Returns:
            List of (section_name, chunk_text) tuples
        """
        chunks = []

        # Split by headers (##, ###, etc.)
        sections = re.split(r"(^#{1,3}\s+.+$)", content, flags=re.MULTILINE)

        current_section = "Introduction"
        current_text = ""

        for part in sections:
            if re.match(r"^#{1,3}\s+", part):
                # This is a header
                if current_text.strip():
                    # Save previous section
                    chunks.extend(
                        self._split_large_chunk(current_section, current_text, max_chunk_size)
                    )
                current_section = part.strip("# ").strip()
                current_text = ""
            else:
                current_text += part

        # Add last section
        if current_text.strip():
            chunks.extend(self._split_large_chunk(current_section, current_text, max_chunk_size))

        return chunks

    def _split_large_chunk(self, section: str, text: str, max_size: int) -> list[tuple[str, str]]:
        """
        Split a large chunk into smaller pieces if needed.

        Args:
            section: Section name
            text: Text content
            max_size: Maximum chunk size

        Returns:
            List of (section, chunk) tuples
        """
        if len(text) <= max_size:
            return [(section, text.strip())]

        # Split by paragraphs
        paragraphs = text.split("\n\n")
        chunks = []
        current_chunk = ""

        for para in paragraphs:
            if len(current_chunk) + len(para) > max_size:
                if current_chunk:
                    chunks.append((section, current_chunk.strip()))
                current_chunk = para
            else:
                current_chunk += "\n\n" + para if current_chunk else para

        if current_chunk:
            chunks.append((section, current_chunk.strip()))

        return chunks

    def clear_collection(self) -> None:
        """Clear all documents from the collection."""
        self.chroma_client.delete_collection(name=self.collection_name)
        self.collection = self.chroma_client.create_collection(
            name=self.collection_name,
            metadata={"description": "SOW documents and knowledge base"},
        )
