# Audit Logging

The SOW Generator includes comprehensive audit logging to track all API requests for compliance, debugging, security, and analytics.

## Overview

Every API request is automatically logged with:
- Timestamp (UTC)
- Endpoint name
- HTTP method
- Request data
- Response summary
- Duration (seconds)
- Status code
- User (placeholder for future authentication)

**Log Format:** JSON Lines (JSONL)  
**Storage:** `data/audit_logs/audit_YYYY-MM-DD.jsonl` (local)  
**Future:** DynamoDB (production)

---

## Why Audit Logging?

### 1. Compliance & Regulatory Requirements 📋

Many industries require audit trails for accountability and legal compliance.

**Compliance Standards:**
- **SOC 2**: Track who accessed what and when
- **GDPR/Privacy Laws**: Log data access for accountability
- **Financial Audits**: Proof of when SOWs were generated

**Use Case:**
```
Client: "Who generated this SOW on January 15th?"
Audit Log: User=john@company.com, Timestamp=2026-01-15T14:23:45Z
```

---

### 2. Debugging & Troubleshooting 🐛

Audit logs serve as a time machine for reproducing issues.

**Example Scenario:**
```
User: "The SOW generated yesterday was wrong!"

Check audit log:
{
  "timestamp": "2026-02-06T08:30:00Z",
  "endpoint": "sow_create",
  "request": {
    "client_id": "CLIENT-001",
    "product": "Real-Time Payments",
    "quality_mode": "production"
  },
  "response_summary": {
    "compliance_score": 85,
    "issues": 2
  },
  "duration_seconds": 34.2,
  "cost_usd": 0.23
}

→ Found the issue: Client tier was MEDIUM instead of HIGH
```

**Without logs:** No way to know what inputs were used ❌  
**With logs:** Exact reproduction and quick fix ✅

---

### 3. Usage Analytics & Optimization 📊

Track system usage patterns to inform optimization decisions.

**Insights from Audit Logs:**
- **Endpoint performance:** Which operations are slowest?
- **Feature usage:** Which endpoints are most popular?
- **Peak times:** When to scale infrastructure?

**Example Analytics:**
```bash
# Average duration by endpoint
cat audit_*.jsonl | jq -s 'group_by(.endpoint) | 
  map({endpoint: .[0].endpoint, avg_duration: (map(.duration_seconds) | add / length)})'

# Result:
[
  {"endpoint": "research_product", "avg_duration": 0.3},
  {"endpoint": "sow_create", "avg_duration": 34.5},
  {"endpoint": "sow_review", "avg_duration": 2.1}
]

→ Insight: sow_create is the bottleneck, optimize first
```

---

### 4. Security & Fraud Detection 🔒

Detect unusual patterns and potential abuse.

**Red Flags:**
- Sudden spike in requests (100/day vs usual 5/day)
- Off-hours activity (SOW generation at 3am)
- Expensive operations overuse (production mode excessive usage)

**Example:**
```json
// Audit log shows suspicious pattern
{"user": "john@company.com", "endpoint": "sow_create", "count": 50, "timeframe": "1 hour"}

→ Action: Investigate potential API abuse, implement rate limiting
```

---

### 5. Cost Tracking & Billing 💰

Track LLM costs per user/team for budgeting and chargeback.

**Cost Attribution:**
```json
{
  "user": "sales-team",
  "endpoint": "sow_create",
  "cost_usd": 0.23,
  "quality_mode": "production"
}
```

**Monthly Cost Report:**
```
Sales Team:    100 SOWs × $0.23 = $23.00
Product Team:   50 SOWs × $0.06 = $3.00
Total LLM Cost:                  $26.00
```

**Benefits:**
- Forecast LLM spending
- Chargeback costs to departments
- Identify cost optimization opportunities

---

### 6. User Behavior Insights 👥

Understand how users interact with the system.

**Questions Answered:**
- Do users prefer quick draft or production quality?
- Do they review SOWs after generation?
- What products are most requested?
- What's the typical workflow?

**Product Decisions:**
```
Analysis: 90% of users select "production" quality mode
Decision: Make production the default, offer quick as opt-in

Analysis: Users rarely call /sow/review separately
Decision: Integrate compliance check into /sow/create response
```

---

## Log Structure

### Example Audit Entry

```json
{
  "timestamp": "2026-02-07T08:30:45Z",
  "endpoint": "sow_create",
  "method": "POST",
  "user": "anonymous",
  "request": {
    "client_id": "CLIENT-001",
    "product": "Real-Time Payments",
    "requirements": "Include migration plan, 6-month timeline",
    "quality_mode": "production"
  },
  "response_summary": {
    "sow_text": "<5234 characters>",
    "generation_time_seconds": 34.2,
    "cost_usd": 0.23,
    "llm_calls": 3,
    "quality_mode": "production"
  },
  "duration_seconds": 34.523,
  "status_code": 200
}
```

**Note:** Large text fields (e.g., `sow_text`) are summarized to prevent huge log files.

---

## Implementation

### How It Works

**Decorator Pattern:**
```python
# src/api/audit.py
from src.api.audit import audit_endpoint

@router.post("/api/v1/sow/create")
@audit_endpoint("sow_create")  # ← Audit decorator
async def create_sow(request: SOWCreateRequest):
    # Endpoint logic
    ...
```

**Automatic Logging:**
1. Request arrives
2. Decorator captures start time
3. Endpoint executes
4. Decorator captures response and duration
5. Log entry written to daily file

**No code changes needed in endpoint logic!**

---

## Querying Audit Logs

### View Today's Logs

```bash
cat data/audit_logs/audit_$(date +%Y-%m-%d).jsonl | jq .
```

### Find Specific Request

```bash
# Find all SOW creations for CLIENT-001
cat audit_*.jsonl | jq 'select(.endpoint == "sow_create" and .request.client_id == "CLIENT-001")'
```

### Performance Analysis

```bash
# Find slow requests (>30 seconds)
cat audit_*.jsonl | jq 'select(.duration_seconds > 30)'
```

### Cost Summary

```bash
# Total LLM cost for the day
cat audit_$(date +%Y-%m-%d).jsonl | jq -s 'map(.response_summary.cost_usd // 0) | add'
```

---

## Real-World Scenarios

### Scenario 1: Debugging Wrong Output

**Problem:**
```
Client: "The SOW you gave us yesterday has incorrect SLA requirements!"
```

**Solution:**
```bash
# Find the SOW generation
cat audit_2026-02-06.jsonl | jq 'select(.endpoint == "sow_create" and .request.client_id == "CLIENT-001")'

# Output shows:
{
  "request": {
    "client_id": "CLIENT-001",
    "product": "Real-Time Payments",
    "quality_mode": "production"
  },
  "response_summary": {
    "compliance_score": 85,
    "issues": ["Missing uptime SLA"]
  }
}

→ Issue identified: Client tier not passed, defaulted to MEDIUM instead of HIGH
→ Regenerate with correct tier
```

---

### Scenario 2: Cost Spike Investigation

**Alert:** LLM costs doubled this month

**Investigation:**
```bash
# Compare request counts
grep "sow_create" audit_2026-01-*.jsonl | wc -l  # January: 100
grep "sow_create" audit_2026-02-*.jsonl | wc -l  # February: 250

# Who's making extra requests?
cat audit_2026-02-*.jsonl | jq -r '.user' | sort | uniq -c | sort -nr

# Output:
150 sales-team
 75 product-team
 25 anonymous

→ Sales team increased usage by 50%
→ Expected: New product launch campaign ✅
```

---

### Scenario 3: Security Incident

**Alert:** Unusual API activity detected

**Analysis:**
```bash
# Check requests from suspicious IP
cat audit_*.jsonl | jq 'select(.user == "external-user")'

# Findings:
{
  "timestamp": "2026-02-07T03:15:00Z",  ← 3am!
  "endpoint": "sow_create",
  "request": {"client_id": "CLIENT-999"} ← Invalid client
}

→ Potential scraping attempt
→ Action: Implement rate limiting, require authentication
```

---

## Production Deployment

### Current: Local JSON Files

**Pros:**
- Simple, no infrastructure needed
- Easy to query with `jq`
- No external dependencies

**Cons:**
- Not scalable for high traffic
- No real-time dashboards
- Manual rotation needed

**Good for:** Development, small deployments (<1000 requests/day)

---

### Future: AWS DynamoDB

**Migration Plan:**
```python
# src/api/audit.py - DynamoDB version

import boto3

class DynamoDBAuditLogger:
    def __init__(self):
        self.table = boto3.resource('dynamodb').Table('sow-audit-logs')
    
    def log_request(self, ...):
        self.table.put_item(Item={
            'timestamp': timestamp,
            'endpoint': endpoint,
            # ... same structure as JSON
        })
```

**Benefits:**
- Automatic scaling
- Real-time queries
- Integrated with CloudWatch
- Long-term retention

**Cost:** ~$1-5/month for typical usage

---

## Compliance Checklist

For enterprise deployments, ensure:

- [x] Audit logs capture timestamp, user, action, input, output
- [x] Logs stored securely (file permissions, encryption at rest)
- [x] Retention policy defined (e.g., 90 days for compliance)
- [ ] User authentication integrated (currently anonymous)
- [ ] PII data handling (mask sensitive fields if needed)
- [ ] Log rotation automated (manual for now)
- [ ] Access controls (who can view audit logs)

---

## Summary

**Audit logging is essential for:**
1. ✅ Compliance (SOC 2, GDPR, audits)
2. ✅ Debugging (reproduce issues)
3. ✅ Analytics (optimize performance)
4. ✅ Security (detect abuse)
5. ✅ Cost tracking (monitor LLM spending)
6. ✅ Product insights (user behavior)

**Trade-off:**
- **Cost:** ~10ms overhead, minimal storage
- **Benefit:** Massive - saves debugging time, prevents legal issues, enables optimization

**Bottom line:** Audit logging is like insurance - you don't need it until you desperately do! 🎯

---

## See Also

- [API Reference](API_REFERENCE.md) - API endpoint documentation
- [Architecture Decisions](ARCHITECTURE_DECISIONS.md) - Why we chose this approach
- [Naming Conventions](NAMING_CONVENTIONS.md) - File naming standards
