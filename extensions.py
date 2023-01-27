import requests
from datetime import datetime
import json
from config import keys, API_KEY


class ConvertionException(Exception):
    pass


class Converter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        url = f"http://data.fixer.io/api/latest?access_key={API_KEY}&symbols={quote_ticker},{base_ticker}&format=1"
        data = requests.get(url).json()
        if data["success"]:
            # request successful
            rates = data["rates"]
            # since we have the rate for our currency to src and dst, we can get exchange rate between both
            # using below calculation
            exchange_rate = 1 / rates[src] * rates[dst]
            last_updated_datetime = datetime.fromtimestamp(data["timestamp"])
            return last_updated_datetime, exchange_rate * amount
        # r = requests.get(f'https://api.apilayer.com/exchangerates_data/convert?fsym={quote_ticker}&tsyms={base_ticker}')
        # total_base = json.loads(r.content)[keys[base]]
        #
        # return total_base
