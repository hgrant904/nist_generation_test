#!/usr/bin/env python3
"""
Example workflow demonstrating the questionnaire engine API usage.
This script creates a sample NIST security questionnaire and simulates an assessment.
"""

import requests
import json
from typing import Optional

BASE_URL = "http://localhost:8000"

def print_section(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def create_questionnaire():
    print_section("Creating Questionnaire")
    
    response = requests.post(
        f"{BASE_URL}/api/questionnaires/",
        json={
            "title": "NIST 800-53 Access Control Assessment",
            "description": "Security assessment focusing on access control measures",
            "category": "security",
            "version": "1.0"
        }
    )
    
    questionnaire = response.json()
    print(f"Created questionnaire: {questionnaire['title']}")
    print(f"ID: {questionnaire['id']}")
    return questionnaire['id']

def create_questions(questionnaire_id: int):
    print_section("Creating Questions with Branching Logic")
    
    questions = [
        {
            "questionnaire_id": questionnaire_id,
            "question_text": "Does your organization have a formal access control policy?",
            "question_type": "yes_no",
            "order_index": 0,
            "is_required": True,
            "question_metadata": {
                "nist_control": "AC-1",
                "category": "policy"
            }
        },
        {
            "questionnaire_id": questionnaire_id,
            "question_text": "How many users have administrative access?",
            "question_type": "number",
            "order_index": 1,
            "is_required": True,
            "depends_on_question_id": 1,
            "depends_on_answer": "yes",
            "question_metadata": {
                "nist_control": "AC-2",
                "category": "account_management"
            }
        },
        {
            "questionnaire_id": questionnaire_id,
            "question_text": "Do you implement multi-factor authentication?",
            "question_type": "yes_no",
            "order_index": 2,
            "is_required": True,
            "question_metadata": {
                "nist_control": "IA-2",
                "category": "authentication"
            }
        },
        {
            "questionnaire_id": questionnaire_id,
            "question_text": "What authentication methods do you use?",
            "question_type": "multiple_choice",
            "order_index": 3,
            "is_required": True,
            "options": [
                "Password only",
                "Password + SMS",
                "Password + Authenticator App",
                "Hardware Token",
                "Biometric"
            ],
            "depends_on_question_id": 3,
            "depends_on_answer": "yes",
            "question_metadata": {
                "nist_control": "IA-2(1)",
                "category": "authentication"
            }
        },
        {
            "questionnaire_id": questionnaire_id,
            "question_text": "How often do you review user access rights?",
            "question_type": "multiple_choice",
            "order_index": 4,
            "is_required": True,
            "options": [
                "Weekly",
                "Monthly",
                "Quarterly",
                "Annually",
                "Never"
            ],
            "question_metadata": {
                "nist_control": "AC-2(7)",
                "category": "account_management"
            }
        }
    ]
    
    question_ids = []
    for q in questions:
        response = requests.post(f"{BASE_URL}/api/questions/", json=q)
        question = response.json()
        question_ids.append(question['id'])
        print(f"Created Q{len(question_ids)}: {question['question_text'][:50]}...")
        
        if question.get('depends_on_question_id'):
            print(f"  └─ Depends on Q{question['depends_on_question_id']} = '{question['depends_on_answer']}'")
    
    return question_ids

def start_assessment(questionnaire_id: int) -> str:
    print_section("Starting Assessment Session")
    
    response = requests.post(
        f"{BASE_URL}/api/assessments/start",
        json={
            "questionnaire_id": questionnaire_id,
            "user_id": "demo_user_123"
        }
    )
    
    session = response.json()
    print(f"Session created: {session['session_token']}")
    print(f"Status: {session['status']}")
    return session['session_token']

def conduct_assessment(session_token: str):
    print_section("Conducting Assessment")
    
    question_count = 0
    
    while True:
        response = requests.get(
            f"{BASE_URL}/api/assessments/sessions/{session_token}/next-question"
        )
        
        question = response.json()
        
        if question is None:
            print("\n✓ Assessment completed - no more questions")
            break
        
        question_count += 1
        print(f"\nQuestion {question_count}: {question['question_text']}")
        print(f"Type: {question['question_type']}")
        
        if question['options']:
            print("Options:")
            for i, option in enumerate(question['options'], 1):
                print(f"  {i}. {option}")
        
        answer = get_simulated_answer(question)
        print(f"Answer: {answer}")
        
        submit_response = requests.post(
            f"{BASE_URL}/api/assessments/responses",
            json={
                "session_token": session_token,
                "question_id": question['id'],
                "answer_value": answer
            }
        )
        
        if submit_response.status_code != 201:
            print(f"Error submitting response: {submit_response.text}")
            break

def get_simulated_answer(question: dict) -> str:
    """Simulate user answers based on question type"""
    question_type = question['question_type']
    
    if question_type == 'yes_no':
        return 'yes'
    elif question_type == 'number':
        return '5'
    elif question_type == 'multiple_choice':
        return question['options'][2] if len(question['options']) > 2 else question['options'][0]
    else:
        return 'Sample text answer'

def view_results(session_token: str):
    print_section("Assessment Results")
    
    session_response = requests.get(
        f"{BASE_URL}/api/assessments/sessions/{session_token}"
    )
    session = session_response.json()
    
    print(f"Session Status: {session['status']}")
    print(f"Started: {session['started_at']}")
    print(f"Completed: {session['completed_at']}")
    
    responses_response = requests.get(
        f"{BASE_URL}/api/assessments/sessions/{session_token}/responses"
    )
    responses = responses_response.json()
    
    print(f"\nTotal Responses: {len(responses)}")
    print("\nAnswers:")
    for i, resp in enumerate(responses, 1):
        print(f"  {i}. Question ID {resp['question_id']}: {resp['answer_value']}")

def main():
    print_section("NIST Questionnaire Engine - Example Workflow")
    print("This script demonstrates the complete questionnaire workflow.")
    print("Make sure the API server is running at http://localhost:8000")
    
    try:
        health_check = requests.get(f"{BASE_URL}/health")
        if health_check.status_code != 200:
            print("❌ API server is not responding")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server at http://localhost:8000")
        print("Please start the server with: uvicorn app.main:app --reload")
        return
    
    questionnaire_id = create_questionnaire()
    
    question_ids = create_questions(questionnaire_id)
    
    session_token = start_assessment(questionnaire_id)
    
    conduct_assessment(session_token)
    
    view_results(session_token)
    
    print_section("Workflow Complete")
    print("✓ Created questionnaire with branching logic")
    print("✓ Completed assessment with dependency resolution")
    print("✓ Recorded all responses with transactional integrity")
    print("\nView the full API documentation at: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
