"Starting elastic search..."
echo $JAVA_HOME
echo "Setting JAVA_HOME"
export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64
echo $ADWISE_HOME
echo "Setting ADWISE_HOME"
export ADWISE_HOME=/home/ubuntu/expooh/repo/adwise-userprofile-mgr
echo $TOOLS_HOME
echo "Setting TOOLS_HOME"
export TOOLS_HOME=/home/ubuntu/tools
echo "Setting VENV_HOME"
export VENV_HOME=/home/ubuntu/expooh/venv
screen -d -m $TOOLS_HOME/elasticsearch-2.3.1/bin/elasticsearch
echo "Starting celery workers..."
echo 'Setting up PYTHONPATH for the worker....'
export PYTHONPATH=$ADWISE_HOME
source $VENV_HOME/bin/activate
screen -d -m celery --app=atlas_ws.celery_config:app worker --loglevel=INFO --concurrency=20 -n worker1.%h
echo "Starting app server..."
screen -d -m python $ADWISE_HOME/manage.py runserver 172.31.41.248:8000 
echo "Starting classifier..." 
$VENV_HOME/bin/python $ADWISE_HOME/tools/classify/classify.py start
echo `$VENV_HOME/bin/python $ADWISE_HOME/tools/classify/classify.py status`
