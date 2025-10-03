"""
Database models.

This module contains SQLAlchemy models for the application:
- User: User accounts with roles (admin/user)
- Product: Products with dimensions and external API sync support
"""

from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship

from app.db.database import Base


class UserRole(str, Enum):
    """User role enumeration."""
    ADMIN = "admin"
    USER = "user"


class User(Base):
    """
    User model.
    
    Represents user accounts with authentication and role-based access control.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # Hashed password
    role = Column(String, default=UserRole.USER, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship with products (one user can own many products)
    products = relationship("Product", back_populates="owner")


class Product(Base):
    """
    Product model.
    
    Represents products in the store with dimensions and external API sync support.
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    price = Column(Numeric(10, 2), nullable=False)
    description = Column(Text)
    
    # External API synchronization
    external_id = Column(Integer, unique=True, index=True)  # ID from external API like DummyJSON
    
    # Product dimensions (height, length, depth as per requirements)
    height = Column(Numeric(10, 2))
    length = Column(Numeric(10, 2))
    depth = Column(Numeric(10, 2))
    
    # Foreign key to user (owner of the product)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="products")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)