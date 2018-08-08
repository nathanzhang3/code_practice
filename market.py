import logging
import time
import sys

from btfxwss import BtfxWss
from database import DataBase
from message import message

logger = logging.getLogger(__name__)


class Market(object):
    """
    This is the market of the cryptocurrency given symbol.
    Data source is Bitfinex Websocket API.
    """
    def __init__(self, symbol='BTCUSD'):
        self.symbol = symbol
        self.wss = BtfxWss()

        self.wss.start()


    def check_connection(self, pat=60):
        """
        Check connection with Bitfinex API. If consecutively failing to connect,
        the program will send an alert message
        :param pat:
            the maximum patience time before sending an alert notification of
            disrupted connection.
        """
        init = time.time()

        # Wait until either connected or exceeding patience
        while not self.wss.conn.connected.is_set() or time.time() > init + pat:
            time.sleep(1)

        # If connection is not set, send a note
        if self.wss.conn.connected.is_set():
            pass
        else:
            message(txt_msg='The connection is disrupted.')
            logger.error('Connection failed.')
            exit()

    def initialize_api(self):
        """
        Initialize the API for the crypto market and subscribe to trades and order
        books. Data is stored as Queues.
        """

        self.check_connection()

        # Subscribe to some channels
        self.wss.subscribe_to_trades(self.symbol)
        self.wss.subscribe_to_order_book(pair=self.symbol, len=100)

        # Initialize a DataBase object
        self.db = DataBase(symbol=self.symbol)

        logger.info('API connection initialized.')

    def create_database(self):
        """
        This function will build connection with Bitfinex Websocket API and AWS
        MySQL DB. Then initialize the csv files and sql databases
        for trades and orderbook.
        """
        # Check connection
        self.check_connection()

        # Prepare csv databases for trades and quotes
        self.db.initialize_trade_csv()
        self.db.initialize_quote_csv()

        # Prepare sql database and tables
        self.db.initialize_sql_db()
        self.db.initialize_trade_sql()
        self.db.initialize_quote_sql()

        # Access data from BtfxWss and return a Queue object for the pair:
        self.trade_q = self.wss.trades(self.symbol)
        self.quote_q = self.wss.books(self.symbol)

        # Take a snapshot of the orderbook
        quote_snapshot = self.quote_q.get()

        # Input the snapshot to database
        self.db.create_order_book(quote_snapshot)
        self.db.create_quote_csv(quote_snapshot)
        self.db.create_quote_sql(quote_snapshot)

        logger.info('Databases created.')

    def stream_data(self):
        """
        This function access the live data with established Bitfinex API, and
        keep streaming new trade and quote data. Then update the csv files and
        sql databases accordingly.
        """
        # Check connection
        self.check_connection()

        # Update trade info
        new_trade = self.trade_q.get()
        self.db.update_trade_csv(new_trade)
        self.db.update_trade_sql(new_trade)

        # Update order book
        quote_change = self.quote_q.get()
        self.db.update_quote_csv(quote_change)
        self.db.update_quote_sql(quote_change)

        logger.info('New trade and quote updated.')
