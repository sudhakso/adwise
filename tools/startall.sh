"Starting elastic search..."
echo $JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64
screen -d -m /home/ubuntu/tools/elasticsearch-2.3.1/bin/elasticsearch
echo "Starting celery workers..."
echo 'Setting up PYTHONPATH for the worker....'
export PYTHONPATH=/home/ubuntu/expooh/repo/adwise-userprofile-mgr/
source /home/ubuntu/expooh/venv/bin/activate
screen -d -m celery --app=atlas_ws.celery_config:app worker --loglevel=INFO --concurrency=2 -n worker1.%h
echo "Starting app server..."
screen -d -m python /home/ubuntu/expooh/repo/adwise-userprofile-mgr/manage.py runserver 172.31.41.248:8000

