import requests

trade_url = "https://api.bitfinex.com/v1/trades/btcusd"
trade_response = requests.request("GET", trade_url)
#print(trade_response.json())

#book_url = "https://api.bitfinex.com/v1/book/btcusd"
book_url = 'https://api.bitfinex.com/v2/book/tBTCUSD/P0'
params = {'len': 100}
book_response = requests.request("GET", book_url, params=params)
print(book_response.json())
