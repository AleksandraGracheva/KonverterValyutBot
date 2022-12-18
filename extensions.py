import requests
import json
from config import keys

class ConvertionException(Exception):
    pass

class ValueConverter:
    @staticmethod
    def getConvert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Введены одинаковые валюты {base}.')
        if not amount.isdigit():
            raise ConvertionException(f'Количество переводимой валюты должно быть отрицательным числом {amount}.')
        if float(amount) < 0:
            raise ConvertionException(f'Количество переводимой валюты не может быть отрицательным {amount}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось перевести валюту {quote}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось перевести валюту {base}.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base
