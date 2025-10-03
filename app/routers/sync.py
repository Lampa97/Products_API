from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel

from app.models.models import User
from app.services.auth import require_admin
from app.services.product_sync import ProductSyncService

router = APIRouter(prefix="/sync", tags=["Product Synchronization"])


class SyncTriggerRequest(BaseModel):
    """Schema for manual sync trigger request."""

    provider_type: Optional[str] = None  # If None, uses settings.external_api_provider


class SyncScheduleRequest(BaseModel):
    """Schema for sync scheduling request."""

    cron_expression: Optional[str] = None
    interval_seconds: Optional[int] = None


@router.post("/trigger", status_code=status.HTTP_202_ACCEPTED)
async def trigger_product_sync(
    request: SyncTriggerRequest = SyncTriggerRequest(), current_user: User = Depends(require_admin)
) -> Any:
    """
    Trigger manual product synchronization (admin only).

    Args:
        request: Sync trigger request
        current_user: Current authenticated admin user

    Returns:
        Sync trigger result
    """
    result = ProductSyncService.start_full_sync(request.provider_type)

    if result["status"] == "error":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])

    return result


@router.get("/status/{task_id}")
async def get_sync_status(task_id: str, current_user: User = Depends(require_admin)) -> Any:
    """
    Get synchronization task status (admin only).

    Args:
        task_id: Celery task ID
        current_user: Current authenticated admin user

    Returns:
        Task status information
    """
    result = ProductSyncService.get_sync_status(task_id)

    if result["status"] == "error":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result["error"])

    return result


@router.delete("/cancel/{task_id}")
async def cancel_sync(task_id: str, current_user: User = Depends(require_admin)) -> Any:
    """
    Cancel synchronization task (admin only).

    Args:
        task_id: Celery task ID
        current_user: Current authenticated admin user

    Returns:
        Cancellation result
    """
    result = ProductSyncService.cancel_sync(task_id)

    if result["status"] == "error":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])

    return result


@router.get("/history")
async def get_sync_history(
    limit: int = Query(10, ge=1, le=100, description="Maximum number of tasks to return"),
    current_user: User = Depends(require_admin),
) -> Any:
    """
    Get synchronization task history (admin only).

    Args:
        limit: Maximum number of tasks to return
        current_user: Current authenticated admin user

    Returns:
        Task history
    """
    result = ProductSyncService.get_sync_history(limit)

    if result["status"] == "error":
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result["error"])

    return result


@router.post("/schedule")
async def schedule_sync(request: SyncScheduleRequest, current_user: User = Depends(require_admin)) -> Any:
    """
    Schedule periodic product synchronization (admin only).

    Args:
        request: Sync scheduling request
        current_user: Current authenticated admin user

    Returns:
        Scheduling result
    """
    result = ProductSyncService.schedule_sync(
        cron_expression=request.cron_expression, interval_seconds=request.interval_seconds
    )

    if result["status"] == "error":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])

    return result


@router.get("/providers")
async def get_available_providers(current_user: User = Depends(require_admin)) -> Any:
    """
    Get list of available external API providers (admin only).

    Args:
        current_user: Current authenticated admin user

    Returns:
        List of available providers
    """
    from app.core.config import settings

    return {
        "status": "success",
        "current_provider": settings.external_api_provider,
        "current_api_url": settings.external_api_url,
        "providers": [
            {"name": "dummyjson", "description": "DummyJSON API for testing", "url": "https://dummyjson.com/products"}
            # Additional providers can be added here
        ],
    }
