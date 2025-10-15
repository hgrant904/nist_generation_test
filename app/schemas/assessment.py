from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class AssessmentSessionCreate(BaseModel):
    questionnaire_id: int
    user_id: Optional[str] = None

class AssessmentSessionResponse(BaseModel):
    id: int
    questionnaire_id: int
    user_id: Optional[str] = None
    session_token: str
    status: str
    current_question_id: Optional[int] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    last_activity_at: datetime

    model_config = {"from_attributes": True}

class QuestionResponse(BaseModel):
    id: int
    question_text: str
    question_type: str
    is_required: bool
    options: Optional[List[str]] = None
    question_metadata: Optional[Dict[str, Any]] = None

class ResponseSubmit(BaseModel):
    session_token: str
    question_id: int
    answer_value: str = Field(..., min_length=1)

class ResponseResponse(BaseModel):
    id: int
    session_id: int
    question_id: int
    answer_value: str
    answered_at: datetime

    model_config = {"from_attributes": True}
