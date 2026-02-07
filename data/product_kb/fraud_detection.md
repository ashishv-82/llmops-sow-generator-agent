# Cuspac AI Fraud Monitor

## Product Overview

Leveraging Cuspac's unique position across both card (Visa/MC) and NPP payment rails, the AI Fraud Monitor provides a holistic view of financial crime. It combines traditional rules-based engines with advanced machine learning models trained on millions of Australian transaction data points to detect mule accounts, scams, and account takeovers in real-time.

## Key Features

### Cross-Rail Detection
- **Unified Scoring**: Single fraud score for transactions across NPP, Becs, and Cards
- **Scam Detection**: Specialized models for "Authorized Push Payment" (APP) fraud
- **Mule Account Identification**: Network analysis to spot mule accounts receiving funds
- **Behavioral Biometrics**: Device-level signals (typing cadence, giro) via SDK

### Real-Time Intervention
- **NPP Hold/Reject**: Ability to hold suspicious NPP payments for up to 24 hours (as per new rules)
- **Card Blocking**: Instant block of card authorization messages (ISO 8583)
- **Step-Up Auth**: Trigger 2FA/Biometric challenges for risky transactions

### Compliance & Reporting
- **Austrac Reporting**: Automated SMR (Suspicious Matter Report) generation
- **Visa/MC Compliance**: 3DSecure v2.2 data processing
- **Case Management**: Analyst portal for reviewing flagged alerts

## Technical Requirements

| Requirement | Specification |
|-------------|---------------|
| Latency Budget | < 100ms for Scores, < 400ms for Decisions |
| Integration | Async API (Risk Score) or Inline Hook (Blocking) |
| Model Updates | Daily retraining pipeline |
| Data Retention | 7 Years (Austrac compliant storage) |

## Typical Implementation Timeline

| Phase | Duration | Activities |
|-------|----------|------------|
| Data Analysis | 4 weeks | Historic transaction analysis, rule definition |
| Shadow Mode | 4-6 weeks | Running models in parallel, tuning false positives |
| Active Blocking | 2-3 weeks | Gradual rollout of blocking rules (1% -> 100%) |
| Training | 1 week | Fraud analyst training on Case Manager |
| **Total** | **11-14 weeks** | |

## Pricing Model

| Component | Pricing (AUD) |
|-----------|---------------|
| Platform License | $220,000/year (includes Case Manager) |
| Scored Transaction | $0.02 per transaction |
| SMR Generation | $150 per report filed |
| Historical Data Load | $15,000 one-time fee |

## Common Use Cases

1. **APP Scam Prevention**: Stopping elderly customers transferring savings to scammers
2. **Crypto On-Ramp Monitoring**: Detecting high-risk flows to crypto exchanges
3. **First-Party Fraud**: Identifying synthetic identities at onboarding
