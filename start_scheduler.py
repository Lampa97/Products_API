#!/usr/bin/env python3
"""
Start Celery beat scheduler for periodic tasks.

Usage:
    python start_scheduler.py
"""
import subprocess
import sys

if __name__ == "__main__":
    cmd = [sys.executable, "-m", "celery", "-A", "app.celery_app", "beat", "--loglevel=info"]

    print("Starting Celery beat scheduler...")
    print(f"Command: {' '.join(cmd)}")

    subprocess.run(cmd)
