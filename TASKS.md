# SOW Generator - Implementation Tasks

A comprehensive checklist for implementing the SOW Generator AI Agent.

---

## Phase 1: Project Setup & Mock Data (3-4 days)

### 1.1 Project Structure
- [x] Create project root with `pyproject.toml`
- [x] Create `.gitignore` for Python/Node/Docker
- [x] Create `.dockerignore` (exclude tests, docs, .git, __pycache__)
- [x] Create `README.md` with project overview and common commands (dev, test, lint, build)

### 1.2 Directory Structure
- [x] Create `src/` directory structure:
  - [x] `src/agent/` - Agent core
  - [x] `src/agent/tools/` - Tool implementations
  - [x] `src/agent/prompts/` - Prompt templates
  - [x] `src/rag/` - RAG pipeline
  - [x] `src/api/` - FastAPI backend
  - [x] `src/ui/` - Streamlit frontend
- [x] Create `data/` directory structure:
  - [x] `data/templates/`
  - [x] `data/historical_sows/`
  - [x] `data/product_kb/`
  - [x] `data/compliance_rules/`
- [x] Create `tests/` directory structure:
  - [x] `tests/unit/`
  - [x] `tests/integration/`
  - [x] `tests/evals/`
- [x] Create `infra/` directory structure:
  - [x] `infra/terraform/`
  - [x] `infra/docker/`
- [x] Create `scripts/` directory
- [x] Create `.github/workflows/` directory

### 1.3 Mock Data - Clients
- [x] Create `data/mock_crm.json` with 3 clients:
  - [x] Client 1: Acme Financial Services (Banking, Enterprise, HIGH compliance)
  - [x] Client 2: TechCorp Industries (Manufacturing, Mid-Market, MEDIUM compliance)
  - [x] Client 3: GlobalRetail Inc (Retail, SMB, LOW compliance)
- [x] Include for each client: id, name, industry, size, contacts, notes, compliance_tier
- [x] Create `data/mock_opportunities.json` with past opportunities per client

### 1.4 Mock Data - Products
- [x] Create `data/product_kb/real_time_payments.md`:
  - [x] Product overview
  - [x] Key features
  - [x] Technical requirements
  - [x] Typical implementation timeline
  - [x] Pricing model
- [x] Create `data/product_kb/fraud_detection.md` (same structure)
- [x] Create `data/product_kb/data_analytics.md` (same structure)

### 1.5 Mock Data - Historical SOWs
- [x] Create `data/historical_sows/SOW-2023-001-acme-payments.md`:
  - [x] Executive Summary
  - [x] Scope of Work
  - [x] Deliverables
  - [x] Timeline
  - [x] Pricing
  - [x] Terms & Conditions
- [x] Create `data/historical_sows/SOW-2023-002-techcorp-fraud.md`
- [ ] Create `data/historical_sows/SOW-2024-001-acme-analytics.md` (To be added later)
- [ ] Create `data/historical_sows/SOW-2024-002-globalretail-payments.md` (To be added later)
- [ ] Create `data/historical_sows/SOW-2024-003-techcorp-analytics.md` (To be added later)

### 1.6 Mock Data - Compliance
- [x] Create `data/compliance_rules/compliance_rules.json`:
  - [x] SLA requirements by compliance tier
  - [x] Data residency clauses
  - [x] Security requirements
  - [x] Liability clauses
- [x] Create `data/compliance_rules/compliance_rules.json` (Consolidated):
  - [x] Banned legal phrases
  - [x] Risky commitments to avoid
  - [x] Ambiguous language patterns

### 1.7 Mock Data - Templates
- [x] Create `data/templates/standard_sow_template.md`:
  - [x] Section headers
  - [x] Placeholder variables
  - [x] Required sections checklist

### 1.8 Development Environment
- [x] Create `infra/docker/Dockerfile`:
  - [x] Python 3.11+ base image
  - [x] Install dependencies
  - [x] Copy source code
  - [x] Set entrypoint
- [x] Create `docker-compose.yml` for local dev:
  - [x] App container
  - [x] Local vector store (ChromaDB)
  - [x] Volume mounts for hot reload
- [x] Create `.env.example` with required env vars
- [ ] Test `make dev` starts local environment (Pending docker build)

---

## Phase 2: Core Agent Implementation (5-7 days)

### 2.1 Agent Foundation
- [ ] Create `src/agent/__init__.py`
- [ ] Create `src/agent/config.py`:
  - [ ] Load environment variables
  - [ ] Configure Bedrock client
  - [ ] Set model parameters (temperature, max_tokens)

### 2.2 Research Tools
- [ ] Create `src/agent/tools/__init__.py`
- [ ] Create `src/agent/tools/research.py`:
  - [ ] `search_crm(client_name: str) -> dict`
  - [ ] `search_opportunities(client_id: str) -> list`
  - [ ] `search_historical_sows(client_id: str, product: str) -> list`
  - [ ] `search_product_kb(product: str) -> dict`
  - [ ] `search_compliance_kb(product: str, client_tier: str) -> dict`
- [ ] Add LangGraph tool definitions
- [ ] Add docstrings for tool descriptions
- [ ] Add input validation with Pydantic

### 2.3 Context Tools
- [ ] Create `src/agent/tools/context.py`:
  - [ ] `assemble_context(crm_data, product_info, history, compliance) -> dict`
  - [ ] `assemble_client_brief(crm_data, opportunities) -> dict`
- [ ] Create context data model (Pydantic)

### 2.4 Content Tools
- [ ] Create `src/agent/tools/content.py`:
  - [ ] `generate_sow_draft(context: dict, template: str) -> str`
  - [ ] `generate_section(section_name: str, context: dict) -> str`
  - [ ] `revise_section(section: str, feedback: str) -> str`
  - [ ] `generate_summary(documents: list) -> str`
- [ ] Integrate with Bedrock Claude for generation
- [ ] Add streaming support for long generations
- [ ] **[NEW]** Implement `export_to_docx(sow_text, template_path)` utility
- [ ] **[NEW]** Implement `parse_document(file_path)` utility (supports PDF/DOCX)

### 2.5 Compliance Tools
- [ ] Create `src/agent/tools/compliance.py`:
  - [ ] `check_mandatory_clauses(sow_text: str, requirements: list) -> dict`
  - [ ] `check_prohibited_terms(sow_text: str) -> dict`
  - [ ] `check_sla_requirements(sow_text: str, product: str) -> dict`
  - [ ] `generate_compliance_report(findings: list) -> str`
- [ ] Return structured findings with severity levels
- [ ] Include suggested fixes for each issue

### 2.6 Prompt Templates
- [ ] Create `src/agent/prompts/planner.yaml`:
  - [ ] System prompt with workflow instructions (verify vs Implementation Plan)
  - [ ] Tool usage guidelines
  - [ ] Output format instructions
- [ ] Create `src/agent/prompts/sow_generator.yaml`:
  - [ ] Section-by-section generation prompts
  - [ ] Context integration instructions
- [ ] Create `src/agent/prompts/compliance_checker.yaml`:
  - [ ] Clause checking prompts
  - [ ] Finding format instructions
- [ ] Create prompt loader utility

### 2.7 Planner/Orchestrator
- [ ] Create `src/agent/planner.py`:
  - [ ] Initialize LLM with Bedrock
  - [ ] Register all tools
  - [ ] Create LangGraph agent graph
  - [ ] Implement `run(user_request: str) -> AgentResponse`
- [ ] Add conversation memory (optional)
- [ ] Add tool execution logging
- [ ] Add error handling and retries

### 2.8 RAG Pipeline
- [ ] Create `src/rag/__init__.py`
- [ ] Create `src/rag/embeddings.py`:
  - [ ] Bedrock Titan embeddings wrapper
  - [ ] Batch embedding support
- [ ] Create `src/rag/indexer.py`:
  - [ ] Document chunking (markdown-aware)
  - [ ] Metadata extraction
  - [ ] Index to vector store
- [ ] Create `src/rag/retriever.py`:
  - [ ] Semantic search
  - [ ] Hybrid search (keyword + semantic)
  - [ ] Reranking (optional)
- [ ] Create indexing script `scripts/index_documents.py`
- [ ] Test RAG pipeline end-to-end

---

## Phase 3: UI & API (3-4 days)

### 3.1 API Foundation
- [ ] Create `src/api/__init__.py`
- [ ] Create `src/api/main.py`:
  - [ ] FastAPI app initialization
  - [ ] CORS middleware
  - [ ] Exception handlers
  - [ ] Health check endpoint
- [ ] Create `src/api/schemas.py`:
  - [ ] `SOWCreateRequest`
  - [ ] `SOWCreateResponse`
  - [ ] `SOWReviewRequest`
  - [ ] `SOWReviewResponse`
  - [ ] `ResearchRequest`
  - [ ] `ResearchResponse`

### 3.2 API Endpoints
- [ ] Implement `POST /api/v1/sow/create`:
  - [ ] Accept client_id, product, requirements
  - [ ] Call planner agent
  - [ ] Return generated SOW
  - [ ] Log to audit trail
- [ ] Implement `POST /api/v1/sow/review`:
  - [ ] Accept SOW document (DOCX/PDF upload)
  - [ ] **[NEW]** Parse document text using utility
  - [ ] Run compliance checks
  - [ ] Return findings and suggestions
- [ ] Implement `POST /api/v1/research/client`:
  - [ ] Accept client_name or client_id
  - [ ] Return client brief
- [ ] Implement `POST /api/v1/research/product`:
  - [ ] Accept product name
  - [ ] Return product summary

### 3.3 Audit Logging
- [ ] Create `src/api/audit.py`:
  - [ ] Log each request with timestamp
  - [ ] Log user, action, input, output
  - [ ] Store to DynamoDB (prod) or JSON (local)
- [ ] Add audit decorator for endpoints

### 3.4 Streamlit UI - Setup
- [ ] Create `src/ui/streamlit_app.py`
- [ ] Set up multi-page navigation
- [ ] Create shared components:
  - [ ] Header/footer
  - [ ] Loading spinner
  - [ ] Error display

### 3.5 Streamlit UI - Pages
- [ ] Create Home page:
  - [ ] Overview of capabilities
  - [ ] Quick action buttons
- [ ] Create "Create SOW" page:
  - [ ] Client dropdown (from mock CRM)
  - [ ] Product dropdown
  - [ ] Additional requirements text area
  - [ ] Generate button
  - [ ] Display generated SOW with download option
- [ ] Create "Review SOW" page:
  - [ ] File upload or paste text
  - [ ] Review button
  - [ ] Display findings with severity badges
- [ ] Create "Research" page:
  - [ ] Tabs for Client / Product research
  - [ ] Search inputs
  - [ ] Display results
- [ ] Create "History" page:
  - [ ] List past generations
  - [ ] View/download past SOWs

### 3.6 Integration Testing
- [ ] Test UI → API → Agent flow
- [ ] Test error handling in UI
- [ ] Test file upload/download

---

## Phase 4: Testing Framework (3-4 days)

### 4.1 Test Setup
- [ ] Configure pytest in `pyproject.toml`
- [ ] Create `conftest.py` with fixtures:
  - [ ] Mock LLM client
  - [ ] Sample test data
  - [ ] API test client

### 4.2 Unit Tests
- [ ] Create `tests/unit/test_research_tools.py`:
  - [ ] Test each research tool function
  - [ ] Test error handling
- [ ] Create `tests/unit/test_content_tools.py`
- [ ] Create `tests/unit/test_compliance_tools.py`
- [ ] Create `tests/unit/test_context_tools.py`
- [ ] Create `tests/unit/test_prompt_loading.py`
- [ ] Create `tests/unit/test_api_schemas.py`
- [ ] Achieve >80% code coverage

### 4.3 Integration Tests
- [ ] Create `tests/integration/test_agent_flows.py`:
  - [ ] Test SOW creation flow end-to-end
  - [ ] Test SOW review flow
  - [ ] Test client research flow
- [ ] Create `tests/integration/test_api_endpoints.py`:
  - [ ] Test each endpoint with mock agent
- [ ] Create `tests/integration/test_rag_pipeline.py`:
  - [ ] Test index → retrieve flow

### 4.4 LLM Evaluation Suite
- [ ] Create `tests/evals/eval_datasets/`:
  - [ ] `sow_creation_cases.json` (5+ test cases, covering different industries)
  - [ ] `sow_review_cases.json` (5+ test cases, including risky clauses)
  - [ ] `research_cases.json` (5+ test cases, for known/unknown entities)
- [ ] Create `tests/evals/test_sow_generation.py`:
  - [ ] Format compliance metric
  - [ ] Section completeness metric
  - [ ] Factual accuracy metric (vs retrieved docs)
- [ ] Create `tests/evals/test_sow_review.py`:
  - [ ] Issue detection accuracy
  - [ ] False positive rate
- [ ] Create `tests/evals/metrics.py`:
  - [ ] Define evaluation metrics
  - [ ] Store baseline results
  - [ ] Compare to baseline
- [ ] Create `scripts/run_evals.py`:
  - [ ] Run full eval suite
  - [ ] Generate report
  - [ ] Flag regressions

---

## Phase 5: CI/CD Pipeline (2-3 days)

### 5.1 CI Pipeline
- [ ] Create `.github/workflows/ci.yml`:
  - [ ] Trigger on PR to main
  - [ ] Job 1: Lint (ruff, black --check, mypy)
  - [ ] Job 2: Unit tests (pytest tests/unit/)
  - [ ] Job 3: Integration tests (pytest tests/integration/)
  - [ ] Job 4: LLM evals (subset for CI)
  - [ ] Fail on lint errors, test failures, or eval regressions
- [ ] Set up GitHub branch protection rules

### 5.2 CD Pipeline - Dev
- [ ] Create `.github/workflows/cd-dev.yml`:
  - [ ] Trigger on merge to main
  - [ ] Build Docker image
  - [ ] Push to ECR
  - [ ] Deploy to dev ECS cluster
  - [ ] Run smoke tests
  - [ ] Notify on Slack/Teams (optional)

### 5.3 CD Pipeline - Prod
- [ ] Create `.github/workflows/cd-prod.yml`:
  - [ ] Manual trigger (workflow_dispatch)
  - [ ] Require approval
  - [ ] Deploy to prod ECS cluster
  - [ ] Run smoke tests
  - [ ] Tag release in GitHub

### 5.4 Code Quality
- [ ] Configure ruff in `pyproject.toml`
- [ ] Configure black in `pyproject.toml`
- [ ] Configure mypy in `pyproject.toml`
- [ ] Create pre-commit hooks (optional)

### 5.5 Secrets Management
- [ ] Add GitHub Secrets:
  - [ ] `AWS_ACCESS_KEY_ID`
  - [ ] `AWS_SECRET_ACCESS_KEY`
  - [ ] `AWS_REGION`
- [ ] Reference secrets in workflows

---

## Phase 6: AWS Deployment (4-5 days)

### 6.1 Terraform Setup
- [ ] Create `infra/terraform/main.tf`:
  - [ ] Terraform version
  - [ ] AWS provider
  - [ ] Backend (S3 for state)
- [ ] Create `infra/terraform/variables.tf`:
  - [ ] Environment (dev/staging/prod)
  - [ ] Region
  - [ ] Container image tag
- [ ] Create `infra/terraform/outputs.tf`
- [ ] **[CRITICAL]** Set up AWS Budget/Billing Alarm (limit ~$100/mo)

### 6.2 Networking
- [ ] Create `infra/terraform/vpc.tf`:
  - [ ] VPC
  - [ ] Public/private subnets
  - [ ] Internet gateway
  - [ ] NAT gateway
  - [ ] Security groups

### 6.3 Compute
- [ ] Create `infra/terraform/ecr.tf`:
  - [ ] ECR repository
  - [ ] Lifecycle policy (retain last 10 images)
- [ ] Create `infra/terraform/ecs.tf`:
  - [ ] ECS cluster
  - [ ] Task definition
  - [ ] Service
  - [ ] Auto-scaling (optional)
- [ ] Create `infra/terraform/alb.tf`:
  - [ ] Application Load Balancer
  - [ ] Target group
  - [ ] Listener rules

### 6.4 API Gateway
- [ ] Create `infra/terraform/api_gateway.tf`:
  - [ ] REST API
  - [ ] Resources and methods
  - [ ] Integration with ALB/ECS
  - [ ] API key (optional)

### 6.5 Data Layer
- [ ] Create `infra/terraform/dynamodb.tf`:
  - [ ] Audit logs table
  - [ ] Indexes
- [ ] Create `infra/terraform/s3.tf`:
  - [ ] Documents bucket
  - [ ] Lifecycle rules
- [ ] Create `infra/terraform/opensearch.tf`:
  - [ ] OpenSearch Serverless collection
  - [ ] Access policies

### 6.6 AI/ML
- [ ] Create `infra/terraform/bedrock.tf`:
  - [ ] Bedrock model access (if IAM needed)
  - [ ] Model invocation role

### 6.7 Security
- [ ] Create `infra/terraform/iam.tf`:
  - [ ] ECS task execution role
  - [ ] ECS task role (Bedrock, DynamoDB, S3, OpenSearch)
  - [ ] Least privilege policies
- [ ] Enable encryption at rest (DynamoDB, S3, OpenSearch)
- [ ] Enable encryption in transit (HTTPS everywhere)

### 6.8 Monitoring
- [ ] Create `infra/terraform/cloudwatch.tf`:
  - [ ] Log groups
  - [ ] Metrics
  - [ ] Alarms (error rate, latency)
  - [ ] Dashboard (optional)

### 6.9 Deployment
- [ ] Initialize Terraform workspaces:
  - [ ] `terraform workspace new dev`
  - [ ] `terraform workspace new staging`
  - [ ] `terraform workspace new prod`
- [ ] Run `terraform plan` for dev
- [ ] Run `terraform apply` for dev
- [ ] Verify deployment works
- [ ] Document runbook for ops

### 6.10 Final Validation
- [ ] Test API Gateway endpoints
- [ ] Test Streamlit UI (if deployed)
- [ ] Verify CloudWatch logs
- [ ] Verify DynamoDB audit entries
- [ ] Run full eval suite against deployed environment
- [ ] Performance/load testing (optional)

---

## Post-Implementation

### Documentation
- [ ] Update README.md with:
  - [ ] Setup instructions
  - [ ] Usage examples
  - [ ] API documentation
- [ ] Create CONTRIBUTING.md
- [ ] Create architecture diagrams (draw.io or Mermaid)

### Handoff
- [ ] Demo to stakeholders
- [ ] Collect feedback
- [ ] Create backlog for v2 features
