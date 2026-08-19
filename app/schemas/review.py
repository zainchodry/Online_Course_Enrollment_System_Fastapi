from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Rating must be between 1 and 5")
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    course_id: int

class ReviewResponse(ReviewBase):
    id: int
    course_id: int
    course_title: str
    student_name: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True