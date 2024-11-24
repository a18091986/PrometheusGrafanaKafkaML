FROM python:3.10-slim

WORKDIR /app

# Установим зависимости
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копируем скрипт
COPY train_model.py .

CMD ["python", "train_model.py"]