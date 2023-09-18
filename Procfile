# web: uvicorn API.api-app:app --host=0.0.0.0 --port=${PORT:-5000}
web: gunicorn api-app:app --bind 0.0.0.0:$PORT --worker-class uvicorn.workers.UvicornWorker
