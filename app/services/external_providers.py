from abc import ABC, abstractmethod
from typing import Any, Dict, List

import httpx

from app.core.config import settings
from app.schemas.external import DummyJSONProduct, DummyJSONResponse, NormalizedProduct


class ExternalAPIProvider(ABC):
    """Abstract base class for external API providers."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name for identification."""
        pass
    
    @abstractmethod
    async def fetch_products(self) -> List[Dict[str, Any]]:
        """Fetch raw products from external API."""
        pass
    
    @abstractmethod
    def normalize_product(self, raw_product: Dict[str, Any]) -> NormalizedProduct:
        """Normalize raw product data to our internal format."""
        pass
    
    async def fetch_and_normalize_products(self) -> List[NormalizedProduct]:
        """Fetch products and normalize them."""
        raw_products = await self.fetch_products()
        return [self.normalize_product(product) for product in raw_products]


class DummyJSONProvider(ExternalAPIProvider):
    """Provider for DummyJSON API."""
    
    def __init__(self, api_url: str = None):
        self.api_url = api_url or "https://dummyjson.com/products"
    
    @property
    def name(self) -> str:
        return "dummyjson"
    
    async def fetch_products(self) -> List[Dict[str, Any]]:
        """Fetch products from DummyJSON API."""
        async with httpx.AsyncClient() as client:
            response = await client.get(self.api_url)
            response.raise_for_status()
            
            dummy_response = DummyJSONResponse(**response.json())
            
            return [product.model_dump() for product in dummy_response.products]
    
    def normalize_product(self, raw_product: Dict[str, Any]) -> NormalizedProduct:
        """Normalize DummyJSON product to our internal format."""
        product = DummyJSONProduct(**raw_product)
        
        dimensions = product.dimensions or {}
        
        return NormalizedProduct(
            external_id=product.id,
            title=product.title,
            price=float(product.price),
            description=product.description,
            height=dimensions.height,
            length=dimensions.width,
            depth=dimensions.depth,
            source_api=self.name
        )


def get_external_provider(provider_type: str = None, **kwargs) -> ExternalAPIProvider:
    """
    Factory function to get external product provider.
    
    Args:
        provider_type: Type of provider (if None, uses settings.external_api_provider)
        **kwargs: Additional arguments for provider initialization
    
    Returns:
        Configured provider instance
    """
    # Use provider from settings if not specified
    if provider_type is None:
        provider_type = settings.external_api_provider
    
    providers = {
        "dummyjson": DummyJSONProvider,
        # Future providers can be added here
    }
    
    if provider_type not in providers:
        raise ValueError(f"Unknown provider type: {provider_type}. Available: {list(providers.keys())}")
    
    # Use configured URL or pass custom one
    if provider_type in providers.keys() and "api_url" not in kwargs:
        kwargs["api_url"] = settings.external_api_url
    
    return providers[provider_type](**kwargs)