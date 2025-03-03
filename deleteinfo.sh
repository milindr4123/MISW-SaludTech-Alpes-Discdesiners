docker-compose --profile pulsar down
docker-compose --profile db down
sudo rm -rf connectors/*
sudo rm -rf data/bookkeeper/*
sudo rm -rf data/zookeeper/*
sudo rm -rf data/mysql/*
sudo rm -rf data/mysql_logs/*