#!/bin/bash

# Остановить все контейнеры
echo "Stopping all containers..."
docker stop $(docker ps -aq)

# Удалить все контейнеры
echo "Removing all containers..."
docker rm $(docker ps -aq)

# Удалить все образы
echo "Removing all images..."
docker rmi $(docker images -q)

# Удалить все тома
echo "Removing all volumes..."
docker volume rm $(docker volume ls -q)

# Удалить все неиспользуемые сети
# echo "Removing all unused networks..."
# docker network prune -f

# Полная очистка системы Docker
echo "Pruning Docker system (including unused images and volumes)..."
docker system prune -a --volumes -f

# Завершение
echo "Docker cleanup complete!"
