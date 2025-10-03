#!/usr/bin/env python3
"""
Celery Beat startup script.

This script starts Celery Beat for scheduling periodic tasks.
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.celery_app import celery_app
# Import tasks to register them with Celery
import app.tasks


def main():
    """Start Celery Beat scheduler."""
    # Set default log level
    log_level = os.getenv("CELERY_LOG_LEVEL", "info")
    
    # Start beat scheduler
    celery_app.start([
        "beat",
        "--loglevel=" + log_level,
        "--schedule=/tmp/celerybeat-schedule",
        "--pidfile=/tmp/celerybeat.pid",
    ])


if __name__ == "__main__":
    main()