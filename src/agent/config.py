"""
Configuration module for the SOW Generator agent.

Loads environment variables and provides shared resources like Bedrock client and ChromaDB.
"""

import os
from pathlib import Path
from typing import Optional

import boto3
import chromadb
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Singleton configuration class for agent resources."""

    _instance: Optional["Config"] = None
    _initialized: bool = False

    def __new__(cls) -> "Config":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialize configuration (only runs once due to singleton pattern)."""
        if self._initialized:
            return

        # AWS Configuration
        self.aws_region = os.getenv("AWS_REGION", "ap-southeast-2")
        self.aws_profile = os.getenv("AWS_PROFILE", "default")
        self.bedrock_model_id = os.getenv(
            "BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20241022-v2:0"
        )

        # Model parameters
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "4096"))

        # Vector store configuration
        self.chroma_persist_dir = os.getenv("CHROMA_PERSIST_DIR", "./data/chromadb")

        # API Configuration
        self.api_host = os.getenv("API_HOST", "0.0.0.0")
        self.api_port = int(os.getenv("API_PORT", "8000"))

        # Logging
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

        # Initialize clients
        self._bedrock_runtime: Optional[boto3.client] = None
        self._chroma_client: Optional[chromadb.Client] = None

        self._initialized = True

    @property
    def bedrock_runtime(self) -> boto3.client:
        """Get or create Bedrock Runtime client."""
        if self._bedrock_runtime is None:
            session = boto3.Session(profile_name=self.aws_profile)
            self._bedrock_runtime = session.client(
                service_name="bedrock-runtime", region_name=self.aws_region
            )
        return self._bedrock_runtime

    @property
    def chroma_client(self) -> chromadb.Client:
        """Get or create ChromaDB client."""
        if self._chroma_client is None:
            # Ensure persist directory exists
            Path(self.chroma_persist_dir).mkdir(parents=True, exist_ok=True)
            self._chroma_client = chromadb.PersistentClient(path=self.chroma_persist_dir)
        return self._chroma_client


# Global config instance
config = Config()
