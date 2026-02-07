# Cuspac Real-Time Payments (NPP)

## Product Overview

Cuspac's Real-Time Payments solution provides direct connectivity to Australia's New Payments Platform (NPP), enabling instant 24/7 fund transfers for ADIs and heavy transaction processors. Cuspac acts as a Participating Member, allowing clients to access the NPP infrastructure without the heavy compliance and technical burden of direct connection.

## Key Features

### Core Connectivity
- **NPP Direct Access**: Full access to NPP infrastructure for SCT (Single Credit Transfer)
- **PayID Management**: Create, update, and resolve PayIDs via API
- **PayTo Support**: End-to-end support for Mandate Creation, Amendment, and Payment Initiation
- **Osko Support**: High-speed overlay service for consumer payments

### Operational Features
- **Liquidity Management**: Real-time settlement monitoring with RBA (Reserve Bank of Australia)
- **Stand-In Processing**: Automated approvals during client system downtime
- **Message Transformation**: ISO 20022 mapping from legacy formats (Becs/Direct Entry)
- **Webhook Notifications**: Instant confirmation of inbound/outbound payments

## Technical Requirements

| Requirement | Specification |
|-------------|---------------|
| Connectivity | Private Link (Direct Connect) or mTLS over Internet |
| API Standard | NPP API Framework v5.2 (REST/JSON) |
| Availability | 99.999% Core Uptime |
| TPS Capacity | Tested up to 15,000 TPS |
| Data Center | Active-Active across Sydney & Melbourne zones |

## Typical Implementation Timeline

| Phase | Duration | Activities |
|-------|----------|------------|
| Technical Discovery | 2-3 weeks | Network design, firewall config, key exchange |
| UAT Integration | 4-6 weeks | API integration, ISO 20022 message validation |
| Industry Testing | 4 weeks | NPP Industry Test compatibility certification |
| PVT (Prod Verification) | 2 weeks | Penny drop testing in production |
| Go-Live | 1 week | Ramping up transaction volumes |
| **Total** | **11-16 weeks** | |

## Pricing Model

| Component | Pricing (AUD) |
|-----------|---------------|
| One-time Setup Fee | $85,000 (Standard) / $150,000 (Enterprise) |
| Monthly Platform Fee | $12,500/month |
| Transaction Fee (Tier 1) | $0.08 per msg (< 100k/mo) |
| Transaction Fee (Tier 2) | $0.045 per msg (> 100k/mo) |
| PayTo Mandate Creation | $0.15 per mandate |

## Common Use Cases

1. **Gig Economy Payouts**: Instant wages for rideshare/delivery drivers
2. **Insurance Claims**: Immediate disaster relief funding
3. **Bill Splitting**: Real-time Osko payments for fintech apps
4. **Corporate Treasury**: Just-in-time liquidity management
