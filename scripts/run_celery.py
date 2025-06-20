#!/usr/bin/env python3
"""Celery worker script for TutorCruncher API"""

from app.core.celery_app import celery_app

if __name__ == '__main__':
    celery_app.start()
