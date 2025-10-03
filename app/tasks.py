import logging
from typing import Any, Dict

from app.celery_app import celery_app
from app.services.sync import sync_products_from_external_sync

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.sync_products")
def sync_products() -> Dict[str, Any]:
    """
    Celery task for periodic product synchronization.

    This task is scheduled to run every 30 minutes and
    synchronizes products from external API.
    """
    logger.info("Starting product synchronization task")
    result = sync_products_from_external_sync()
    logger.info(f"Product synchronization completed: {result}")
    return result
