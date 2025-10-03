"""
Base schemas and mixins.

This module contains common base classes and mixins used across other schemas.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TimestampMixin(BaseModel):
    """Mixin for models with timestamps."""
    created_at: datetime
    updated_at: Optional[datetime] = None


class ErrorResponse(BaseModel):
    """Schema for error responses."""
    detail: str
    error_code: Optional[str] = None


class ValidationErrorResponse(BaseModel):
    """Schema for validation error responses."""
    detail: str
    errors: list[dict]