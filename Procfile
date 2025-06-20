web: gunicorn -k uvicorn.workers.UvicornWorker app.main:app
worker: celery -A app.core.celery_app.celery_app worker --loglevel=info 