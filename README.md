# PrometheusGrafanaKafkaML

## Stock Price Prediction Simple Example

## Stack: 
- Kafka
- Postgres
- Scikit-Learn (pipeline, grid search)
- MLFlow
- Prometheus
- Grafana
- Loki
- Promtail
- Docker


### web
- :8050 - dash
- :3000 - grafana
- :3100/metrics - Loki
- :9090/graph - prometheus
- :9100/metrics - node exporter
- :9080 - promtail
- :8080 - mlflow


### grafana config

1. connections -> prometheus -> http://localhost:9090 -> save 
2. dashboards -> new -> import -> 1860
3. data sources -> Loki -> http://localhost:3100 -> save -> explore data -> label browser -> select -> show
4. dashboards -> new -> visualisation -> loki -> Logs