import logging
import time
import sys
import csv

from btfxwss import BtfxWss
from database import DataBase

log = logging.getLogger(__name__)

fh = logging.FileHandler('test.log')
fh.setLevel(logging.DEBUG)
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)

log.addHandler(sh)
log.addHandler(fh)
logging.basicConfig(level=logging.DEBUG, handlers=[fh, sh])


class Market(object):
    """
    This is the market of the cryptocurrency given symbol.
    Data source is Bitfinex Websocket API.
    """
    def __init__(self, symbol='BTCUSD'):
        self.symbol = symbol
        self.wss = BtfxWss()

    def initialize(self):
        """
        Initialize the market of the crypto and subscribe to trades and order
        books. Data is stored as Queues.
        """
        self.wss.start()

        while not self.wss.conn.connected.is_set():
            time.sleep(1)

        # Subscribe to some channels
        self.wss.subscribe_to_trades(self.symbol)
        self.wss.subscribe_to_order_book(pair=self.symbol, len=100)

        # Create a database
        self.db = DataBase(symbol=self.symbol)

    def create_database(self):
        """
        This function will stream real-time trade and order book data from
        Bitfinex using the websocket API and save the result into a two
        separate csv files.
        It will also create two separate tables with names bitfinex_quotes,
        bitfinex_trades in the AWS MySQL database and save the same
        results into database.
        """
        # Prepare csv databases for trades and quotes
        self.db.initialize_trade_csv()
        self.db.initialize_quote_csv()

        # Access data from BtfxWss:
        self.trade_q = self.wss.trades(self.symbol)  # returns a Queue object for the pair.
        self.quote_q = self.wss.books(self.symbol)

        # Take a snapshot of the orderbook
        self.quote_snapshot = self.quote_q.get()

        # Input the snapshot to database
        db.create_order_book_csv(self.quote_snapshot)

    def stream_data():
        # Continue streaming data
        while True:
            new_trade = self.trade_q.get()
            if new_trade[0][0] == 'te':
                with open('bitfinex_trades_'+self.symbol+'.csv', 'a') as file:
                    writer = csv.writer(file, delimiter = ',')
                    writer.writerow(new_trade[0][1])

            new_order = self.quote_q.get()
            with open('bitfinex_quotes_'+self.symbol+'.csv', 'a') as file:
                writer = csv.writer(file, delimiter = ',')
                writer.writerow(new_order[0][0])
