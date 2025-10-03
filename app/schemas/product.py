from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.base import TimestampMixin
from app.schemas.user import UserResponse


class ProductBase(BaseModel):
    """Base product schema with common fields."""
    title: str = Field(..., min_length=1, max_length=255, description="Product title")
    price: Decimal = Field(..., gt=0, decimal_places=2, description="Product price must be positive")
    description: Optional[str] = Field(None, max_length=2000, description="Product description")
    
    # Dimensions (optional)
    height: Optional[Decimal] = Field(None, ge=0, decimal_places=2, description="Product height in cm")
    length: Optional[Decimal] = Field(None, ge=0, decimal_places=2, description="Product length in cm") 
    depth: Optional[Decimal] = Field(None, ge=0, decimal_places=2, description="Product depth in cm")


class ProductCreate(ProductBase):
    """Schema for product creation."""
    pass


class ProductUpdate(BaseModel):
    """Schema for product updates (all fields optional)."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    description: Optional[str] = Field(None, max_length=2000)
    height: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    length: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    depth: Optional[Decimal] = Field(None, ge=0, decimal_places=2)


class ProductResponse(ProductBase, TimestampMixin):
    """Schema for product responses."""
    id: int
    external_id: Optional[int] = Field(None, description="ID from external API")
    owner_id: int
    
    model_config = ConfigDict(from_attributes=True)


class ProductWithOwner(ProductResponse):
    """Schema for product responses that include owner information."""
    owner: UserResponse


class ProductFilters(BaseModel):
    """Schema for product filtering parameters."""
    search: Optional[str] = Field(None, max_length=100, description="Search in title and description")
    min_price: Optional[Decimal] = Field(None, ge=0, description="Minimum price filter")
    max_price: Optional[Decimal] = Field(None, ge=0, description="Maximum price filter")


class PaginationParams(BaseModel):
    """Schema for pagination parameters."""
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")
    
    @property
    def skip(self) -> int:
        """Calculate offset for database query."""
        return (self.page - 1) * self.page_size
    
    @property
    def limit(self) -> int:
        """Get limit for database query."""
        return self.page_size
    
    @property
    def per_page(self) -> int:
        """Alias for page_size."""
        return self.page_size


class ProductListResponse(BaseModel):
    """Schema for paginated product list responses."""
    products: List[ProductResponse]
    total: int = Field(..., ge=0, description="Total number of products")
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, description="Items per page")
    total_pages: int = Field(..., ge=0, description="Total number of pages")