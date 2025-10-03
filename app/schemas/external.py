from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class BaseExternalProduct(BaseModel):
    """Base schema for external product data."""
    id: Union[int, str]
    title: str
    price: Union[float, int, str]
    description: Optional[str] = None
    
    extra_data: Dict[str, Any] = Field(default_factory=dict)


class BaseExternalProductList(BaseModel):
    """Base schema for external product list responses."""
    products: List[BaseExternalProduct]
    total: Optional[int] = None
    
    pagination_info: Dict[str, Any] = Field(default_factory=dict)


class DummyJSONDimensions(BaseModel):
    """Schema for DummyJSON product dimensions."""
    width: Optional[float] = None
    height: Optional[float] = None  
    depth: Optional[float] = None


class DummyJSONProduct(BaseModel):
    """Schema for DummyJSON API product response."""
    id: int
    title: str
    price: float
    description: str
    category: Optional[str] = None
    brand: Optional[str] = None
    thumbnail: Optional[str] = None
    images: Optional[List[str]] = None
    dimensions: Optional[DummyJSONDimensions] = None
    weight: Optional[float] = None
    rating: Optional[float] = None
    stock: Optional[int] = None
    tags: Optional[List[str]] = None
    
    # Allow any additional fields DummyJSON might add
    model_config = {"extra": "allow"}


class DummyJSONResponse(BaseModel):
    """Schema for DummyJSON products list response."""
    products: List[DummyJSONProduct]
    total: int
    skip: int
    limit: int


class NormalizedProduct(BaseModel):
    """Normalized product schema for internal use."""
    external_id: Union[int, str]
    title: str
    price: float 
    description: Optional[str] = None
    height: Optional[float] = None
    length: Optional[float] = None
    depth: Optional[float] = None
    
    source_api: str = Field(..., description="Source API name")



ExternalProductDimensions = DummyJSONDimensions
ExternalProductResponse = DummyJSONProduct  
ExternalProductsResponse = DummyJSONResponse