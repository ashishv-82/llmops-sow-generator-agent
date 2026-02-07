"""
Embeddings module for RAG pipeline using Amazon Bedrock Titan.
"""

from typing import List

import boto3

from src.agent.config import config


class BedrockEmbeddings:
    """Wrapper for Bedrock Titan embeddings."""

    def __init__(self, model_id: str = "amazon.titan-embed-text-v2:0") -> None:
        """
        Initialize Bedrock embeddings.

        Args:
            model_id: Bedrock model ID for embeddings
        """
        self.model_id = model_id
        self.client = config.bedrock_runtime

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of documents.

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors
        """
        embeddings = []
        for text in texts:
            embedding = self._embed_single(text)
            embeddings.append(embedding)
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query string.

        Args:
            text: Query text to embed

        Returns:
            Embedding vector
        """
        return self._embed_single(text)

    def _embed_single(self, text: str) -> List[float]:
        """
        Embed a single text string.

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        import json

        body = json.dumps({"inputText": text})

        response = self.client.invoke_model(
            modelId=self.model_id,
            body=body,
            accept="application/json",
            contentType="application/json",
        )

        response_body = json.loads(response["body"].read())
        return response_body["embedding"]
