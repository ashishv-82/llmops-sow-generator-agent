# CI/CD Pipeline

## Overview

Automated pipelines for code quality, testing, and deployment using GitHub Actions.

## Workflows

### 1. CI Pipeline (`.github/workflows/ci.yml`)

**Trigger:** Every PR to main + push to main

**Jobs:**
1. **Lint & Format Check**
   - Runs `ruff` for linting
   - Runs `black --check` for format validation
   - Runs `mypy` for type checking

2. **Run Tests**
   - Unit tests (`pytest tests/unit/`)
   - Integration tests (`pytest tests/integration/`)
   - Code coverage report (uploaded to Codecov)

3. **LLM Evaluations** (PR only)
   - Runs evaluation metrics tests
   - Comments on PR with results

**Status:** ✅ Active

---

### 2. CD - Dev (`.github/workflows/cd-dev.yml`)

**Trigger:** Push to main OR manual dispatch

**Actions:**
1. Build Docker image (`sow-generator-agent:dev`)
2. Save as artifact
3. Deploy notification

**Future (Phase 6):**
- Push to AWS ECR
- Deploy to ECS dev cluster
- Run smoke tests

**Status:** ✅ Active (Docker build only, AWS deployment in Phase 6)

---

### 3. CD - Production (`.github/workflows/cd-prod.yml`)

**Trigger:** Manual workflow dispatch

**Inputs:**
- `version`: Version tag to deploy (e.g., `v1.0.0`)

**Actions:**
1. Validate version tag
2. Build production Docker image
3. Create GitHub release
4. Deployment notification

**Future (Phase 6):**
- Push to AWS ECR (production)
- Deploy to ECS production cluster
- Run production smoke tests

**Status:** ✅ Active (Docker build + release, AWS deployment in Phase 6)

---

## Running Locally

### Linting
```bash
# Run ruff
ruff check src/ tests/

# Auto-fix issues
ruff check src/ tests/ --fix

# Run black
black src/ tests/

# Check formatting
black --check src/ tests/

# Run mypy
mypy src/ --ignore-missing-imports
```

### Testing
```bash
# Unit tests
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# With coverage
pytest tests/ --cov=src --cov-report=term --cov-report=html
```

### Docker Build
```bash
# Build image
docker build -t sow-generator-agent:local .

# Run container (API)
docker run -p 8000:8000 sow-generator-agent:local

# Run container (UI)
docker run -p 8501:8501 sow-generator-agent:local streamlit run src/ui/app.py
```

---

## GitHub Secrets (For Phase 6)

Required secrets for AWS deployment:

| Secret Name | Purpose | Example Value |
|-------------|---------|---------------|
| `AWS_ACCESS_KEY_ID` | AWS credentials | `AKIA...` |
| `AWS_SECRET_ACCESS_KEY` | AWS credentials | `secret` |
| `AWS_REGION` | AWS region | `us-east-1` |
| `ECR_REPOSITORY` | ECR repository name | `sow-generator` |
| `CODECOV_TOKEN` | Code coverage reporting | `token` (optional) |

**How to add:**
1. Go to repository Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add each secret

---

## Branch Protection Rules

Recommended settings for `main` branch:

✅ **Require a pull request before merging**
- Require approvals: 1
- Dismiss stale pull request approvals

✅ **Require status checks to pass**
- Required checks:
  - `Lint & Format Check`
  - `Run Tests`

✅ **Require branches to be up to date before merging**

✅ **Do not allow bypassing the above settings**

❌ **Do not allow force pushes**

❌ **Do not allow deletions**

**How to configure:**
1. Go to repository Settings → Branches
2. Add branch protection rule for `main`
3. Enable recommended settings above

---

## Code Quality Tools

### Ruff
- Fast Python linter
- Configuration: `[tool.ruff]` in `pyproject.toml`
- Rules: E (errors), F (pyflakes), I (import sorting), N (naming), W (warnings), UP (pyupgrade)

### Black
- Opinionated Python formatter
- Line length: 100 characters
- Configuration: `[tool.black]` in `pyproject.toml`

### MyPy
- Static type checker
- Gradual typing mode (not strict)
- Ignores missing imports
- Configuration: `[tool.mypy]` in `pyproject.toml`

---

## Workflow Status Badges

Add to `README.md`:

```markdown
![CI](https://github.com/ashishv-82/llmops-sow-generator-agent/actions/workflows/ci.yml/badge.svg)
![Deploy to Dev](https://github.com/ashish v-82/llmops-sow-generator-agent/actions/workflows/cd-dev.yml/badge.svg)
```

---

## Troubleshooting

### CI Failing on Lint Errors

**Fix:**
```bash
# Auto-fix most issues
ruff check src/ tests/ --fix
black src/ tests/

# Commit and push
git add .
git commit -m "style: Auto-fix lint issues"
git push
```

### Tests Failing in CI but Passing Locally

**Common causes:**
- Missing dependencies in `pyproject.toml`
- Environment variables not set
- Path issues (use absolute imports)

**Debug:**
1. Check CI logs for error details
2. Run tests in fresh virtual environment locally
3. Ensure all test dependencies are in `[project.optional-dependencies] dev`

### Docker Build Failing

**Common causes:**
- Missing files not in `.dockerignore`
- Build context too large
- Dependency installation issues

**Debug:**
```bash
# Build locally with verbose output
docker build -t test . --progress=plain

# Check image size
docker images | grep sow-generator
```

---

## Next Steps (Phase 6)

1. **AWS ECR Integration**
   - Push Docker images to ECR
   - Tag with commit SHA and version

2. **ECS Deployment**
   - Deploy to Fargate clusters
   - Update task definitions

3. **Smoke Tests**
   - Health check endpoints
   - Basic functionality tests

4. **Monitoring**
   - CloudWatch integration
   - Deployment notifications (Slack/Teams)
