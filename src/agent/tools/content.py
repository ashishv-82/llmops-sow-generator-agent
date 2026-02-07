"""
Content generation tools for the SOW Generator agent.

Uses Amazon Bedrock Claude for text generation.
"""

import json
from pathlib import Path
from typing import Annotated, Dict, List

from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool

from src.agent.config import config

# Templates directory
TEMPLATES_DIR = Path(__file__).parent.parent.parent.parent / "data" / "templates"


def _get_llm() -> ChatBedrock:
    """Get configured Bedrock LLM instance."""
    return ChatBedrock(
        model_id=config.bedrock_model_id,
        client=config.bedrock_runtime,
        model_kwargs={
            "temperature": config.temperature,
            "max_tokens": config.max_tokens,
        },
    )


@tool
def generate_sow_draft(
    context: Annotated[Dict, "Context package with client, product, history, compliance"],
    template_name: Annotated[str, "Template to use"] = "standard",
) -> str:
    """
    Generate a complete SOW draft using the provided context.

    Creates all sections including executive summary, scope, deliverables, timeline, pricing, and terms.

    Args:
        context: Context package from assemble_context tool
        template_name: Name of the template to use (default: "standard")

    Returns:
        Complete SOW draft in markdown format
    """
    # Load template
    template_file = TEMPLATES_DIR / f"{template_name}_sow_template.md"
    if not template_file.exists():
        return f"Error: Template '{template_name}' not found"

    template = template_file.read_text()

    # Build system prompt
    system_prompt = """You are an expert SOW (Statement of Work) writer. 
Generate a professional, comprehensive SOW based on the provided context and template.

Key requirements:
- Use formal, professional language
- Include all mandatory compliance clauses
- Base technical details on the product information provided
- Reference similar past SOWs for structure and pricing guidance
- Ensure all sections are complete and specific (no placeholders)
"""

    # Build human prompt
    human_prompt = f"""Generate a complete SOW using this context:

CLIENT INFORMATION:
{json.dumps(context.get('client', {}), indent=2)}

PRODUCT INFORMATION:
{json.dumps(context.get('product', {}), indent=2)}

COMPLIANCE REQUIREMENTS:
{json.dumps(context.get('compliance', {}), indent=2)}

HISTORICAL REFERENCE (similar past SOWs):
{json.dumps(context.get('historical_sows', []), indent=2)}

TEMPLATE STRUCTURE:
{template}

Generate a complete, professional SOW following the template structure."""

    # Generate
    llm = _get_llm()
    messages = [SystemMessage(content=system_prompt), HumanMessage(content=human_prompt)]
    response = llm.invoke(messages)

    return response.content


@tool
def generate_sow_draft_with_reflection(
    context: Annotated[Dict, "Context package with client, product, history, compliance"],
    template_name: Annotated[str, "Template to use"] = "standard",
) -> str:
    """
    Generate a production-grade SOW draft with internal reflection and refinement.
    
    Multi-step process:
    1. Generate initial draft
    2. Self-critique for quality, compliance, and completeness
    3. Revise based on critique
    4. Return polished final SOW
    
    This hybrid approach combines tool simplicity with agent-like reasoning.
    
    Args:
        context: Context package from assemble_context tool
        template_name: Name of the template to use (default: "standard")
    
    Returns:
        Production-grade SOW draft in markdown format
    """
    # Load template
    template_file = TEMPLATES_DIR / f"{template_name}_sow_template.md"
    if not template_file.exists():
        return f"Error: Template '{template_name}' not found"
    
    template = template_file.read_text()
    llm = _get_llm()
    
    # STEP 1: Generate initial draft
    generation_system = """You are an expert SOW (Statement of Work) writer.
Generate a comprehensive, professional SOW based on the provided context.

Key requirements:
- Use formal, professional language
- Include all mandatory compliance clauses  
- Base technical details on product information provided
- Reference similar past SOWs for structure and pricing
- Ensure all sections are complete and specific (no placeholders)
- Be clear about scope boundaries (what's included vs excluded)"""
    
    generation_prompt = f"""Generate a complete SOW using this context:

CLIENT INFORMATION:
{json.dumps(context.get('client', {}), indent=2)}

PRODUCT INFORMATION:
{json.dumps(context.get('product', {}), indent=2)}

COMPLIANCE REQUIREMENTS:
{json.dumps(context.get('compliance', {}), indent=2)}

HISTORICAL REFERENCE (similar past SOWs):
{json.dumps(context.get('historical_sows', []), indent=2)}

TEMPLATE STRUCTURE:
{template}

Generate a complete, professional SOW following the template structure."""
    
    initial_messages = [
        SystemMessage(content=generation_system),
        HumanMessage(content=generation_prompt)
    ]
    initial_draft = llm.invoke(initial_messages).content
    
    # STEP 2: Self-critique
    critique_system = """You are an expert SOW reviewer and compliance auditor.
Analyze the provided SOW draft and identify areas for improvement.

Focus on:
- Missing or incomplete sections
- Compliance gaps (missing mandatory clauses)
- Vague language that should be specific
- Inconsistencies or contradictions
- Professional tone and clarity
- Technical accuracy based on product info"""
    
    critique_prompt = f"""Review this SOW draft:

{initial_draft}

COMPLIANCE REQUIREMENTS TO CHECK:
{json.dumps(context.get('compliance', {}), indent=2)}

Provide a detailed critique covering:
1. What's done well
2. What's missing or needs improvement
3. Specific recommendations for revision

Be constructive but thorough."""
    
    critique_messages = [
        SystemMessage(content=critique_system),
        HumanMessage(content=critique_prompt)
    ]
    critique = llm.invoke(critique_messages).content
    
    # STEP 3: Revise based on critique
    revision_system = """You are an expert SOW writer performing final revision.
Improve the SOW draft based on the detailed critique provided.

Maintain what works well, fix what doesn't, and ensure:
- All mandatory compliance requirements are met
- All sections are complete and professional
- Language is clear, specific, and unambiguous
- The final SOW is production-ready"""
    
    revision_prompt = f"""Revise this SOW draft based on the critique:

ORIGINAL DRAFT:
{initial_draft}

CRITIQUE:
{critique}

Produce the final, polished SOW incorporating all improvements.
Return ONLY the revised SOW, not the critique or commentary."""
    
    revision_messages = [
        SystemMessage(content=revision_system),
        HumanMessage(content=revision_prompt)
    ]
    final_sow = llm.invoke(revision_messages).content
    
    return final_sow


@tool
def generate_section(
    section_name: Annotated[str, "Name of the section to generate"],
    context: Annotated[Dict, "Context information for generation"],
) -> str:
    """
    Generate a specific section of the SOW.

    Useful for regenerating or creating individual sections.

    Args:
        section_name: Name of section (e.g., "Executive Summary", "Scope of Work")
        context: Relevant context for this section

    Returns:
        Generated section content
    """
    system_prompt = f"""You are an expert SOW writer. Generate only the "{section_name}" section.
Be specific, professional, and ensure compliance with requirements."""

    human_prompt = f"""Generate the "{section_name}" section using this context:

{json.dumps(context, indent=2)}

Return only the section content, properly formatted in markdown."""

    llm = _get_llm()
    messages = [SystemMessage(content=system_prompt), HumanMessage(content=human_prompt)]
    response = llm.invoke(messages)

    return response.content


@tool
def revise_section(
    section: Annotated[str, "Current section content"],
    feedback: Annotated[str, "Feedback or issues to address"],
) -> str:
    """
    Revise a section based on feedback or compliance issues.

    Args:
        section: Current section content
        feedback: Description of what needs to be fixed

    Returns:
        Revised section content
    """
    system_prompt = """You are an expert SOW writer. Revise the provided section to address the feedback.
Maintain professional language and ensure compliance."""

    human_prompt = f"""Revise this section:

CURRENT CONTENT:
{section}

FEEDBACK TO ADDRESS:
{feedback}

Return the revised section."""

    llm = _get_llm()
    messages = [SystemMessage(content=system_prompt), HumanMessage(content=human_prompt)]
    response = llm.invoke(messages)

    return response.content


@tool
def generate_summary(documents: Annotated[List[str], "List of documents to summarize"]) -> str:
    """
    Generate a summary of multiple documents.

    Useful for summarizing research results or historical SOWs.

    Args:
        documents: List of document texts

    Returns:
        Summary text
    """
    system_prompt = """You are an expert at summarizing technical and business documents.
Create a concise, accurate summary highlighting key points."""

    combined_docs = "\n\n---\n\n".join(documents)

    human_prompt = f"""Summarize these documents:

{combined_docs}

Provide a clear, structured summary of the key information."""

    llm = _get_llm()
    messages = [SystemMessage(content=system_prompt), HumanMessage(content=human_prompt)]
    response = llm.invoke(messages)

    return response.content
