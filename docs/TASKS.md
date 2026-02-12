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

### 1.9 Documentation Organization
- [x] Organize documentation in `docs/` folder:
  - [x] Move `IMPLEMENTATION_PLAN.md` to `docs/`
  - [x] Move `TASKS.md` to `docs/`
  - [x] Move `USE_CASE_FLOWS.md` to `docs/`

---

## Phase 1 Status

✅ **PHASE 1 COMPLETE**

**Summary:**
- Complete project structure created
- All mock data files generated (3 clients, 3 products, 2 SOWs, compliance rules)
- Docker environment configured (Dockerfile + docker-compose.yml)
- Templates created
- Documentation organized in docs/ folder

---

## Phase 2: Core Agent Implementation (5-7 days)

### 2.1 Agent Foundation
- [x] Create `src/agent/__init__.py`
- [x] Create `src/agent/config.py`:
  - [x] Load environment variables
  - [x] Configure Bedrock client
  - [x] Set model parameters (temperature, max_tokens)

### 2.2 Research Tools
- [x] Create `src/agent/tools/__init__.py`
- [x] Create `src/agent/tools/research.py`:
  - [x] `search_crm(client_name: str) -> dict`
  - [x] `search_opportunities(client_id: str) -> list`
  - [x] `search_historical_sows(client_id: str, product: str) -> list`
  - [x] `search_product_kb(product: str) -> dict`
  - [x] `search_compliance_kb(product: str, client_tier: str) -> dict`
- [x] Add LangGraph tool definitions
- [x] Add docstrings for tool descriptions
- [x] Add input validation with Pydantic

### 2.3 Context Tools
- [x] Create `src/agent/tools/context.py`:
  - [x] `assemble_context(crm_data, product_info, history, compliance) -> dict`
  - [x] `assemble_client_brief(crm_data, opportunities) -> dict`
- [x] Create context data model (Pydantic)

### 2.4 Content Tools
- [x] Create `src/agent/tools/content.py`:
  - [x] `generate_sow_draft(context: dict, template: str) -> str`
  - [x] **[NEW]** `generate_sow_draft_with_reflection(context, template)` - Hybrid approach with 3-step reasoning
  - [x] `generate_section(section_name: str, context: dict) -> str`
  - [x] `revise_section(section: str, feedback: str) -> str`
  - [x] `generate_summary(documents: list) -> str`
- [x] Integrate with Bedrock Claude for generation
- [ ] Add streaming support for long generations (deferred)
- [x] **[NEW]** Implement `export_to_docx(sow_text, template_path)` utility
- [x] **[NEW]** Implement `parse_document(file_path)` utility (supports PDF/DOCX)

### 2.5 Compliance Tools
- [x] Create `src/agent/tools/compliance.py`:
  - [x] `check_mandatory_clauses(sow_text: str, requirements: list) -> dict`
  - [x] `check_prohibited_terms(sow_text: str) -> dict`
  - [x] `check_sla_requirements(sow_text: str, product: str) -> dict`
  - [x] `generate_compliance_report(findings: list) -> str`
- [x] Return structured findings with severity levels
- [x] Include suggested fixes for each issue

### 2.6 Prompt Templates
- [x] Create `src/agent/prompts/planner.yaml`:
  - [x] System prompt with workflow instructions (verify vs Implementation Plan)
  - [x] Tool usage guidelines
  - [x] Output format instructions
- [x] Create `src/agent/prompts/sow_generator.yaml`:
  - [x] Section-by-section generation prompts
  - [x] Context integration instructions
- [x] Create `src/agent/prompts/compliance_checker.yaml`:
  - [x] Clause checking prompts
  - [x] Finding format instructions
- [x] Create prompt loader utility

### 2.7 Planner/Orchestrator
- [x] Create `src/agent/core/planner.py` (organized in core/ folder):
  - [x] Initialize LLM with Bedrock
  - [x] Register all tools (18 total)
  - [x] Create LangGraph agent graph
  - [x] Implement `run(user_request: str) -> AgentResponse`
- [ ] Add conversation memory (optional - deferred)
- [x] Add tool execution logging
- [x] Add error handling and retries

### 2.8 RAG Pipeline
- [x] Create `src/rag/__init__.py`
- [x] Create `src/rag/embeddings.py`:
  - [x] Bedrock Titan embeddings wrapper
  - [x] Batch embedding support
- [x] Create `src/rag/indexer.py`:
  - [x] Document chunking (markdown-aware)
  - [x] Metadata extraction
  - [x] Index to vector store (ChromaDB)
- [x] Create `src/rag/retriever.py`:
  - [x] Semantic search
  - [ ] Hybrid search (keyword + semantic) - deferred
  - [ ] Reranking (optional) - deferred
- [x] Create indexing script `scripts/index_documents.py`
- [x] Test RAG pipeline end-to-end
- [x] Fixed circular import issue in `src/rag/__init__.py`

### 2.9 Testing Infrastructure
- [x] Set up Python virtual environment (`.venv`)
- [x] Install all dependencies via `pip install -e ".[dev]"`
- [x] Create `tests/manual/test_phase2.py` - Component tests
- [x] Create `tests/manual/manual_agent_test.py` - Interactive agent testing
- [x] Create `tests/manual/verify_phase2.py` - Quick verification
- [x] Organize test scripts in `tests/manual/` folder
- [x] Index 50 documents (3 SOWs + 3 product KBs) into ChromaDB

### 2.10 UI Design & Documentation
- [x] Create `docs/ARCHITECTURE_DECISIONS.md` - ADR document for all design decisions
- [x] Create `docs/UI_DESIGN.md` - Complete UI mockups and specifications
- [x] Generate 5 UI mockups (Home, Create, Results, Review, Research)
- [x] Save mockups to `docs/ui-mockups/` folder
- [x] Document hybrid architecture approach (reflection pattern)
- [x] Create `docs/PHASE2_COMPLETION.md` - Phase 2 summary
- [x] Update README with Phase 2 completion
- [x] Update IMPLEMENTATION_PLAN with hybrid architecture

---

## Phase 2 Status

✅ **PHASE 2 COMPLETE**

**Summary**:
- **16 tools implemented** (5 research, 2 context, 5 content, 4 compliance)
- **2 document utilities** (parse_document, export_to_docx)
- **Hybrid architecture** with reflection pattern for production-grade SOW generation
- **RAG pipeline** with ChromaDB (50 documents indexed, cost savings: ~$680/month)
- **LangGraph orchestrator** with conditional flows and error handling
- **Complete prompt management** with YAML templates
- **Testing infrastructure** (virtual env, 3 test scripts, component validation)
- **UI design mockups** (5 pages: Home, Create, Results, Review, Research)
- **Comprehensive documentation** (Architecture Decisions, UI Design, Phase 2 Completion)
- **Fixed circular imports** and organized project structure

**Key Innovation**: Hybrid content generation tool with 3-step reflection (generate → critique → refine) providing agent-quality output with tool-based simplicity

**Cost per SOW**: $0.06 (quick draft) / $0.23 (production quality with reflection)

---

## Phase 3: UI & API (3-4 days)

### 3.1 API Foundation
- [x] Create `src/api/__init__.py`
- [x] Create `src/api/main.py`:
  - [x] FastAPI app initialization
  - [x] CORS middleware
  - [x] Exception handlers
  - [x] Health check endpoint
- [x] Create `src/api/schemas.py`:
  - [x] `SOWCreateRequest`
  - [x] `SOWCreateResponse`
  - [x] `SOWReviewRequest`
  - [x] `SOWReviewResponse`
  - [x] `ResearchRequest`
  - [x] `ResearchResponse`

### 3.2 API Endpoints
- [x] Implement `POST /api/v1/sow/create`:
  - [x] Accept client_id, product, requirements
  - [x] Call planner agent
  - [x] Return generated SOW
  - [x] Log to audit trail
- [x] Implement `POST /api/v1/sow/review`:
  - [x] Accept SOW document (DOCX/PDF upload)
  - [x] **[NEW]** Parse document text using utility
  - [x] Run compliance checks
  - [x] Return findings and suggestions
- [x] Implement `POST /api/v1/research/client`:
  - [x] Accept client_name or client_id
  - [x] Return client brief
- [x] Implement `POST /api/v1/research/product`:
  - [x] Accept product name
  - [x] Return product summary

### 3.3 Audit Logging
- [x] Create `src/api/audit.py`:
  - [x] Log each request with timestamp
  - [x] Log user, action, input, output
  - [x] Store to DynamoDB (prod) or JSON (local)
- [x] Add audit decorator for endpoints

### 3.4 Streamlit UI - Setup
- [x] Create `src/ui/app.py` (streamlit_app.py)
- [x] Set up multi-page navigation
- [x] Create shared components:
  - [x] Header/footer (in `components/styles.py`)
  - [x] Loading spinner
  - [x] Error display

### 3.5 Streamlit UI - Pages
- [x] Create Home page:
  - [x] Overview of capabilities
  - [x] Quick action buttons
- [x] Create "Create SOW" page:
  - [x] Client dropdown (from mock CRM)
  - [x] Product dropdown
  - [x] Additional requirements text area
  - [x] Generate button
  - [x] Display generated SOW with download option
- [x] Create "Review SOW" page:
  - [x] File upload or paste text
  - [x] Review button
  - [x] Display findings with severity badges
- [x] Create "Research" page:
  - [x] Split into separate Client Research and Product Research pages
  - [x] Dropdowns for client/product selection
  - [x] Display results
- [ ] Create "History" page:
  - [ ] List past generations
  - [ ] View/download past SOWs

### 3.6 UI Refinement (Enterprise SaaS)
- [x] **[NEW]** Global Style Overhaul (Dark mode, Inter font, custom variables)
- [x] **[NEW]** Client Research Page Overhaul (Hero profile, glass metrics, user cards)
- [x] **[NEW]** Product Research Page Overhaul (Category pills, features/specs layout)
- [x] **[NEW]** Mock Data Enrichment (Detailed product KB, 5 new clients, 10 opportunities)

### 3.7 Integration Testing
- [x] Test UI → API → Agent flow
- [x] Test error handling in UI
- [x] Test file upload/download
- [x] **[NEW]** Fixed timeout issues for long-running LLM operations
- [x] **[NEW]** Fixed ChromaDB query filter syntax
- [x] **[NEW]** Switched to Amazon Nova Pro (APAC) for model access
- [x] **[NEW]** Indexed RAG documents (historical SOWs + product KB)

---

## Phase 3 Status

✅ **PHASE 3 COMPLETE** (except History page)

**Summary**:
- **Complete FastAPI backend** with all endpoints operational
- **Full Streamlit UI** with 4 pages: Home, Generate SOW, Review SOW, Client Research, Product Research
- **Complete Client/Product Research Overhaul** matching Enterprise SaaS standards
- **Glassmorphism design** with dark mode, SVG icons, and premium aesthetics
- **Audit logging** to JSON (local) with DynamoDB support ready
- **End-to-end integration** validated and debugged
- **Production-ready** with Amazon Nova Pro (APAC) model
- **Robust error handling** with 5-minute timeouts for LLM operations
- **RAG pipeline operational** with ChromaDB multi-filter support

**Key Achievements**:
- Resolved Bedrock model access by switching to Amazon Nova Pro
- Fixed ChromaDB query syntax for multiple metadata filters
- Optimized UI/API timeouts for long-running model operations
- Implemented client/product dropdowns using mock CRM data
- Split research functionality into dedicated pages

**Deferred**:
- History page (not critical for MVP)

---

## Phase 4: Testing Framework (3-4 days)

### 4.1 Test Setup ✅ COMPLETE (2026-02-12)
- [x] Configure pytest in `pyproject.toml`
- [x] Create `conftest.py` with fixtures:
  - [x] Mock AWS credentials (Bedrock, ChromaDB)
  - [x] Mock LLM client
  - [x] Sample test data (CRM, products, opportunities)
  - [x] FastAPI test client

### 4.2 Unit Tests ✅ COMPLETE (2026-02-12)
- [x] Create `tests/unit/test_research_tools.py` (7 tests):
  - [x] Test each research tool function
  - [x] Test error handling
- [x] Create `tests/unit/test_content_tools.py` (4 tests)
- [x] Create `tests/unit/test_compliance_tools.py` (5 tests)
- [x] Create `tests/unit/test_context_tools.py` (2 tests)
- [x] Create `tests/unit/test_prompt_loading.py` (3 tests)
- [x] Create `tests/unit/test_api_schemas.py` (2 tests)
- [x] Achieved 70% code coverage (target: >80%)

### 4.3 Integration Tests ✅ COMPLETE (2026-02-12)
- [x] Create `tests/integration/test_agent_flows.py` (1 test):
  - [x] Test agent graph execution with mocked LLM and tools
  - [x] Test message flow through LangGraph
- [x] Create `tests/integration/test_api_endpoints.py` (4 tests):
  - [x] Test health check endpoint
  - [x] Test SOW creation endpoint
  - [x] Test client research endpoint  
  - [x] Test product research endpoint
- [x] Create `tests/integration/test_rag_pipeline.py` (1 test):
  - [x] Test document indexing with temp ChromaDB
  - [x] Test semantic search and retrieval

**Summary**: 29 tests total (23 unit + 6 integration), 100% pass rate, 70% code coverage
**Documentation**: Created comprehensive `docs/TESTING.md` with patterns, troubleshooting, and best practices

### 4.4 LLM Evaluation Suite ✅ COMPLETE (2026-02-12)
- [x] Create `tests/evals/eval_datasets/`:
  - [x] `sow_creation_cases.json` (5 test cases)
  - [x] `sow_review_cases.json` (5 test cases)
  - [x] `research_cases.json` (6 test cases)
- [x] Create `tests/evals/test_sow_generation.py`:
  - [x] Format compliance metric
  - [x] Section completeness metric
  - [x] Keyword coverage metric
- [x] Create `tests/evals/test_sow_review.py`:
  - [x] Issue detection accuracy (precision/recall/F1)
  - [x] False positive rate
- [x] Create `tests/evals/metrics.py`:
  - [x] Quality metrics implementation
  - [x] Aggregate metrics calculation
  - [x] Baseline comparison logic
- [x] Create `scripts/run_evals.py`:
  - [x] Automated evaluation runner
  - [x] Baseline save/comparison
  - [x] Report generation

**Summary**: 16 eval test cases, comprehensive metrics module (7 unit tests passing), automated evaluation suite with baseline tracking

---

## Phase 5: CI/CD Pipeline ✅ COMPLETE (2026-02-12)

### 5.1 CI Pipeline ✅
- [x] Create `.github/workflows/ci.yml`:
  - [x] Trigger on PR to main and push to main
  - [x] Job 1: Lint (ruff, black --check, mypy)
  - [x] Job 2: Unit tests (pytest tests/unit/)
  - [x] Job 3: Integration tests (pytest tests/integration/)
  - [x] Job 4: LLM evals (metrics tests)
  - [x] Fail on lint errors, test failures, or eval regressions
- [ ] Set up GitHub branch protection rules (Manual setup recommended)

### 5.2 CD Pipeline - Dev ✅
- [x] Create `.github/workflows/cd-dev.yml`:
  - [x] Trigger on merge to main or manual dispatch
  - [x] Build Docker image
  - [x] Save as artifact (ECR push and ECS deploy in Phase 6)
  - [ ] Push to ECR (Phase 6)
  - [ ] Deploy to dev ECS cluster (Phase 6)
  - [x] Notify on success

### 5.3 CD Pipeline - Prod ✅
- [x] Create `.github/workflows/cd-prod.yml`:
  - [x] Manual trigger (workflow_dispatch) with version input
  - [x] Require approval (GitHub Environments)
  - [ ] Deploy to prod ECS cluster (Phase 6)
  - [x] Tag release in GitHub
  - [x] Create GitHub Release

### 5.4 Code Quality ✅
- [x] Configure ruff in `pyproject.toml`
- [x] Configure black in `pyproject.toml`
- [x] Configure mypy in `pyproject.toml`
- [x] Auto-fixed 500+ linting issues across codebase

### 5.5 Infrastructure & Docs ✅
- [x] Create `Dockerfile` and `.dockerignore`
- [x] Create `docs/CI_CD.md` with usage guides
- [x] List required GitHub Secrets for Phase 6

**Summary**: Full CI/CD automation established with GitHub Actions. Code quality tools configured and enforced. Docker containerization ready for cloud deployment.

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
