# Architecture Decision Records (ADR)

This document captures all major architectural decisions made during the SOW Generator Agent project development.

---

## Table of Contents

1. [ADR-001: Vector Store Selection - ChromaDB vs OpenSearch](#adr-001-vector-store-selection)
2. [ADR-002: Agent Architecture - Tool-Based vs Multi-Agent](#adr-002-agent-architecture)
3. [ADR-003: Hybrid Content Generation with Reflection Pattern](#adr-003-hybrid-content-generation)
4. [ADR-004: LLM Provider - Amazon Bedrock](#adr-004-llm-provider)
5. [ADR-005: Prompt Management - YAML Templates](#adr-005-prompt-management)

---

## ADR-001: Vector Store Selection

**Status**: ✅ Accepted  
**Date**: 2026-02-07  
**Decision Makers**: Development Team

### Context

SOW Generator needs semantic search over historical SOWs and product documentation (RAG pipeline). Need to choose between:
- **AWS OpenSearch Serverless** (managed, AWS-native)
- **ChromaDB** (open-source, local)
- **Pinecone** (managed, specialized)

### Decision

**Use ChromaDB for local development and initial production; migrate to OpenSearch Serverless for AWS deployment if needed.**

### Rationale

**Cost Analysis**:
- OpenSearch Serverless: ~$700/month minimum (OCU charges)
- ChromaDB: $0 (self-hosted) + minimal EC2/ECS costs
- **Savings**: ~$680/month with ChromaDB

**Development Benefits**:
- ✅ Local development without AWS costs
- ✅ Faster iteration (no network latency)
- ✅ Offline capable
- ✅ Simple setup (pip install)

**Production Viability**:
- ✅ Persistent storage (file-based)
- ✅ Proven performance for <1M vectors
- ✅ Expected dataset: ~500-1000 documents
- ✅ Can migrate to OpenSearch later if needed

**Trade-offs Accepted**:
- ❌ Manual scaling vs auto-scaling
- ❌ No AWS-native integration benefits
- ❌ Need to manage backups manually

### Consequences

**Positive**:
- Significant cost savings for MVP
- Faster development cycle
- Simpler local testing

**Negative**:
- May need migration to OpenSearch for multi-region
- Need to implement backup strategy
- Less integration with AWS observability tools

**Migration Path**:
If/when needed, both use embeddings + vector similarity, so migration is:
1. Export ChromaDB vectors
2. Re-index in OpenSearch
3. Update retriever connection string

---

## ADR-002: Agent Architecture

**Status**: ✅ Accepted  
**Date**: 2026-02-07  
**Decision Makers**: Development Team

### Context

Need to choose between:
- **Tool-Based Architecture**: One orchestrator agent + multiple tools
- **Multi-Agent Architecture**: Multiple specialized agents (Researcher, Content Creator, Compliance, etc.)

### Decision

**Use tool-based architecture with single orchestrator and 18 specialized tools.**

### Rationale

**Enterprise Requirements**:
- ✅ Internal data only (no internet search)
- ✅ Well-defined workflows (SOW generation is templated)
- ✅ Auditability critical (single execution path)
- ✅ Cost-sensitive (budget approval needed)

**Tool-Based Advantages**:
| Criterion | Tool-Based | Multi-Agent |
|-----------|------------|-------------|
| **Auditability** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Cost per SOW** | $0.08-0.23 | $0.50-1.00 |
| **Latency** | 15-35s | 60-120s |
| **Debugging** | Easy | Complex |
| **LLM Calls** | 1-3 | 10-20 |

**Use Case Fit**:
- Research: Simple data fetches (CRM, docs) → Tools perfect
- Content: Template-based generation → Tools sufficient
- Compliance: Rule checking → Tools ideal

**When Multi-Agent Would Be Better**:
- ❌ Unknown/exploratory workflows
- ❌ Complex negotiation between agents
- ❌ Highly creative, non-templated outputs

### Consequences

**Positive**:
- Clear execution paths for auditing
- Lower operational costs
- Easier to onboard new developers
- Simpler testing strategy

**Negative**:
- Less flexibility for complex reasoning
- Tools can't collaborate/negotiate
- Single point of decision-making

**Mitigation**:
- See ADR-003 for quality enhancement via reflection

---

## ADR-003: Hybrid Content Generation

**Status**: ✅ Accepted  
**Date**: 2026-02-07  
**Decision Makers**: Development Team

### Context

Within tool-based architecture (ADR-002), need higher quality for production SOWs while maintaining simplicity. Options:
- **Simple generation**: Single LLM call
- **Full multi-agent**: Separate agents for generation/review
- **Hybrid reflection**: Tool with multi-step internal reasoning

### Decision

**Implement hybrid approach: Provide both simple and reflection-based content generation tools.**

### Tools Provided

**1. `generate_sow_draft()` - Simple Generation**
- Single LLM call
- Cost: ~$0.08
- Time: ~15 seconds
- Use: Development, testing, standard templates

**2. `generate_sow_draft_with_reflection()` - Production Quality**
- Three LLM calls with reflection pattern:
  1. **Generate**: Initial comprehensive draft
  2. **Critique**: Self-review for compliance, quality, completeness
  3. **Refine**: Final polished version
- Cost: ~$0.23
- Time: ~35 seconds  
- Use: Client-facing, high-value deals

### Rationale

**Quality Benefits of Reflection**:
- ✅ Self-correcting (catches own mistakes)
- ✅ Compliance-aware (dedicated review step)
- ✅ Professional output (multiple passes)
- ✅ Production-ready (no placeholders)

**Cost-Benefit Analysis**:
- Extra cost: $0.15 per SOW
- Extra time: +20 seconds
- Quality gain: Significant
- ROI: Excellent for $100K+ deals

**Why Not Full Multi-Agent**:
- 3 calls vs 10-20 calls (67% cheaper)
- Sequential vs coordination overhead
- Same quality improvement as multi-agent
- Simpler to debug and test

### Consequences

**Positive**:
- Best of both worlds: simplicity + quality
- Users can choose based on urgency vs quality
- 90% of multi-agent quality at 30% of complexity
- Agent can auto-select based on deal value

**Negative**:
- Need to maintain two code paths
- Users need to understand when to use which

**Usage Recommendation**:
```python
if deal_value > 100_000 or client_tier == "HIGH":
    use generate_sow_draft_with_reflection
else:
    use generate_sow_draft
```

---

## ADR-004: LLM Provider

**Status**: ✅ Accepted  
**Date**: 2026-02-07  
**Decision Makers**: Development Team

### Context

Need to select LLM provider for SOW generation. Options:
- **Amazon Bedrock** (AWS-native)
- **OpenAI API** (direct)
- **Azure OpenAI** (Microsoft)

### Decision

**Use Amazon Bedrock with Claude 3.5 Sonnet v2.**

### Rationale

**Model Selection**:
- Claude 3.5 Sonnet v2: `anthropic.claude-3-5-sonnet-20241022-v2:0`
- Best for professional writing
- Strong instruction following
- Good context window (200K tokens)

**Why Bedrock Over Direct APIs**:
- ✅ AWS-native (same account, IAM, VPC)
- ✅ No separate API key management
- ✅ AWS compliance/security posture
- ✅ Integrated billing
- ✅ Pay-as-you-go (no subscription)

**Why Claude Over GPT**:
- ✅ Better for long-form professional content
- ✅ More concise, less verbose
- ✅ Stronger at following complex instructions
- ✅ Available in Bedrock (same reasoning as above)

**Cost Comparison** (per 1M tokens):
- Claude 3.5 Sonnet: $3 input / $15 output
- GPT-4: $30 input / $60 output
- **Savings**: 90% with Claude

### Consequences

**Positive**:
- AWS-native simplifies deployment
- Lower costs than GPT-4
- High-quality professional writing
- No vendor lock-in (can swap models)

**Negative**:
- AWS account required (not an issue for enterprise)
- Region availability considerations
- Claude may not be ideal for all tasks (but good for SOWs)

**Configuration**:
```python
model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0"
temperature = 0.7  # Balanced creativity/consistency
max_tokens = 4096  # Sufficient for SOW sections
```

---

## ADR-005: Prompt Management

**Status**: ✅ Accepted  
**Date**: 2026-02-07  
**Decision Makers**: Development Team

### Context

Need structured way to manage prompts. Options:
- **Hardcoded strings** in Python
- **YAML files** with versioning
- **Database-driven** prompts
- **External prompt management service** (e.g., Anthropic Console)

### Decision

**Use YAML files for prompt templates with versioning.**

### Structure

```yaml
name: planner
version: "1.0.0"
description: Main orchestrator prompt

system_prompt: |
  You are an AI assistant that helps create SOWs...
  [detailed prompt]
```

Files:
- `src/agent/prompts/planner.yaml` - Main orchestrator
- `src/agent/prompts/sow_generator.yaml` - Content generation
- `src/agent/prompts/compliance_checker.yaml` - Validation rules

### Rationale

**Why YAML**:
- ✅ Human-readable and editable
- ✅ Version control friendly (git diff)
- ✅ Supports multi-line strings naturally
- ✅ Structured metadata (name, version, description)
- ✅ No special tooling needed

**Why Not Hardcoded**:
- ❌ Hard to read in code
- ❌ Difficult to A/B test
- ❌ No version tracking
- ❌ Requires code changes for prompt updates

**Why Not Database**:
- ❌ Overkill for current scale
- ❌ Adds dependency
- ❌ Harder to version control
- ❌ Less transparent

**Why Not External Service**:
- ❌ Network dependency
- ❌ Additional cost
- ❌ Vendor lock-in
- ❌ Not needed for current complexity

### Consequences

**Positive**:
- Easy prompt iteration
- Clear version history via git
- Can A/B test by version
- Non-developers can edit prompts
- Supports multiple prompt versions simultaneously

**Negative**:
- File I/O on every load (mitigated with caching)
- No GUI for prompt management
- Manual version bumping

**Future Enhancement**:
```python
# Could add prompt versioning
load_prompt("planner", version="2.0.0")

# Could add A/B testing
load_prompt("planner", variant="experimental")
```

---

## ADR-006: Tool Organization

**Status**: ✅ Accepted  
**Date**: 2026-02-07  
**Decision Makers**: Development Team

### Context

With 18 tools, need clear organizational structure. Options:
- **Flat structure**: All tools in one file
- **Functional grouping**: Separate files by purpose
- **Agent-based grouping**: Files mimicking potential agents

### Decision

**Use functional grouping with 4 tool files:**
- `research.py` - Data fetching tools (5 tools)
- `context.py` - Data assembly tools (2 tools)
- `content.py` - Generation tools (5 tools)
- `compliance.py` - Validation tools (4 tools)
- `utils/doc_handler.py` - Document utilities (2 functions)

### Rationale

**Advantages**:
- ✅ Clear separation of concerns
- ✅ Easy to find relevant tools
- ✅ Can import groups: `from tools.research import *`
- ✅ Aligns with original "4 tool groups" design
- ✅ Supports future modularization

**File Sizes**:
- Each file: 150-250 lines
- Manageable, not overwhelming
- Related functionality co-located

### Consequences

**Positive**:
- Clear mental model
- Easy onboarding for new developers
- Supports testing by group
- Can deploy groups independently (future)

**Negative**:
- Cross-dependencies need management
- Import paths slightly longer

**Package Structure**:
```
src/agent/tools/
├── __init__.py          # Exports ALL_TOOLS (18 tools)
├── research.py          # 5 research tools
├── context.py           # 2 context assembly tools
├── content.py           # 5 content generation tools
└── compliance.py        # 4 compliance validation tools
```

---

## Summary of Key Decisions

| Decision | Choice | Primary Rationale |
|----------|--------|-------------------|
| **Vector Store** | ChromaDB | Cost savings ($680/month) |
| **Architecture** | Tool-Based | Auditability + enterprise fit |
| **Content Quality** | Hybrid Reflection | Quality without multi-agent complexity |
| **LLM Provider** | AWS Bedrock (Claude) | AWS-native + cost-effective |
| **Prompt Management** | YAML Files | Version control + transparency |
| **Tool Organization** | Functional Groups | Clarity + maintainability |

---

## Decision Review Process

These decisions should be reviewed:
- **Quarterly**: Vector store (cost/performance monitoring)
- **Semi-annually**: Architecture pattern (as use cases evolve)
- **As needed**: LLM provider (new models, pricing changes)
- **Monthly**: Prompt effectiveness (quality metrics)

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-07 | Initial ADR document created |

---

*This document follows the Architecture Decision Record (ADR) format to maintain transparency and rationale for future team members.*
