# Cuspac CDR & Open Banking (Data Holder/ADR)

## Product Overview

Cuspac's Open Banking suite enables ADIs and Fintechs to participate in the Consumer Data Right (CDR) ecosystem. Whether you are a Data Holder (Bank) needing to comply with ACCC rules, or an Accredited Data Recipient (ADR) wanting to consume data, Cuspac provides the compliant gateway, consent management, and API infrastructure.

## Key Features

### For Data Holders (Compliance)
- **FAPI Compliant Gateway**: Financial Grade API security (OpenID Connect / OAuth 2.0)
- **Consent Dashboard**: ACCC-compliant UI for customers to manage consents
- **Product Reference Data (PRD)**: Public API hosting for banking products
- **Regulatory Reporting**: Automated CTS (GetMetrics) reporting to ACCC

### For Data Recipients (Consumption)
- **Single API Integration**: One API to access data from all Australian banks
- **Data Enrichment**: Transaction categorization and merchant identification (via Basiq)
- **Income Verification**: Instant income/expense analysis for lending decisions
- **Account Verification**: Check account ownership before payments (pay-anyone defense)

## Technical Requirements

| Requirement | Specification |
|-------------|---------------|
| Security standard | FAPI 1.0 Advanced / CIBA |
| Certificate Mgmt | Automated dynamic client registration with ACCC |
| Availability | 99.5% (Non-Customer facing), 99.9% (Customer facing) |
| Hosting | AWS Sydney Region (Data Sovereignty strictness) |

## Typical Implementation Timeline

| Phase | Duration | Activities |
|-------|----------|------------|
| Conformance Testing | 3-4 weeks | Passing ACCC Conformance Test Suite (CTS) |
| Security Review | 2-3 weeks | InfoSec review of FAPI implementation |
| Production Setup | 2 weeks | Key ceremony with ACCC Register |
| Pilot Launch | 2-4 weeks | Testing with "Friendly Consumers" |
| **Total** | **9-13 weeks** | |

## Pricing Model

| Component | Pricing (AUD) |
|-----------|---------------|
| Data Holder Compliance | $180,000/year (Flat fee) |
| ADR Access Platform | $5,000/month + Usage |
| Consent Lifecycle | $2.00 per active consent/month |
| Enrichment API | $0.15 per API call |

## Common Use Cases

1. **Lending Assessment**: Using CDR data to verify income/expenses for loan approval
2. **PFM Apps**: Personal Finance Management apps aggregating bank accounts
3. **Switching Services**: Analyzing transaction history to recommend better energy/telco plans
