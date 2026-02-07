# Statement of Work: Real-Time Payments Implementation

**Client:** Acme Financial Services  
**Date:** March 15, 2022  
**SOW Reference:** SOW-2022-001  
**Status:** Executed  

## 1. Executive Summary

This Statement of Work (SOW) outlines the implementation of the Real-Time Payments (RTP) solution for Acme Financial Services ("Client"). The project aims to enable instant domestic transfers for Acme's retail and commercial customers, ensuring compliance with local payment regulations.

## 2. Scope of Work

The scope includes the end-to-end implementation of the RTP platform, integration with Acme's core banking system, and configuration of the payment gateway.

### In Scope
- Deployment of RTP platform in Acme's AWS environment
- Integration with Core Banking System (FIS Profile) via REST API
- Configuration of transaction processing rules and limits
- Implementation of ISO 20022 message formats
- Setup of settlement reporting
- User Acceptance Testing (UAT) support
- Go-live support and hypercare (2 weeks)

### Out of Scope
- Major upgrades to the Core Banking System itself
- Customer-facing mobile app development (API endpoints only provided)
- Hardware procurement

## 3. Deliverables

| ID | Deliverable | Format | Due Date |
|----|-------------|--------|----------|
| D1 | Solution Architecture Document | PDF | Week 3 |
| D2 | API Specification (OpenAPI) | YAML/HTML | Week 4 |
| D3 | Test Strategy & Plan | PDF | Week 5 |
| D4 | Configured RTP Environment (UAT) | Software | Week 10 |
| D5 | Production Deployment | Software | Week 14 |
| D6 | Operational Runbook | PDF | Week 15 |

## 4. Timeline

The project is estimated to take 16 weeks from kickoff to go-live.

- **Phase 1: Discovery & Design** (Weeks 1-4)
- **Phase 2: Build & Integration** (Weeks 5-10)
- **Phase 3: Testing (SIT/UAT)** (Weeks 11-13)
- **Phase 4: Go-Live & Handover** (Weeks 14-16)

## 5. Pricing

This functionality is delivered on a Fixed Price basis for professional services.

| Item | Cost (USD) |
|------|------------|
| Implementation Services | $450,000 |
| Solution Architecture | $50,000 |
| Project Management | $75,000 |
| **Total Services Cost** | **$575,000** |

Licensing fees are billed separately as per the Master Services Agreement (MSA).

## 6. Payment Schedule

- 20% upon Contract Signature
- 30% upon Approval of Design (D1, D2)
- 30% upon Deployment to UAT (D4)
- 20% upon Go-Live Sign-off

## 7. Terms & Conditions

This SOW is governed by the Master Services Agreement signed on Jan 10, 2019.

**Specific Clauses:**
1. **Data Residency**: All customer data must remain within the AU region.
2. **SLA**: System availability requirement is 99.99% during business hours.
3. **Intellectual Property**: Custom integrations belong to the Client; the Platform IP remains with the Vendor.
