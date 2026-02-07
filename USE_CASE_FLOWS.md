# SOW Generator - Use Case Flows

This document describes how the agent components work together for each use case.

---

## Agent Components

| Component | Role |
|-----------|------|
| 🧠 **Planner** | Orchestrates workflow, decides tool order |
| 🔍 **Research** | Fetches data from CRM, KB, historical docs |
| 📋 **Context** | Assembles relevant info into coherent package |
| ✍️ **Content** | Generates SOW sections, summaries, text |
| ✅ **Compliance** | Validates output against rules |

---

## Example 1: SOW Creation Flow

**User Request:** *"Create a SOW for Client ABC for the Real-Time Payments product"*

```mermaid
sequenceDiagram
    participant Planner as 🧠 Planner
    participant Research as 🔍 Research
    participant Context as 📋 Context
    participant Content as ✍️ Content
    participant Compliance as ✅ Compliance
    
    Planner->>Planner: Analyze request: Needs client info, past SOWs, product details
    
    Note over Planner, Research: Step 2: Information Gathering
    Planner->>Research: search_crm("ABC")
    Research-->>Planner: Client profile, contacts
    Planner->>Research: search_historical_sows("ABC")
    Research-->>Planner: 2 past SOWs
    Planner->>Research: search_product_kb("Real-Time Payments")
    Research-->>Planner: Product specs
    Planner->>Research: search_compliance_kb("Real-Time Payments")
    Research-->>Planner: Compliance requirements

    Note over Planner, Context: Step 3: Context Assembly
    Planner->>Context: assemble_context(crm, past_sows, product, compliance)
    Context-->>Planner: Structured Context Package

    Note over Planner, Content: Step 4: Content Generation
    Planner->>Content: generate_sow_draft(context, template="standard")
    Content-->>Planner: Full SOW Draft

    Note over Planner, Compliance: Step 5: Compliance Check
    Planner->>Compliance: check_compliance(draft)
    Compliance-->>Planner: Status: WARNING (Missing uptime clause)

    Note over Planner, Content: Step 6: Revision
    Planner->>Content: revise_section("4.2 SLA", fix="Add Service Availability")
    Content-->>Planner: Revised Section

    Planner->>Compliance: Re-check (OK)
    Planner->>Planner: Human Approval Gate
    Planner-->>User: Final SOW ready for SharePoint
```

### Components Used

| Component | Usage |
|-----------|-------|
| Research | ✅ Heavy |
| Context | ✅ Yes |
| Content | ✅ Heavy |
| Compliance | ✅ Yes |

---

## Example 2: SOW Review Flow

**User Request:** *"Review this SOW document for compliance issues"* (upload SOW.docx)

```mermaid
sequenceDiagram
    participant Planner as 🧠 Planner
    participant Research as 🔍 Research
    participant Context as 📋 Context
    participant Compliance as ✅ Compliance
    participant Content as ✍️ Content

    Planner->>Planner: Extract sections from DOCX
    
    Note over Planner, Research: Step 3: Fetch Rules
    Planner->>Research: search_compliance_kb(product)
    Research-->>Planner: Compliance rules
    Planner->>Research: fetch_template("standard_sow")
    Research-->>Planner: Expected structure

    Planner->>Context: assemble_review_context(sections, rules)
    Context-->>Planner: Review Context

    Note over Planner, Compliance: Step 5: Compliance Validation
    Planner->>Compliance: check_structure(sections)
    Compliance-->>Planner: Structure Score
    Planner->>Compliance: check_clauses(sections)
    Compliance-->>Planner: Clause Findings
    Planner->>Compliance: check_risk_language(sections)
    Compliance-->>Planner: Risk Findings
    
    Note over Planner, Content: Step 6: Report Generation
    Planner->>Content: generate_review_report(findings, recommendations)
    Content-->>Planner: Formatted Review Report

    Planner-->>User: Final Review Report with Fixes
```

### Components Used

| Component | Usage |
|-----------|-------|
| Research | ✅ Light |
| Context | ✅ Yes |
| Content | ✅ Light (report) |
| Compliance | ✅ Heavy |

---

## Example 3: Client Research Flow

**User Request:** *"Give me background on Client XYZ before my sales meeting"*

```mermaid
sequenceDiagram
    participant Planner as 🧠 Planner
    participant Research as 🔍 Research
    participant Context as 📋 Context
    participant Content as ✍️ Content

    Planner->>Planner: Analyze request for client background

    Note over Planner, Research: Step 2: Deep Dive Research
    Planner->>Research: search_crm("XYZ")
    Research-->>Planner: Profile & Contacts
    Planner->>Research: search_opportunities("XYZ")
    Research-->>Planner: Pipeline data
    Planner->>Research: search_historical_sows("XYZ")
    Research-->>Planner: Past engagements
    Planner->>Research: search_kyc("XYZ")
    Research-->>Planner: Compliance status

    Note over Planner, Context: Step 3: Synthesis
    Planner->>Context: assemble_client_brief(crm, opps, sows)
    Context-->>Planner: Client Brief data

    Note over Planner, Content: Step 4: Summary Generation
    Planner->>Content: generate_client_summary(brief)
    Content-->>Planner: Executive Summary (Key contacts, history, notes)

    Planner-->>User: "Here is the briefing for Client XYZ..."
```

### Components Used

| Component | Usage |
|-----------|-------|
| Research | ✅ Heavy |
| Context | ✅ Yes |
| Content | ✅ Yes |
| Compliance | ❌ No |

---

## Example 4: Product Research Flow

**User Request:** *"What are the key features and pricing for our Fraud Detection Suite?"*

```mermaid
sequenceDiagram
    participant Planner as 🧠 Planner
    participant Research as 🔍 Research
    participant Context as 📋 Context
    participant Content as ✍️ Content
    
    Planner->>Planner: Analyze request: Needs product and pricing info
    
    Note over Planner, Research: Step 2: Product & Pricing Lookup
    Planner->>Research: search_product_kb("Fraud Detection Suite")
    Research-->>Planner: Technical docs & features
    Planner->>Research: search_pricing_kb("Fraud Detection Suite")
    Research-->>Planner: Pricing models

    Note over Planner, Context: Step 3: Synthesis
    Planner->>Context: assemble_product_brief(docs, pricing)
    Context-->>Planner: Product Brief

    Note over Planner, Content: Step 4: Summary Generation
    Planner->>Content: generate_product_summary(brief)
    Content-->>Planner: Formatted Product Overview

    Planner-->>User: "Fraud Detection Suite features: A, B, C..."
```

### Components Used

| Component | Usage |
|-----------|-------|
| Research | ✅ Heavy |
| Context | ✅ Light |
| Content | ✅ Yes |
| Compliance | ❌ No |

---

## Summary: Component Usage by Use Case

| Use Case | Research | Context | Content | Compliance |
|----------|:--------:|:-------:|:-------:|:----------:|
| **SOW Creation** | ✅ Heavy | ✅ Yes | ✅ Heavy | ✅ Yes |
| **SOW Review** | ✅ Light | ✅ Yes | ✅ Light | ✅ Heavy |
| **Client Research** | ✅ Heavy | ✅ Yes | ✅ Yes | ❌ No |
| **Product Research** | ✅ Heavy | ✅ Light | ✅ Yes | ❌ No |
