#pip install websocket-client
#pip install finnhub-python

# Stream real-time trades for US stocks, forex and crypto
import websocket

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    #ws.send('{"type":"subscribe","symbol":"AAPL"}')
    #ws.send('{"type":"subscribe","symbol":"AMZN"}')
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')
    #ws.send('{"type":"subscribe","symbol":"IC MARKETS:1"}')

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=cdcf9kaad3i6ap45vle0cdcf9kaad3i6ap45vleg",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever() #run until we stop it
    ws.close() #when we press the stop button


# Search for best-matching symbols based on your query
import finnhub

finnhub_client = finnhub.Client(api_key="cdcf9kaad3i6ap45vle0cdcf9kaad3i6ap45vleg")
print(finnhub_client.symbol_lookup('BTC'))


# Get general information of a company
finnhub_client = finnhub.Client(api_key="cdcf9kaad3i6ap45vle0cdcf9kaad3i6ap45vleg")
print(finnhub_client.company_profile2(symbol='AAPL'))


# Get latest market news
finnhub_client = finnhub.Client(api_key="cdcf9kaad3i6ap45vle0cdcf9kaad3i6ap45vleg")
print(finnhub_client.general_news('general', min_id=0))


# Get company peers. Return a list of peers operating in the same country and sector/industry.
finnhub_client = finnhub.Client(api_key="cdcf9kaad3i6ap45vle0cdcf9kaad3i6ap45vleg")
print(finnhub_client.company_peers('AAPL'))


# Get company basic financials such as margin, P/E ratio, 52-week high/low etc
finnhub_client = finnhub.Client(api_key="cdcf9kaad3i6ap45vle0cdcf9kaad3i6ap45vleg")
print(finnhub_client.company_basic_financials('AAPL', 'all'))


# Get insider sentiment data for US companies, from -100 for the most negative to 100 for the most positive
finnhub_client = finnhub.Client(api_key="cdcf9kaad3i6ap45vle0cdcf9kaad3i6ap45vleg")
print(finnhub_client.stock_insider_sentiment('AAPL', '2021-01-01', '2022-03-01'))


# Get latest analyst recommendation trends for a company.
finnhub_client = finnhub.Client(api_key="cdcf9kaad3i6ap45vle0cdcf9kaad3i6ap45vleg")
print(finnhub_client.recommendation_trends('AAPL'))




