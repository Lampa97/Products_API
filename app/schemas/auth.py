from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.models.models import UserRole


class Token(BaseModel):
    """Schema for JWT token response."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for JWT token payload data."""

    email: Optional[str] = None


class LoginRequest(BaseModel):
    """Schema for user login request."""

    email: EmailStr
    password: str = Field(..., max_length=72, description="Password (max 72 characters for bcrypt)")


class RegisterRequest(BaseModel):
    """Schema for user registration request."""

    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72, description="Password (6-72 characters)")
    role: Optional[UserRole] = UserRole.USER

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password requirements."""
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password too long (max 72 bytes)")
        if len(v) < 6:
            raise ValueError("Password too short (min 6 characters)")
        return v


class UpdateUserRoleRequest(BaseModel):
    """Schema for updating user role (admin only)."""

    user_id: int
    role: UserRole
