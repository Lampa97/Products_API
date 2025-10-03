from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.models import UserRole
from app.schemas.base import TimestampMixin


class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters")
    role: UserRole = UserRole.USER


class UserUpdate(BaseModel):
    """Schema for user updates."""
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None


class UserResponse(UserBase, TimestampMixin):
    """Schema for user responses (excludes password)."""
    id: int
    role: UserRole
    
    model_config = ConfigDict(from_attributes=True)


class UserInDB(UserResponse):
    """Schema for user data as stored in database (includes password hash)."""
    password: str


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str