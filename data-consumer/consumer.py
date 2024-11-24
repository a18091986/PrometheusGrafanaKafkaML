from sqlalchemy import create_engine, Column, Integer, Float, String, MetaData, Table
from sqlalchemy.orm import sessionmaker
from confluent_kafka import Consumer
import json

# Настройка SQLAlchemy для PostgreSQL
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"
POSTGRES_DB = "stocks"
POSTGRES_HOST = "postgres"
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Определение таблицы
stocks_table = Table(
    'stock_data', metadata,
    Column('id', Integer, primary_key=True),
    Column('date', String, nullable=False),
    Column('close', Float, nullable=False)
)
metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Настройка Kafka Consumer
consumer_config = {
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'stock_consumer_group',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(consumer_config)

topic = 'stock_prices'
consumer.subscribe([topic])

# Получение данных из Kafka и запись в PostgreSQL
print("Waiting for messages...")
while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print(f"Consumer error: {msg.error()}")
        continue

    data = json.loads(msg.value().decode('utf-8'))
    print(f"Received: {data}")

    # Вставка данных в PostgreSQL
    session.execute(stocks_table.insert().values(date=data['date'], close=data['close']))
    session.commit()

consumer.close()


# import datetime
#
# from confluent_kafka import Consumer
# from sqlalchemy import create_engine, Column, Integer, Float, String, MetaData, Table
# from sqlalchemy.orm import sessionmaker
# import json
#
# # Настройка Kafka Consumer
# consumer_config = {
#     'bootstrap.servers': 'kafka:9092',
#     'group.id': 'stock_consumer_group',
#     'auto.offset.reset': 'earliest'
# }
# consumer = Consumer(consumer_config)
#
# topic = 'stock_prices'
# consumer.subscribe([topic])
#
# # Настройка SQLAlchemy
# DATABASE_URL = "sqlite:////app/data/stocks.db"
# engine = create_engine(DATABASE_URL)
# metadata = MetaData()
#
# # Определение таблицы
# stocks_table = Table(
#     'stock_data', metadata,
#     Column('id', Integer, primary_key=True),
#     Column('date', String, nullable=False),
#     Column('close', Float, nullable=False)
# )
# metadata.create_all(engine)
#
# Session = sessionmaker(bind=engine)
# session = Session()
#
# # Получение данных из Kafka и запись в БД
# print("Waiting for messages...")
# while True:
#     print("--------------------------------------------------------------------------------------------------")
#     msg = consumer.poll(3.0)  # Ожидание сообщения
#     if msg is None:
#         continue
#     if msg.error():
#         print(f"Consumer error: {msg.error()}")
#         continue
#
#     data = json.loads(msg.value().decode('utf-8'))
#     print(f"Received: {data}")
#
#     with open('log.txt', 'a') as f:
#         f.write(f"{datetime.datetime.now()}: {data}\n")
#
#     # Вставка данных в БД
#     session.execute(stocks_table.insert().values(date=data['date'], close=data['close']))
#     session.commit()
#
# consumer.close()
