from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.models import Product, User
from app.schemas.product import PaginationParams, ProductCreate, ProductListResponse, ProductResponse, ProductUpdate
from app.services.auth import get_current_active_user, require_admin

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)
) -> Any:
    """
    Create a new product (admin only).

    Args:
        product_data: Product creation data
        db: Database session
        current_user: Current authenticated admin user

    Returns:
        Created product data
    """
    # Create product with owner_id from current user
    product_dict = product_data.model_dump()
    product_dict["owner_id"] = current_user.id
    db_product = Product(**product_dict)

    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)

    return db_product


@router.get("/", response_model=ProductListResponse)
async def get_products(
    pagination: PaginationParams = Depends(),
    search: str = Query(None, description="Search in title and description"),
    category: str = Query(None, description="Filter by category"),
    min_price: float = Query(None, ge=0, description="Minimum price filter"),
    max_price: float = Query(None, ge=0, description="Maximum price filter"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get products list with pagination and filters.

    Args:
        pagination: Pagination parameters
        search: Search query for title and description
        category: Category filter
        min_price: Minimum price filter
        max_price: Maximum price filter
        db: Database session
        current_user: Current authenticated user

    Returns:
        Paginated list of products
    """
    # Build query
    query = select(Product)

    # Apply search filter
    if search:
        search_filter = Product.title.ilike(f"%{search}%") | Product.description.ilike(f"%{search}%")
        query = query.where(search_filter)

    # Apply category filter
    if category:
        query = query.where(Product.category.ilike(f"%{category}%"))

    # Apply price filters
    if min_price is not None:
        query = query.where(Product.price >= min_price)
    if max_price is not None:
        query = query.where(Product.price <= max_price)

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Apply pagination and execute
    query = query.offset(pagination.skip).limit(pagination.limit)
    result = await db.execute(query)
    products = result.scalars().all()

    # Convert products to response format
    product_responses = [ProductResponse.model_validate(product) for product in products]

    # Ensure total is not None
    total_count = total or 0

    return ProductListResponse(
        products=product_responses,
        total=total_count,
        page=pagination.page,
        page_size=pagination.page_size,
        total_pages=((total_count - 1) // pagination.page_size) + 1 if total_count > 0 else 0,
    )


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get product by ID.

    Args:
        product_id: Product ID
        db: Database session
        current_user: Current authenticated user

    Returns:
        Product data

    Raises:
        HTTPException: If product not found
    """
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    return product


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> Any:
    """
    Update product (admin only).

    Args:
        product_id: Product ID
        product_data: Product update data
        db: Database session
        current_user: Current authenticated admin user

    Returns:
        Updated product data

    Raises:
        HTTPException: If product not found
    """
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    # Update product fields
    update_data = product_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)

    await db.commit()
    await db.refresh(product)

    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)
) -> None:
    """
    Delete product (admin only).

    Args:
        product_id: Product ID
        db: Database session
        current_user: Current authenticated admin user

    Raises:
        HTTPException: If product not found
    """
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    await db.delete(product)
    await db.commit()
