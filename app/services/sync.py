import asyncio
from typing import Any, Dict

from sqlalchemy import select

from app.db.database import AsyncSessionLocal
from app.models.models import Product
from app.services.external_providers import get_external_provider


async def sync_products_from_external() -> Dict[str, Any]:
    """
    Synchronize products from external API.

    Fetches products from external API and updates local database:
    - New products are added
    - Existing products are updated by external_id

    Returns:
        Dictionary with sync results
    """
    try:
        # Get external provider
        provider = get_external_provider()

        # Fetch and normalize products
        normalized_products = await provider.fetch_and_normalize_products()

        async with AsyncSessionLocal() as db:
            added_count = 0
            updated_count = 0

            for product_data in normalized_products:
                # Check if product exists by external_id
                result = await db.execute(select(Product).where(Product.external_id == product_data.external_id))
                existing_product = result.scalar_one_or_none()

                if existing_product:
                    # Update existing product
                    setattr(existing_product, "title", product_data.title)
                    setattr(existing_product, "price", product_data.price)
                    setattr(existing_product, "description", product_data.description)
                    setattr(existing_product, "height", product_data.height)
                    setattr(existing_product, "length", product_data.length)
                    setattr(existing_product, "depth", product_data.depth)
                    updated_count += 1
                else:
                    # Create new product
                    new_product = Product(
                        external_id=product_data.external_id,
                        title=product_data.title,
                        price=product_data.price,
                        description=product_data.description,
                        height=product_data.height,
                        length=product_data.length,
                        depth=product_data.depth,
                    )
                    db.add(new_product)
                    added_count += 1

            await db.commit()

            return {
                "status": "success",
                "added": added_count,
                "updated": updated_count,
                "total_processed": len(normalized_products),
            }

    except Exception as e:
        return {"status": "error", "error": str(e)}


def sync_products_from_external_sync() -> Dict[str, Any]:
    """
    Synchronous wrapper for the async sync function.
    Required for Celery task execution.
    """
    return asyncio.run(sync_products_from_external())
