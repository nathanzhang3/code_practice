import logging
import time
import sys

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

# Subscribe to some channels
wss.subscribe_to_trades('BTCUSD')
wss.subscribe_to_order_book('BTCUSD')

# Do something else
t = time.time()
while time.time() - t < 10:
    pass

# Accessing data stored in BtfxWss:
trade_q = wss.trades('BTCUSD')  # returns a Queue object for the pair.
while True:
    print(trade_q.get())
