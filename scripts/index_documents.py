#!/usr/bin/env python
"""
Script to index documents into ChromaDB for RAG retrieval.

Indexes:
- Historical SOWs from data/historical_sows/
- Product knowledge base from data/product_kb/
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.rag.indexer import DocumentIndexer


def main() -> None:
    """Index all documents into ChromaDB."""
    print("🔍 Starting document indexing...")

    indexer = DocumentIndexer(collection_name="sow_documents")

    # Clear existing data
    print("🗑️  Clearing existing collection...")
    indexer.clear_collection()

    # Index historical SOWs
    sow_dir = project_root / "data" / "historical_sows"
    if sow_dir.exists():
        print(f"\n📄 Indexing historical SOWs from {sow_dir}...")
        for sow_file in sow_dir.glob("*.md"):
            print(f"  - {sow_file.name}")

            # Extract metadata from filename (e.g., SOW-2023-001-acme-payments.md)
            parts = sow_file.stem.split("-")
            metadata = {
                "doc_type": "historical_sow",
                "year": parts[1] if len(parts) > 1 else "unknown",
            }

            # Try to extract client and product from filename
            if len(parts) >= 4:
                metadata["client_id"] = parts[3] if len(parts) > 3 else "unknown"
                metadata["product"] = parts[4] if len(parts) > 4 else "unknown"

            indexer.index_markdown_file(sow_file, metadata)

    # Index product knowledge base
    product_dir = project_root / "data" / "product_kb"
    if product_dir.exists():
        print(f"\n📚 Indexing product knowledge base from {product_dir}...")
        for product_file in product_dir.glob("*.md"):
            print(f"  - {product_file.name}")

            # Extract product name from filename
            product_name = product_file.stem.replace("_", " ").title()

            metadata = {
                "doc_type": "product_kb",
                "product": product_name,
            }

            indexer.index_markdown_file(product_file, metadata)

    print("\n✅ Indexing complete!")
    print(f"   Collection: {indexer.collection_name}")
    print(f"   Documents indexed: {indexer.collection.count()}")


if __name__ == "__main__":
    main()
