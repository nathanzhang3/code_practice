import logging
import time
import sys
import csv

from btfxwss import BtfxWss

log = logging.getLogger(__name__)

fh = logging.FileHandler('test.log')
fh.setLevel(logging.DEBUG)
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)

log.addHandler(sh)
log.addHandler(fh)
logging.basicConfig(level=logging.DEBUG, handlers=[fh, sh])

wss = BtfxWss()
wss.start()

while not wss.conn.connected.is_set():
    time.sleep(1)

symbol = 'BTCUSD'

# Subscribe to some channels
wss.subscribe_to_trades(symbol)
wss.subscribe_to_order_book(symbol)

# Do something else
t = time.time()
while time.time() - t < 10:
    pass

# Accessing data stored in BtfxWss:
trade_q = wss.trades(symbol)  # returns a Queue object for the pair.
book_q = wss.books(symbol)
while True:
    new_trade = trade_q.get()
    if new_trade[0][0] == 'te':
        print(new_trade)
        with open('streaming_trades_'+symbol+'_'+str(t)+'.csv', 'a') as file:
            writer = csv.writer(file, delimiter = ',')
            writer.writerow(new_trade)

    new_order = book_q.get()
    print(new_order)
    with open('streaming_orders_'+symbol+'_'+str(t)+'.csv', 'a') as file:
        writer = csv.writer(file, delimiter = ',')
        writer.writerow(new_order)
