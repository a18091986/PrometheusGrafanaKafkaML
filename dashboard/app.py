import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objs as go
from sqlalchemy import create_engine

# Параметры подключения к базе данных
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"
POSTGRES_DB = "stocks"
POSTGRES_HOST = "postgres"
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"

# Подключение к базе данных
engine = create_engine(DATABASE_URL)


# Загрузка данных из базы
def load_data():
    query = "SELECT date, close FROM stock_data ORDER BY date ASC"
    historical_data = pd.read_sql(query, engine)

    query = "SELECT date, predicted_price FROM predicted_prices ORDER BY date ASC"
    predicted_data = pd.read_sql(query, engine)

    return historical_data, predicted_data


# Инициализация Dash приложения
app = dash.Dash(__name__)
app.title = "Stock Price Dashboard"

# Макет дашборда
app.layout = html.Div([
    html.H1("Stock Price Dashboard", style={'textAlign': 'center'}),
    dcc.Graph(id='price-graph'),
    dcc.Interval(
        id='interval-component',
        interval=3 * 60 * 1000,  # Обновление каждые 3 минуты
        n_intervals=0
    )
])


# Callback для обновления графика
@app.callback(
    dash.dependencies.Output('price-graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_graph(n_intervals):
    historical_data, predicted_data = load_data()

    # Построение исторических данных
    trace_historical = go.Scatter(
        x=historical_data['date'],
        y=historical_data['close'],
        mode='lines',
        name='Historical Prices'
    )

    # Построение предсказанных значений
    trace_predicted = go.Scatter(
        x=predicted_data['date'],
        y=predicted_data['predicted_price'],
        mode='markers',
        name='Predicted Prices',
        marker=dict(size=10, color='red')
    )

    # Создание фигуры
    figure = {
        'data': [trace_historical, trace_predicted],
        'layout': {
            'title': 'Stock Prices and Predictions',
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Price'}
        }
    }

    return figure


# Запуск приложения
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050)
