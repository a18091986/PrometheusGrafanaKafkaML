FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY producer.py .
COPY stock.csv .
CMD ["python", "producer.py"]
