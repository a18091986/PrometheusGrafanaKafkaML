import random
from confluent_kafka import Producer
import pandas as pd
import time
from sqlalchemy import create_engine, text


POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"
POSTGRES_DB = "stocks"
POSTGRES_HOST = "postgres"
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"


producer_config = {'bootstrap.servers': 'kafka:9092'}
producer = Producer(producer_config)

topic = 'stock_prices'


engine = create_engine(DATABASE_URL)


data = pd.read_csv('stock.csv')
# data['date'] = pd.to_datetime(data['date'])  # Убедимся, что даты имеют правильный формат


with engine.connect() as conn:
    last_date_query = text("SELECT MAX(date) FROM stock_data")
    result = conn.execute(last_date_query).fetchone()
    last_date_in_db = result[0]  # Получаем максимальную дату

if last_date_in_db:
    print(f"Last date in database: {last_date_in_db}")
else:
    print("No data found in the database. Starting from the beginning.")


if last_date_in_db:
    data_to_send = data[data['date'] > last_date_in_db]
else:
    data_to_send = data


for _, row in data_to_send.iterrows():
    message = row.to_json()
    producer.produce(topic, message)
    producer.flush()
    print(f"Sent: {message}")
    time.sleep(random.randint(1, 10))  # Пауза между сообщениями
