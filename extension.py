import requests
import json
import math
from config import keys, api_key

class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        # if quote == base:
        #     raise APIException(f'Enter different values: {base}.')

        # quote_ticker, base_ticker = keys[quote], keys[base]
        if base not in keys:
            raise APIException(f'Unknown currency: {base}')
        # try:
        #     base_ticker = keys[base]
        # except KeyError:
        #     raise APIException(f'Failed to process the value {base}')
        base_ticker = keys[base]
        if quote not in keys:
            raise APIException(f'Unknown currency: {quote}')
        if quote == base:
            raise APIException(f'Enter different values: {base}.')
        # try:
        #     quote_ticker = keys[quote]
        # except KeyError:
        #     raise APIException(f'Failed to process the value {quote}')
        quote_ticker = keys[quote]
        try:
            amount = float(amount.replace(",", "."))
            if not math.isfinite(amount):
                raise APIException('Amount must be a finite number')


        except ValueError:
            raise APIException(f'Failed to process the amount  {amount}')
        if amount <= 0:
            raise APIException(f'Ensure amount is more then 0')


        url = 'https://min-api.cryptocompare.com/data/price'

        params = {
            'fsym': base_ticker,
            'tsyms': quote_ticker,
            'api_key': api_key
        }

        try:
            r = requests.get(url, params=params)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise APIException('Something went wrong. Please try again later.')
        print(r.status_code)
        print(r.text)
        total_base = round(json.loads(r.content)[keys[quote]] * amount, 3)
        return total_base
