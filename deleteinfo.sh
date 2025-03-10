echo "Stopping and removing Pulsar containers..."
docker-compose --profile pulsar down

echo "Stopping and removing DB containers..."
docker-compose --profile db down

echo "Removing connectors directory..."
sudo rm -rf connectors

echo "Removing data directory..."
sudo rm -rf data

echo "Creating data/bookkeeper directory..."
sudo mkdir -p data/bookkeeper

echo "Creating data/zookeeper directory..."
sudo mkdir -p data/zookeeper

echo "Creating data/mysql directory..."
sudo mkdir -p data/mysql

echo "Creating data/mysql_logs directory..."
sudo mkdir -p data/mysql_logs

echo "Creating connectors directory..."
sudo mkdir -p connectors

echo "Setting permissions for data directory..."
sudo chmod -R 777 data

echo "Setting permissions for connectors directory..."
sudo chmod -R 777 connectors

echo "Start DB container..."
docker-compose --profile db up -d

echo "Script execution completed."
