# Testing Framework Documentation

## Overview

This document describes the comprehensive testing framework for the SOW Generator Agent, covering unit tests, integration tests, and the RAG pipeline testing strategy.

## Test Suite Summary

### Test Results
- **Total Tests**: 29
- **Pass Rate**: 100% (29/29)
- **Code Coverage**: 70%
- **Test Categories**: Unit Tests (23), Integration Tests (6)

### Test Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── unit/                    # Unit tests for individual components
│   ├── test_api_schemas.py
│   ├── test_compliance_tools.py
│   ├── test_content_tools.py
│   ├── test_context_tools.py
│   ├── test_prompt_loading.py
│   └── test_research_tools.py
├── integration/             # Integration tests for workflows
│   ├── test_agent_flows.py
│   ├── test_api_endpoints.py
│   └── test_rag_pipeline.py
└── manual/                  # Manual testing scripts (excluded from pytest)
    └── manual_agent_test.py
```

## Running Tests

### Prerequisites
Tests must be run using the virtual environment to ensure all dependencies are available:

```bash
# Activate virtual environment (if not already activated)
source .venv/bin/activate

# Or use the venv python directly
.venv/bin/python -m pytest
```

### Basic Test Execution

```bash
# Run all tests
.venv/bin/python -m pytest tests/unit/ tests/integration/

# Run with verbose output
.venv/bin/python -m pytest tests/unit/ tests/integration/ -v

# Run specific test file
.venv/bin/python -m pytest tests/unit/test_research_tools.py

# Run specific test function
.venv/bin/python -m pytest tests/unit/test_research_tools.py::test_search_crm_found
```

### Coverage Reporting

```bash
# Run tests with coverage
.venv/bin/python -m pytest tests/ --cov=src --cov-report=term-missing

# Generate HTML coverage report
.venv/bin/python -m pytest tests/ --cov=src --cov-report=html
# View report at htmlcov/index.html
```

## Test Categories

### Unit Tests (23 tests)

#### API Schemas (`test_api_schemas.py`)
- Validates Pydantic model schemas
- Tests request/response model validation
- Ensures default values are correct

#### Compliance Tools (`test_compliance_tools.py`)
- `test_check_mandatory_clauses_pass/fail`: Validates mandatory clause detection
- `test_check_prohibited_terms_pass/fail`: Tests prohibited term detection
- `test_check_sla_requirements_pass`: Verifies SLA requirement validation

#### Content Tools (`test_content_tools.py`)
- `test_generate_sow_draft`: Tests SOW generation
- `test_generate_section`: Tests individual section generation
- `test_revise_section`: Tests section revision logic
- `test_generate_summary`: Tests document summarization

#### Context Tools (`test_context_tools.py`)
- `test_assemble_context`: Validates context assembly from multiple sources
- `test_assemble_client_brief`: Tests client brief generation

#### Prompt Loading (`test_prompt_loading.py`)
- `test_load_prompt_success`: Tests YAML prompt template loading
- `test_load_prompt_not_found`: Tests error handling for missing prompts
- `test_get_system_prompt`: Validates system prompt retrieval

#### Research Tools (`test_research_tools.py`)
- `test_search_crm_found/not_found`: CRM search functionality
- `test_search_opportunities_found`: Opportunities search
- `test_search_historical_sows`: Historical SOW retrieval
- `test_search_product_kb_mock_file`: Product KB search (file-based)
- `test_search_product_kb_rag_fallback`: Product KB search (RAG-based)
- `test_search_compliance_kb`: Compliance KB search

### Integration Tests (6 tests)

#### Agent Flows (`test_agent_flows.py`)
- `test_agent_graph_execution_flow`: Tests complete LangGraph agent execution with mocked LLM and tool responses

#### API Endpoints (`test_api_endpoints.py`)
- `test_health_check`: Validates health check endpoint
- `test_create_sow_endpoint`: Tests SOW creation API
- `test_research_client_endpoint`: Tests client research API
- `test_research_product_endpoint`: Tests product research API

#### RAG Pipeline (`test_rag_pipeline.py`)
- `test_rag_pipeline_e2e`: End-to-end test of document indexing and retrieval

## Testing Patterns

### 1. Mocking AWS Services

```python
@pytest.fixture
def mock_aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_REGION"] = "us-east-1"

@pytest.fixture
def mock_bedrock_client(mock_aws_credentials):
    with patch("boto3.client") as mock_client:
        mock_bedrock = MagicMock()
        mock_client.return_value = mock_bedrock
        yield mock_bedrock
```

### 2. Mocking LLM Responses

```python
with patch("src.agent.tools.content._get_llm") as mock_get_llm:
    mock_llm = MagicMock()
    mock_llm.invoke.return_value.content = "Generated Content"
    mock_get_llm.return_value = mock_llm
    result = generate_sow_draft.invoke({...})
```

### 3. Testing LangChain Tools

**Important**: LangChain tools created with `@tool` decorator are frozen Pydantic models and don't have a patchable `invoke` method. Patch the underlying function instead:

```python
# ❌ WRONG - This will fail
with patch("src.agent.tools.research.search_crm.invoke", return_value=mock_data):
    ...

# ✅ CORRECT - Patch the .func attribute
with patch("src.agent.tools.research.search_crm.func", return_value=mock_data):
    result = search_crm.invoke({"client_name": "Test"})
```

### 4. Testing FastAPI Endpoints

```python
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_endpoint():
    response = client.post("/api/v1/sow/create", json={...})
    assert response.status_code == 200
    data = response.json()
    assert "sow_text" in data
```

### 5. RAG Pipeline Testing

```python
@pytest.fixture
def temp_chroma_db(tmp_path):
    original_dir = config.chroma_persist_dir
    config.chroma_persist_dir = str(tmp_path / "chroma_test")
    config._chroma_client = None
    yield
    config.chroma_persist_dir = original_dir
    config._chroma_client = None

def test_rag_pipeline_e2e(temp_chroma_db, tmp_path):
    mock_embeddings = MagicMock()
    mock_embeddings.embed_documents.return_value = [[0.1] * 1536]
    
    with patch("src.rag.indexer.BedrockEmbeddings", return_value=mock_embeddings):
        indexer = DocumentIndexer(collection_name="test")
        indexer.index_markdown_file(doc_path)
        
        retriever = DocumentRetriever(collection_name="test")
        results = retriever.search("query")
        assert len(results) > 0
```

## Code Coverage Report

### Overall Coverage: 70%

```
Name                                Stmts   Miss  Cover
---------------------------------------------------------
src/agent/config.py                    43      1    98%
src/agent/core/planner.py              55      7    87%
src/agent/prompts/__init__.py          14      0   100%
src/agent/tools/compliance.py          90     34    62%
src/agent/tools/content.py             67     20    70%
src/agent/tools/context.py             24      0   100%
src/agent/tools/research.py            76      8    89%
src/api/audit.py                       61      9    85%
src/api/dependencies.py                 5      0   100%
src/api/main.py                        28      5    82%
src/api/routes/research_routes.py      60     25    58%
src/api/routes/sow_routes.py           78     45    42%
src/api/schemas.py                     63      0   100%
src/rag/embeddings.py                  21     13    38%
src/rag/indexer.py                     63     15    76%
src/rag/retriever.py                   26      5    81%
---------------------------------------------------------
TOTAL                                 866    264    70%
```

### Coverage Analysis

**High Coverage (>85%)**
- Configuration and initialization
- Research tools
- Agent orchestration (LangGraph)
- API audit logging
- Pydantic schemas

**Medium Coverage (60-85%)**
- Content generation tools
- Compliance checking
- Main API application
- RAG components

**Low Coverage (<60%)**
- API route error handling (sow_routes: 42%, research_routes: 58%)
- Embeddings module (38%)

## Common Issues and Solutions

### Issue 1: Module Import Errors
**Symptom**: `ModuleNotFoundError: No module named 'src'`

**Solution**: Always run tests using the virtual environment:
```bash
.venv/bin/python -m pytest
# OR set PYTHONPATH
PYTHONPATH=. pytest
```

### Issue 2: Tool Invocation Errors
**Symptom**: `AttributeError: 'StructuredTool' object has no attribute 'invoke'`

**Solution**: Patch `tool.func` instead of `tool.invoke`:
```python
with patch("src.agent.tools.research.search_crm.func", return_value=data):
    ...
```

### Issue 3: Manual Tests Executing
**Symptom**: `SystemExit: 1` from manual test files

**Solution**: Configure pytest to exclude manual tests in `pyproject.toml`:
```toml
[tool.pytest.ini_options]
testpaths = ["tests/unit", "tests/integration"]
```

### Issue 4: ChromaDB Persistence Issues
**Symptom**: ChromaDB collection conflicts between tests

**Solution**: Use temporary directories for test ChromaDB instances:
```python
@pytest.fixture
def temp_chroma_db(tmp_path):
    config.chroma_persist_dir = str(tmp_path / "chroma_test")
    config._chroma_client = None
    yield
    # Cleanup
```

## Test Configuration

### pytest Configuration (`pyproject.toml`)

```toml
[tool.pytest.ini_options]
testpaths = ["tests/unit", "tests/integration"]
asyncio_mode = "auto"
```

### Shared Fixtures (`tests/conftest.py`)

The `conftest.py` file provides shared fixtures:
- `mock_aws_credentials`: Mock AWS environment variables
- `mock_bedrock_client`: Mock Bedrock client
- `mock_chroma_client`: Mock ChromaDB client
- `api_client`: FastAPI test client
- Sample data fixtures for CRM, products, and opportunities

## Continuous Integration

### GitHub Actions (Future)

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.12'
      - run: pip install -e .[dev]
      - run: pytest tests/ --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v2
```

## Best Practices

### 1. Test Isolation
- Each test should be independent
- Use fixtures for setup/teardown
- Mock external dependencies (AWS, databases, file I/O)

### 2. Test Naming
- Use descriptive test names: `test_<function>_<scenario>`
- Example: `test_search_crm_not_found`

### 3. Assertions
- Use specific assertions
- Include meaningful error messages
- Test both success and failure cases

### 4. Mocking Strategy
- Mock at the boundary (external services)
- Keep business logic unmocked
- Use `MagicMock` for complex objects

### 5. Coverage Goals
- Aim for >80% overall coverage
- 100% coverage for critical paths (auth, compliance)
- Document reasons for uncovered code

## Future Enhancements

### Phase 4.4: LLM Evaluation Suite
- Create evaluation datasets for SOW generation quality
- Implement automated metrics (correctness, completeness, compliance)
- Add performance benchmarks
- Create regression test suite

### Additional Test Types
1. **Performance Tests**: Load testing for API endpoints
2. **E2E Tests**: Full workflow tests with real AWS services (CI only)
3. **Snapshot Tests**: Regression testing for generated content
4. **Security Tests**: Input validation, injection testing
5. **Contract Tests**: API contract validation

## Troubleshooting

### Tests failing with ChromaDB errors
1. Ensure ChromaDB client is being mocked or using temp directories
2. Reset singleton `config._chroma_client = None` in fixtures

### LLM tool tests failing
1. Verify you're patching `tool.func`, not `tool.invoke`
2. Check that mock return values match expected types
3. Ensure LangChain versions are compatible

### Coverage not showing
1. Install pytest-cov: `pip install pytest-cov`
2. Run with explicit src path: `--cov=src`
3. Check that source files are importable

## References

- [pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [LangChain Testing Guide](https://python.langchain.com/docs/contributing/testing)
- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)

---

**Last Updated**: 2026-02-12  
**Test Suite Version**: 1.0.0  
**Maintained By**: SOW Generator Team
