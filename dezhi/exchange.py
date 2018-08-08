from hitbtc import HitBTC
import time
import requests
import datetime
from database import DataBase
import numpy as np
from settlement import Settlement

class Exchange(object):
    """
    This is the exchange of cryptocurrency.
    Hitbtc exchange was used in this code.
    Hitbtc will provide the trade data.
    """
    def __init__(self, url='https://api.hitbtc.com'):
        self.url = url
        self.session = requests.session()
        self.trader_dict = None
        self.settlement = Settlement()
        self.database = None
        self.from_time = None
        self.till_time = None
        self.settlement_price = {'BTCUSD': 0, 'ETHUSD': 0}

    def assign_traders(self, trader_dict):
        """
        Assign traders to exchange

        :param trader_dict:
            a dict of Trader
        """
        self.trader_dict = trader_dict

    def assign_database(self, user_name='postgres', password='123456',
                 ip='5432', database_name='postgres'):
        """
        Add database to exchange
        WARNING:
            Please customize your own configs
        """
        self.database = DataBase(self.trader_dict, user_name=user_name,
                password=password, ip=ip, database_name=database_name)

    def initialize(self):
        """
        Initialize the starting time. From now on the settlement begins
        """
        self.from_time = datetime.datetime.now()

    def settle_trigger(self, symbols):
        """
        A trigger to run incremental settlements.
        Using RESTful api to query data from exchange.
        The settlement process includes produce a settlement price;
        calculate the settlements obligations; and adjust traders' balance;
        also record the trade data, settlements, and balance to a database

        :param symbol:
            A list of string. (ie. ['BTCUSD', 'ETHUSD'])
        """
        self.till_time = datetime.datetime.now()
        for symbol in symbols:
            query = ('/api/2/public/trades/{}?sort=DESC&by=timestamp&'
                     'from={}&till={}&limit=1000'.format(symbol, self.from_time,
                                                         self.till_time))
            trade_data = self.session.get(self.url + query).json()
            trade_data = self.process_trade_data(trade_data, symbol)
            self.database.write_trade_data(trade_data)
            self.settlement_price[symbol] = self.one_hour_vwap(symbol)
            stl_data = self.database.write_settlement_data(trade_data,
                                                self.settlement_price[symbol])
            self.database.write_balance_data(stl_data)
        self.from_time = self.till_time

    def process_trade_data(self, trade_data, symbol):
        """
        Make up the symbol in the trade_data;
        randomly assign trader id and counter-party id to trade data

        :param trade_data:
            A list of dict
        :param symbol:
            A string
        :return:
            A list of dict
        """
        for data in trade_data:
            trader_id, counterparty_id = np.random.choice(range(10), size=2,
                                                          replace=False)
            data.update({'symbol': symbol, 'trader_id': str(trader_id),
                         'counterparty': str(counterparty_id)})
        return trade_data

    def one_hour_vwap(self, symbol):
        """
        Query the last one hour trade data and calculate the volume weighed
        average price as the settlement price

        :param symbol:
            A string
        :return:
            A float
        """
        till_time = datetime.datetime.now()
        from_time = till_time - datetime.timedelta(hours=1)
        query = ('/api/2/public/trades/{}?sort=DESC&by=timestamp&'
                 'from={}&till={}&limit=1000'.format(symbol, from_time,
                                                    till_time))
        one_hour_data = self.session.get(self.url+query).json()
        vwap = self.settlement.settlement_price(one_hour_data)
        return vwap
