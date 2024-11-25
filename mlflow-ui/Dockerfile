FROM python:3.9-slim
RUN pip install mlflow
WORKDIR /app
EXPOSE 8080
CMD ["mlflow", "ui", "--host", "0.0.0.0", "--port", "8080", "--backend-store-uri", "file:///mlruns"]
