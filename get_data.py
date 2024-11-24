from pathlib import Path
import pandas as pd
from urllib.request import urlopen
import certifi
import json
from urllib.request import urlopen


def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)


url = ("https://financialmodelingprep.com/api/v3/historical-price-full/AAPL?from=1990-10-10&apikey"
       "=b4923a762a0652761e749843270bc8bf")
data = get_jsonparsed_data(url).get('historical')
df = pd.DataFrame(data)
df_reversed = df.iloc[::-1]
df_reversed[['date', 'close']].to_csv(Path('data-producer', 'stock.csv'), index=False)
