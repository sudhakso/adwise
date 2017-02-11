echo 'Setting up PYTHONPATH for the worker....'
export PYTHONPATH=/home/ubuntu/expooh/repo/adwise-userprofile-mgr/
echo 'Starting worker...'
celery --app=atlas_ws.celery_config:app worker --loglevel=DEBUG --concurrency=15 -n worker1.%h
