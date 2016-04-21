echo 'Setting up PYTHONPATH for the worker....'
export PYTHONPATH=/home/sonu/thomas/atlas/venv/atlas/atlas_ws
echo 'Starting worker...'
celery --app=atlas_ws.celery_config:app worker --loglevel=INFO --concurrency=2 -n worker1.%h
