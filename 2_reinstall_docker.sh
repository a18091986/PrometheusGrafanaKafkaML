#!/bin/bash

set -e

echo "=== УДАЛЕНИЕ DOCKER И ДОПОЛНИТЕЛЬНЫХ КОМПОНЕНТОВ ==="

# Остановка всех контейнеров
echo "Остановка всех контейнеров..."
sudo docker stop $(docker ps -aq) || true
sudo docker rm $(docker ps -aq) || true

# Удаление Docker и связанных данных
echo "Удаление Docker и связанных данных..."
sudo apt-get remove --purge -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin || true
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd
sudo rm -rf /etc/docker

# Удаление Docker Compose (если установлен отдельно)
echo "Удаление Docker Compose..."
sudo rm /usr/local/bin/docker-compose || true

# Удаление ненужных пакетов и групп
echo "Удаление дополнительных пакетов и групп..."
sudo apt-get autoremove -y
sudo apt-get autoclean
sudo groupdel docker || true

echo "=== УДАЛЕНИЕ ЗАВЕРШЕНО ==="

echo "=== УСТАНОВКА DOCKER И ДОПОЛНИТЕЛЬНЫХ КОМПОНЕНТОВ ==="

# Установка зависимостей
echo "Установка зависимостей..."
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg

# Добавление ключа и репозитория Docker
echo "Добавление ключа и репозитория Docker..."
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor --yes -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo "Добавление Docker репозитория..."
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
$(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Установка Docker
echo "Установка Docker..."
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Проверка установки Docker
echo "Проверка установки Docker..."
docker --version
sudo systemctl start docker
sudo systemctl enable docker

sudo docker network create kafka_network
sudo mkdir -p /tmp/loki/wal /tmp/loki/chunks /tmp/loki/index /tmp/loki/compactor
sudo chown -R 10001:10001 /tmp/loki


echo "Переход в папку /PrometheusGrafanaKafkaML..."
if [ -d "./PrometheusGrafanaKafkaML" ]; then
  cd PrometheusGrafanaKafkaML
  echo "Запуск docker-compose up --build..."
  sudo docker-compose up --build
else
  echo "Папка /PrometheusGrafanaKafkaML не найдена. Проверьте наличие директории."
fi


# sudo systemctl status docker

# Установка Docker Compose (опционально)
# echo "Установка Docker Compose..."
# sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
# sudo chmod +x /usr/local/bin/docker-compose
# docker-compose --version

echo "=== УСТАНОВКА ЗАВЕРШЕНА ==="
