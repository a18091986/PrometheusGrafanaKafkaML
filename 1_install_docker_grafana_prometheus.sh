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
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o -y /etc/apt/keyrings/docker.gpg
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
    sudo apt install -y prometheus
    sudo cp PrometheusGrafanaKafkaML/prometheus.yml /etc/prometheus/prometheus.yml
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
    sudo wget https://dl.grafana.com/oss/release/grafana_11.3.1_amd64.deb
    sudo dpkg -i grafana_11.3.1_amd64.deb
    sudo systemctl start grafana-server
    sudo systemctl enable grafana-server
    echo "Grafana установлена."
}

install_node_exporter() {
    echo "Устанавливаем Node Exporter..."
    # Скачивание и установка Node Exporter
    wget https://github.com/prometheus/node_exporter/releases/latest/download/node_exporter-1.8.2.linux-amd64.tar.gz
    tar -xvzf node_exporter-1.8.2.linux-amd64.tar.gz
    sudo mv node_exporter-1.8.2.linux-amd64/node_exporter /usr/local/bin/
    rm -rf node_exporter-1.8.2.linux-amd64*

    # Создание пользователя для Node Exporter
    sudo useradd -rs /bin/false nodeexporter

    # Создание системной службы для Node Exporter
    sudo bash -c 'cat > /etc/systemd/system/node_exporter.service <<EOF
[Unit]
Description=Node Exporter
After=network.target

[Service]
User=nodeexporter
Group=nodeexporter
Type=simple
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
EOF'

    # Настройка прав
    sudo chown nodeexporter:nodeexporter /usr/local/bin/node_exporter

    # Запуск и включение Node Exporter
    sudo systemctl daemon-reload
    sudo systemctl enable node_exporter
    sudo systemctl start node_exporter

    echo "Node Exporter установлен."
}

# Основной процесс установки
main() {
    echo "Начало установки компонентов..."
    install_docker
    install_docker_compose
    install_prometheus
    install_grafana
    install_node_exporter
    echo "Установка завершена!"
}

main
