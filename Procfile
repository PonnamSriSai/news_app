# Flask News Application
web: gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 --max-requests 1000 --max-requests-jitter 100 app:app
worker: celery -A app.celery worker --loglevel=info
beat: celery -A app.celery beat --loglevel=info
