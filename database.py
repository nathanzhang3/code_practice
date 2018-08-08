import pymysql
import os
import csv

HOST = "carloudydbtest.cqofkkppbnkd.us-east-2.rds.amazonaws.com"
PORT = 3306
DBNAME = "ForRPython"
USERNAME = "codetester"
PASSWORD = "getonrocket"


class DataBase(object):
    """
    This is the database.
    The database can store streamed data into databases.
    """
    def __init__(self, symbol='BTCUSD',host=HOST, port=PORT, dbname=DBNAME,
                 uname=USERNAME, pw=PASSWORD):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.uname = uname
        self.pw = pw
        self.sym = symbol
        self.order_book = {}

    def initialize_trade_csv(self):
        self.trade_fname = 'data/bitfinex_trades_'+self.sym+'.csv'

        # Remove previous files
        try:
            os.remove(self.trade_fname)
        except OSError:
            pass

        # Create csv file to store trades data
        with open(self.trade_fname, 'a') as file:
            writer = csv.writer(file, delimiter = ',')
            writer.writerow(['ID', 'Timestamp', 'Amount', 'Price'])

    def initialize_quote_csv(self):
        self.quote_fname = 'data/bitfinex_quotes_'+self.sym+'.csv'

        # Remove previous files
        try:
            os.remove(self.quote_fname)
        except OSError:
            pass

        # Create csv file to store orders data
        with open(self.quote_fname, 'a') as file:
            writer = csv.writer(file, delimiter = ',')
            writer.writerow(['Price', 'Count', 'Amount'])

    def initialize_sql_db(self, dbname = 'test_db'):
        bitfinex_quotes,
        bitfinex_trades
        # Create a mysql connection
        self.conn = pymysql.connect(self.host, user=self.uname, port=self.port,
                                    passwd=self.pw)

        # Create a cursor object
        self.cur = self.conn.cursor()

    def create_quote_csv(self, snapshot):
        for row in snapshot[0][0]:
            self.order_book[row[0]] = row[1:]
            with open('data/bitfinex_quotes_'+self.sym+'.csv', 'a') as file:
                writer = csv.writer(file, delimiter = ',')
                writer.writerow(row)
        print(self.order_book)

    def create_sql_db(self):
        # Execute the sqlQuery
        self.cur.execute('SHOW DATABASES')

        #Fetch all the rows
        databaseList = self.cur.fetchall()

        if (dbname, ) in databaseList:
            # Execute the create database SQL statment through the cursor
            # instance
            self.cur.execute('CREATE DATABASE' + dbname)
            #print('Database created.')
        else:
            print('Database exists.')

    def update_trade_csv(self, new_trade):
        if new_trade[0][0] == 'te': # keep only real-time data
            with open('data/bitfinex_trades_'+self.sym+'.csv', 'a') as file:
                writer = csv.writer(file, delimiter = ',')
                writer.writerow(new_trade[0][1])

    def update_quote_csv(self, quote_chg):
        price = quote_chg[0]
        count = quote_chg[1]
        amount = quote_chg[2]

        if count > 0:
            if amount > 0:
                if price in self.order_book:
                    pass
                else:
                    pass
            elif amount < 0:
                if price in self.order_book:
                    pass
                else:
                    pass
        elif count == 0:
            if amount == 1:
                pass
            elif amount == -1:
                pass

        os.remove(self.quote_fname)

        for key, value in self.order_book.items():
            with open('data/bitfinex_quotes_'+self.sym+'.csv', 'a') as file:
                writer = csv.writer(file, delimiter = ',')
                writer.writerow([key, value[0], value[1]])
