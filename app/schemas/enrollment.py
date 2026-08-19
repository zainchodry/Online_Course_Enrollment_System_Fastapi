from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from models.base import PaymentStatusEnum

# --- Payment Schemas ---
class PaymentResponse(BaseModel):
    id: int
    amount: Decimal
    status: PaymentStatusEnum
    transaction_id: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True

# --- Progress Schemas ---
class LessonProgressResponse(BaseModel):
    id: int
    lesson_id: int
    is_completed: bool
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True

class ProgressUpdate(BaseModel):
    lesson_id: int
    is_completed: bool = True

# --- Enrollment Schemas ---
class EnrollmentCreate(BaseModel):
    course_id: int

class EnrollmentResponse(BaseModel):
    id: int
    course_id: int
    course_title: str
    student_email: str
    enrolled_at: datetime
    is_active: bool
    completed_at: Optional[datetime]
    payment: Optional[PaymentResponse]
    progress: List[LessonProgressResponse] = []

    class Config:
        from_attributes = True