# File Naming Conventions

This document outlines the naming conventions used throughout the project to avoid conflicts and improve clarity.

## General Principles

1. **Descriptive Names**: File names should clearly indicate their purpose
2. **No Duplicates**: No two files should have the same name across the project
3. **Suffixes for Context**: Use suffixes to distinguish files with similar purposes in different layers

---

## Agent Layer (`src/agent/`)

### Tools (`src/agent/tools/`)
- **Pattern**: `{domain}.py`
- **Purpose**: Tool implementations (business logic)

**Files:**
- `research.py` - Research tools (CRM, opportunities, historical SOWs, product KB, compliance KB)
- `context.py` - Context assembly tools
- `content.py` - Content generation tools (SOW drafts, sections, summaries)
- `compliance.py` - Compliance checking tools
- `utilities.py` - Document parsing and export utilities

### Core (`src/agent/core/`)
- **Pattern**: `{purpose}.py`

**Files:**
- `planner.py` - LangGraph orchestrator and agent logic

### Prompts (`src/agent/prompts/`)
- **Pattern**: `{purpose}.yaml`

**Files:**
- `planner.yaml` - Planner system prompts
- `sow_generator.yaml` - SOW generation prompts
- `compliance_checker.yaml` - Compliance checking prompts

---

## API Layer (`src/api/`)

### Routes (`src/api/routes/`)
- **Pattern**: `{domain}_routes.py`
- **Purpose**: API endpoint definitions (FastAPI routes)
- **Suffix**: `_routes` to distinguish from tool implementations

**Files:**
- `sow_routes.py` - SOW creation and review endpoints
- `research_routes.py` - Client and product research endpoints

### Core API Files
- `main.py` - FastAPI application initialization
- `schemas.py` - Pydantic request/response models
- `dependencies.py` - Dependency injection utilities
- `audit.py` - Audit logging (to be added in 3.3)

---

## RAG Layer (`src/rag/`)

**Files:**
- `embeddings.py` - Bedrock Titan embeddings wrapper
- `indexer.py` - Document chunking and indexing
- `retriever.py` - Semantic search and retrieval

---

## UI Layer (`src/ui/`)

### Main App
- `app.py` - Main Streamlit application

### Pages (`src/ui/pages/`)
- **Pattern**: `{number}_{emoji}_{name}.py`
- Numbered for sidebar ordering

### Components (`src/ui/components/`)
- **Pattern**: `{component_name}.py`
- Reusable UI components

---

## Scripts (`scripts/`)

**Files:**
- `index_documents.py` - Document indexing utility
- `start_dev.sh` - Development server launcher (to be added)

---

## Tests (`tests/`)

### Manual Tests (`tests/manual/`)
- **Pattern**: `{purpose}.py`

**Files:**
- `test_phase2.py` - Component tests
- `manual_agent_test.py` - Interactive agent testing
- `verify_phase2.py` - Quick verification

### Unit Tests (`tests/unit/`)
- **Pattern**: `test_{module}.py`
- Mirrors source structure

### Integration Tests (`tests/integration/`)
- **Pattern**: `test_{flow}.py`
- End-to-end workflow tests

---

## Why Suffixes?

### Problem (Before):
```
src/agent/tools/research.py          # Research tool implementations
src/api/routes/research.py           # Research API endpoints
```
❌ **Confusing**: Same filename, different purposes

### Solution (After):
```
src/agent/tools/research.py          # Research tool implementations
src/api/routes/research_routes.py    # Research API endpoints
```
✅ **Clear**: Suffix indicates API layer

---

## Import Examples

```python
# Agent tools (business logic)
from src.agent.tools.research import search_crm, search_product_kb
from src.agent.tools.content import generate_sow_draft

# API routes (endpoints)
from src.api.routes.sow_routes import router as sow_router
from src.api.routes.research_routes import router as research_router

# No confusion!
```

---

## Future Additions

When adding new files, follow these patterns:

### New API Routes
```python
# src/api/routes/audit_routes.py
# src/api/routes/admin_routes.py
```

### New Agent Tools
```python
# src/agent/tools/analytics.py
# src/agent/tools/templates.py
```

### New UI Pages
```python
# src/ui/pages/5_📊_Analytics.py
# src/ui/pages/6_⚙️_Settings.py
```

---

This convention ensures clarity and avoids import conflicts! 🎯
