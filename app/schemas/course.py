from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

# --- Category Schemas ---
class CategoryBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    slug: str

    class Config:
        from_attributes = True

# --- Lesson Schemas ---
class LessonBase(BaseModel):
    title: str = Field(..., max_length=200)
    content: Optional[str] = None
    video_url: Optional[str] = None
    order: int = 0
    is_free_preview: bool = False

class LessonCreate(LessonBase):
    module_id: int

class LessonResponse(LessonBase):
    id: int

    class Config:
        from_attributes = True

# --- Module Schemas ---
class ModuleBase(BaseModel):
    title: str = Field(..., max_length=200)
    order: int = 0

class ModuleCreate(ModuleBase):
    course_id: int

class ModuleResponse(ModuleBase):
    id: int
    lessons: List[LessonResponse] = []

    class Config:
        from_attributes = True

# --- Course Schemas ---
class CourseBase(BaseModel):
    title: str = Field(..., max_length=200)
    description: str
    price: Decimal = Field(default=0.00, decimal_places=2, max_digits=8)
    is_published: bool = False
    category_id: Optional[int] = None

class CourseCreate(CourseBase):
    pass # Files like thumbnail handled via Form data in routes

class CourseListResponse(BaseModel):
    id: int
    title: str
    slug: str
    price: Decimal
    thumbnail: Optional[str]
    is_published: bool
    instructor_name: str
    category_name: Optional[str]
    average_rating: float

    class Config:
        from_attributes = True

class CourseDetailResponse(CourseBase):
    id: int
    slug: str
    thumbnail: Optional[str]
    instructor_name: str
    category: Optional[CategoryResponse]
    modules: List[ModuleResponse] = []
    average_rating: float
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True