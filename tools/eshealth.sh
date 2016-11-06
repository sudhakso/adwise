echo "Step1: Listing nodes..."
curl http://127.0.0.1:9200/_cat/nodes?v
echo '###'
echo "Step2: Checking health of the overall cluster..."
curl http://127.0.0.1:9200/_cat/health?v
echo '###'
echo "Step3: Checling indices..."
curl http://127.0.0.1:9200/_cat/indices?v
echo '###'
