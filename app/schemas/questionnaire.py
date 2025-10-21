from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class QuestionnaireBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = None
    version: str = "1.0"
    is_active: bool = True

class QuestionnaireCreate(QuestionnaireBase):
    pass

class QuestionnaireUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = None
    version: Optional[str] = None
    is_active: Optional[bool] = None

class QuestionnaireResponse(QuestionnaireBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

class QuestionnaireList(BaseModel):
    items: List[QuestionnaireResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
