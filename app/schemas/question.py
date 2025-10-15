from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class BranchingRule(BaseModel):
    condition: str
    next_question_id: Optional[int] = None
    action: str

class QuestionBase(BaseModel):
    question_text: str = Field(..., min_length=1)
    question_type: str = Field(..., pattern="^(text|multiple_choice|yes_no|rating|number)$")
    order_index: int = 0
    is_required: bool = True
    options: Optional[List[str]] = None
    branching_rules: Optional[List[Dict[str, Any]]] = None
    depends_on_question_id: Optional[int] = None
    depends_on_answer: Optional[str] = None
    question_metadata: Optional[Dict[str, Any]] = None

class QuestionCreate(QuestionBase):
    questionnaire_id: int

class QuestionUpdate(BaseModel):
    question_text: Optional[str] = Field(None, min_length=1)
    question_type: Optional[str] = Field(None, pattern="^(text|multiple_choice|yes_no|rating|number)$")
    order_index: Optional[int] = None
    is_required: Optional[bool] = None
    options: Optional[List[str]] = None
    branching_rules: Optional[List[Dict[str, Any]]] = None
    depends_on_question_id: Optional[int] = None
    depends_on_answer: Optional[str] = None
    question_metadata: Optional[Dict[str, Any]] = None

class QuestionResponse(QuestionBase):
    id: int
    questionnaire_id: int

    model_config = {"from_attributes": True}
