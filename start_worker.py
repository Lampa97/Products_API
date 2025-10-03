#!/usr/bin/env python3
"""
Start Celery worker for background tasks.

Usage:
    python start_worker.py
"""
import subprocess
import sys

if __name__ == "__main__":
    cmd = [
        sys.executable, "-m", "celery", 
        "-A", "app.celery_app", 
        "worker", 
        "--loglevel=info"
    ]
    
    print("Starting Celery worker...")
    print(f"Command: {' '.join(cmd)}")
    
    subprocess.run(cmd)