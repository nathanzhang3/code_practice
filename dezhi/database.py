from sqlalchemy import (Table, Column, Integer, String, FLOAT,
                        MetaData, create_engine, select)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settlement import Settlement

class DataBase(object):
    """
    This is the database.
    When create database, provide your own configs.
    """
    def __init__(self, trader_dict, user_name='postgres', password='123456',
                 ip='5432', database_name='postgres'):
        database_url = ('postgresql://{}:{}@localhost:{}/{}'.format(
            user_name, password, ip, database_name))
        self.engine = create_engine(database_url)
        self.metadata = MetaData(self.engine)
        self.tradetable = self.build_trade_table()
        self.balancetable = self.build_balance_table(trader_dict)
        self.settlementtable = self.build_settlements_table()
        self.conn = self.engine.connect()
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()
        self.settlement = Settlement()

    def drop_all(self):
        self.metadata.drop_all(bind=self.engine, tables='balances')

    def build_trade_table(self):
        """
        Build a table for trade data
        """
        tradetable = Table('trades', self.metadata,
                          Column('id', Integer, primary_key=True),
                          Column('price', String(50)),
                          Column('timestamp', String(50)),
                          Column('symbol', String(50)),
                          Column('side', String(50)),
                          Column('quantity', String(50)),
                          Column('trader_id', String(50)),
                          Column('counterparty', String(50)))
        self.metadata.create_all()
        return tradetable

    def build_balance_table(self, trader_dict):
        """
        Build a table for balance and initialize this table according to
        trader's balance

        :param trader_dict:
            A list of Trader class
        """
        balancetable = Table('balances', self.metadata,
                             Column('trader_id', String(50),
                                    primary_key=True),
                             Column('balance', FLOAT))
        self.metadata.drop_all()
        self.metadata.create_all()
        initial_balance = [{'trader_id': id, 'balance': trader.balance} for
                          id, trader in trader_dict.items()]
        self.engine.execute(balancetable.insert(), initial_balance)
        return balancetable

    def build_settlements_table(self):
        """
        Build a table for settlements
        """
        settlementstable = Table('settlements', self.metadata,
                                 Column('id', Integer, primary_key=True),
                                 Column('from_participant', String(50)),
                                 Column('to_participant', String(50)),
                                 Column('currency', FLOAT))
        self.metadata.create_all()
        return settlementstable

    def write_trade_data(self, trade_data):
        """
        Write trade data to trade table
        :param trade_data:
            A list of dict
        """
        self.engine.execute(self.tradetable.insert(), trade_data)

    def write_settlement_data(self, trade_data, stl_price):
        """
        Write settlement data to settlements table

        :param trade_data:
            A list of dict
        :param stl_price:
            A float
        """
        settlement_data = []
        for data in trade_data:
            stl_data = self.settlement.settlement_obligation(data, stl_price)
            settlement_data.append(stl_data)
        self.engine.execute(self.settlementtable.insert(), settlement_data)
        return settlement_data

    def write_balance_data(self, settlement_data):
        """
        Find trader according to trader_id and update his balance

        :param settlement_data:
            A list of dict
        """
        for data in settlement_data:
            from_trader_bal = self.query_balance(data['from_participant'])
            to_trader_bal = self.query_balance(data['to_participant'])
            bal_data = self.settlement.settlement_balance(from_trader_bal,
                                            to_trader_bal, data['currency'])
            from_bal = self.balancetable.update().where(
                self.balancetable.c.trader_id == data[
                    'from_participant']).values(balance=bal_data[
                'from_trader_bal'])
            rsf = self.conn.execute(from_bal)
            to_bal = self.balancetable.update().where(
                self.balancetable.c.trader_id == data[
                    'to_participant']).values(balance=bal_data[
                'to_trader_bal'])
            rst = self.conn.execute(to_bal)

    def query_balance(self, trader_id):
        """
        Query the balance of a trader according to trader_id

        :param trader_id:
            A string
        :return:
            A float
        """
        trader = self.session.query(self.balancetable).filter(
            self.balancetable.c.trader_id == trader_id).first()
        balance = trader.balance
        return balance
