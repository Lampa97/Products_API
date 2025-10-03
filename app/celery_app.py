from celery import Celery
from celery.schedules import crontab

from app.core.config import settings

# Create Celery app
celery_app = Celery("products_api", broker=settings.redis_url, backend=settings.redis_url, include=["app.tasks"])

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    result_expires=3600,  # 1 hour
)

# Periodic tasks configuration
# Sync products every 30 minutes
celery_app.conf.beat_schedule = {
    "sync-products-every-30-minutes": {
        "task": "app.tasks.sync_products",
        "schedule": crontab(minute="*/30"),  # Every 30 minutes
    },
}

celery_app.conf.timezone = "UTC"
