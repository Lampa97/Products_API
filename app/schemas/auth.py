"""
Authentication-related Pydantic schemas.

This module contains all schemas related to authentication:
- JWT tokens
- Token validation
- Authentication responses
"""

from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for JWT token payload data."""
    email: Optional[str] = None