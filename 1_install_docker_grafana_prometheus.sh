#!/bin/bash

# Установить Docker
install_docker() {
    echo "Устанавливаем Docker..."
    sudo apt-get update -y
    sudo apt-get install -y \
        ca-certificates \
        curl \
        gnupg \
        lsb-release

    # Добавляем официальный репозиторий Docker
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt-get update -y
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

    # Убедиться, что Docker работает
    sudo systemctl enable docker
    sudo systemctl start docker

    echo "Docker установлен."
}

# Установить Docker Compose
install_docker_compose() {
    echo "Устанавливаем Docker Compose..."
    sudo apt-get update -y
    sudo apt-get install -y docker-compose
    echo "Docker Compose установлен."
}

# Установить Prometheus
install_prometheus() {
    echo "Устанавливаем Prometheus..."
    sudo mkdir -p /opt/prometheus
    cd /opt/prometheus

    # Скачиваем последнюю версию Prometheus
    curl -LO https://github.com/prometheus/prometheus/releases/latest/download/prometheus-*-linux-amd64.tar.gz
    tar -xvf prometheus-*-linux-amd64.tar.gz --strip-components=1

    # Создаём Prometheus сервис
    sudo tee /etc/systemd/system/prometheus.service << EOF
[Unit]
Description=Prometheus
After=network.target

[Service]
User=root
ExecStart=/opt/prometheus/prometheus \
  --config.file=/opt/prometheus/prometheus.yml \
  --storage.tsdb.path=/opt/prometheus/data
Restart=always

[Install]
WantedBy=multi-user.target
EOF

    # Запускаем Prometheus
    sudo systemctl daemon-reload
    sudo systemctl enable prometheus
    sudo systemctl start prometheus

    echo "Prometheus установлен."
}

# Установить Grafana
install_grafana() {
    echo "Устанавливаем Grafana..."
    sudo apt-get install -y adduser libfontconfig1 musl
    wget https://dl.grafana.com/oss/release/grafana_11.3.1_amd64.deb
    sudo dpkg -i grafana_11.3.1_amd64.deb
    sudo systemctl start grafana-server
    sudo systemctl enable grafana-server
    echo "Grafana установлена."
}

# Основной процесс установки
main() {
    echo "Начало установки компонентов..."
    install_docker
    install_docker_compose
    install_prometheus
    install_grafana
    echo "Установка завершена!"
}

main
