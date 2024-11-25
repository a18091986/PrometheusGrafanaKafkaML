
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN mkdir -p /app/data
COPY consumer.py .
CMD ["python", "consumer.py"]
