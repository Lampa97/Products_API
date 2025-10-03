#!/usr/bin/env python3
"""
Celery worker startup script.

This script starts a Celery worker for processing background tasks.
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
    """Start Celery worker."""
    # Set default log level
    log_level = os.getenv("CELERY_LOG_LEVEL", "info")
    
    # Start worker
    celery_app.worker_main([
        "worker",
        "--loglevel=" + log_level,
        "--concurrency=4",
        "--prefetch-multiplier=1",
        "--without-gossip",
        "--without-mingle",
        "--without-heartbeat",
    ])


if __name__ == "__main__":
    main()