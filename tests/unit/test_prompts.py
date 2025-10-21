import pytest
from src.prompts.system_prompts import (
    get_system_prompt_with_context,
    format_questionnaire_context,
    NIST_CSF_SYSTEM_PROMPT,
)


def test_get_system_prompt_without_context():
    prompt = get_system_prompt_with_context()
    assert prompt == NIST_CSF_SYSTEM_PROMPT
    assert "cybersecurity advisor" in prompt.lower()
    assert "NIST" in prompt


def test_get_system_prompt_with_context():
    context = "User uses Microsoft 365"
    prompt = get_system_prompt_with_context(context)
    
    assert NIST_CSF_SYSTEM_PROMPT in prompt
    assert context in prompt
    assert "CONTEXT FROM PREVIOUS QUESTIONNAIRE RESPONSES" in prompt


def test_format_questionnaire_context_empty():
    context = format_questionnaire_context([])
    assert context == ""


def test_format_questionnaire_context_single_response():
    responses = [
        {
            "category": "Cloud Services",
            "question": "Do you use cloud services?",
            "answer": "Yes, Microsoft 365",
        }
    ]
    
    context = format_questionnaire_context(responses)
    assert "Cloud Services" in context
    assert "Do you use cloud services?" in context
    assert "Yes, Microsoft 365" in context


def test_format_questionnaire_context_multiple_responses():
    responses = [
        {
            "category": "Cloud Services",
            "question": "Do you use cloud services?",
            "answer": "Yes, Microsoft 365",
        },
        {
            "category": "Data Backup",
            "question": "Do you have backups?",
            "answer": "Daily backups to external drive",
        }
    ]
    
    context = format_questionnaire_context(responses)
    assert "Cloud Services" in context
    assert "Data Backup" in context
    assert "Microsoft 365" in context
    assert "Daily backups" in context
