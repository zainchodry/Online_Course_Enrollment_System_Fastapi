from pydantic import BaseModel, EmailStr, Field, HttpUrl
from typing import Optional
from datetime import datetime
from models.base import RoleEnum

# --- User Profile Schemas ---
class UserProfileBase(BaseModel):
    headline: Optional[str] = Field(None, max_length=150, description="e.g. Full Stack Developer / Student")
    bio: Optional[str] = None
    phone_number: Optional[str] = Field(None, max_length=20)
    avatar_url: Optional[str] = None
    website_link: Optional[str] = None
    qualification: Optional[str] = Field(None, max_length=100)

class UserProfileUpdate(UserProfileBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserProfileResponse(UserProfileBase):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    role: RoleEnum
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

# --- User Auth Schemas ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    first_name: str
    last_name: str
    role: RoleEnum = RoleEnum.STUDENT

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    role: RoleEnum

    class Config:
        from_attributes = True

# --- Password & Token Schemas ---
class ChangePassword(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8, max_length=100)
    confirm_new_password: str = Field(..., min_length=8, max_length=100)

class ResetPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordConfirm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8, max_length=100)
    confirm_new_password: str = Field(..., min_length=8, max_length=100)

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

