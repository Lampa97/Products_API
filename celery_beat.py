import os
import sys
from pathlib import Path

import app.tasks
from app.celery_app import celery_app

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def main() -> None:
    """Start Celery Beat scheduler."""
    # Set default log level
    log_level = os.getenv("CELERY_LOG_LEVEL", "info")

    # Start beat scheduler
    celery_app.start(
        [
            "beat",
            "--loglevel=" + log_level,
            "--schedule=/tmp/celerybeat-schedule",
            "--pidfile=/tmp/celerybeat.pid",
        ]
    )


if __name__ == "__main__":
    main()
