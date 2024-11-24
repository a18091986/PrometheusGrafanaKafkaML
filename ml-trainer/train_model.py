import time
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import psycopg2
from sqlalchemy import create_engine
import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature
from datetime import datetime, timedelta
from sqlalchemy.sql import text
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("/var/log/stock_prediction.log"),  # Путь к файлу логов
        logging.StreamHandler()
    ]
)

# Параметры PostgreSQL
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"
POSTGRES_DB = "stocks"
POSTGRES_HOST = "postgres"
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"

# Подключение к базе данных
engine = create_engine(DATABASE_URL)


# Функция для обучения и предсказания
def train_and_predict():
    logging.info("Loading data from PostgreSQL...")
    query = "SELECT date, close FROM stock_data ORDER BY date ASC"
    data = pd.read_sql(query, engine)

    # Преобразуем дату в индексы и создаём лаги
    data['date'] = pd.to_datetime(data['date'])
    data['close_lag1'] = data['close'].shift(1)
    data.dropna(inplace=True)

    # Разделяем на обучающую и тестовую выборки
    X = data[['close_lag1']]
    y = data['close']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Настройка модели с использованием Pipeline и GridSearchCV
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('regressor', LinearRegression())
    ])

    param_grid = {
        'regressor__fit_intercept': [True, False],
    }

    grid_search = GridSearchCV(pipeline, param_grid, cv=3, scoring='r2')

    # Логируем модель в MLflow
    mlflow.set_tracking_uri("file:///app/mlruns")
    mlflow.set_experiment("stock_prediction")
    with mlflow.start_run():
        logging.info("Training the model...")
        grid_search.fit(X_train, y_train)
        best_model = grid_search.best_estimator_

        # Пример входных данных и подпись модели
        input_example = pd.DataFrame({'close_lag1': [100.0]})
        signature = infer_signature(X_train, y_train)

        # Логирование модели с подписью
        mlflow.log_params(grid_search.best_params_)
        mlflow.log_metric("train_r2", grid_search.best_score_)
        mlflow.sklearn.log_model(
            sk_model=best_model,
            artifact_path="model",
            signature=signature,
            input_example=input_example
        )

        print("Model training complete.")

    # Предсказание цены на следующий день
    latest_close = data['close'].iloc[-1]
    predicted_price = best_model.predict(pd.DataFrame({'close_lag1': [latest_close]}))[0]
    next_day = data['date'].iloc[-1] + timedelta(days=1)

    print(f"Predicted price for {next_day.date()}: {predicted_price}")

    # Сохраняем результат в новую таблицу
    print("Saving prediction to PostgreSQL...")
    prediction_table_query = text("""
    CREATE TABLE IF NOT EXISTS predicted_prices (
        id SERIAL PRIMARY KEY,
        date DATE NOT NULL,
        predicted_price FLOAT NOT NULL
    )
    """)
    insert_prediction_query = text("""
    INSERT INTO predicted_prices (date, predicted_price) VALUES (:date, :predicted_price)
    """)
    with engine.begin() as conn:
        # Выполняем создание таблицы
        conn.execute(prediction_table_query)
        # Вставляем предсказание
        conn.execute(insert_prediction_query, {"date": next_day.date(), "predicted_price": float(predicted_price)})

    print("Prediction saved.")


if __name__ == "__main__":
    while True:
        try:
            print(f"Starting training and prediction at {datetime.now()}...")
            try:
                train_and_predict()
            except:
                pass
            time.sleep(30)
        except Exception as e:
            logging.error("An error occurred", exc_info=True)
