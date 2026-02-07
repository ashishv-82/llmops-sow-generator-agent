# SOW Generator AI Agent

A production-grade AI agent for automating Statement of Work (SOW) generation, review, client research, and product research.

## Features

- **SOW Creation**: Generate SOW drafts using templates + context from CRM and knowledge bases
- **SOW Review**: Validate SOWs (DOCX/PDF) against compliance rules and quality criteria
- **Client Research**: Retrieve client history, contacts, and past engagements
- **Product Research**: Search product knowledge bases for features and pricing
- **Document Handling**: Ingest PDF/DOCX and export SOWs to DOCX format

## Tech Stack

| Layer | Technology |
|-------|------------|
| Agent Framework | LangGraph |
| LLM | Amazon Bedrock (Claude 3.5 Sonnet) |
| Vector Store | OpenSearch Serverless (local: ChromaDB) |
| API | FastAPI |
| UI | Streamlit |
| Infrastructure | Terraform + ECS Fargate |

## Project Structure

```
sow-generator/
├── src/
│   ├── agent/          # LangGraph agent + tools
│   ├── rag/            # RAG pipeline
│   ├── api/            # FastAPI backend
│   └── ui/             # Streamlit frontend
├── data/               # Mock data + templates
├── tests/              # Unit, integration, evals
└── infra/              # Terraform + Docker
```

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- AWS CLI configured (for Bedrock access)

### Local Development

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Start local services (ChromaDB)
docker-compose up -d

# Run the API
uvicorn src.api.main:app --reload

# Run the UI (in another terminal)
streamlit run src/ui/streamlit_app.py
```

### Running Tests

```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# All tests with coverage
pytest --cov=src tests/
```

### Linting & Formatting

```bash
# Check code style
ruff check .
black --check .
mypy src/

# Auto-fix
ruff check --fix .
black .
```

### Docker Build

```bash
docker build -t sow-generator .
docker run -p 8000:8000 sow-generator
```

## Environment Variables

Create a `.env` file based on `.env.example`:

```bash
AWS_REGION=ap-southeast-2
AWS_PROFILE=default
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0
```

## Documentation

- [Implementation Plan](IMPLEMENTATION_PLAN.md) - Architecture & design
- [Use Case Flows](USE_CASE_FLOWS.md) - Agent workflow diagrams
- [Tasks](TASKS.md) - Implementation checklist

## License

Internal use only.
