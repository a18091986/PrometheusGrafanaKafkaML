# Используем официальный Python-образ
FROM python:3.9-slim

# Устанавливаем MLflow
RUN pip install mlflow

# Указываем рабочую директорию
WORKDIR /app

# Экспортируем порт для MLflow
EXPOSE 8080

# Устанавливаем точку входа
CMD ["mlflow", "ui", "--host", "0.0.0.0", "--port", "8080", "--backend-store-uri", "file:///mlruns"]
