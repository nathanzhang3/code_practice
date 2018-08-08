import pymysql
import os
import csv

HOST = "carloudydbtest.cqofkkppbnkd.us-east-2.rds.amazonaws.com"
PORT = 3306
USERNAME = "codetester"
PASSWORD = "getonrocket"


class DataBase(object):
    """
    This is the database.
    The database can store streamed data into databases.
    """
    def __init__(self, symbol='BTCUSD', host=HOST, port=PORT, uname=USERNAME,
                 pw=PASSWORD, dbname='Bitfinex'):
        # symbol of the pair this database will store information for
        self.sym = symbol

        # SQL connection related variables
        self.host = host
        self.port = port
        self.uname = uname
        self.pw = pw

        # order book stored as dictionary
        self.order_book = {}

        # sql database and table names
        self.dbname = dbname
        self.trade_tname = 'Trades_' + self.sym
        self.quote_tname = 'Quotes_' + self.sym

        # csv names
        self.trade_csvpath = 'data/bitfinex_trades_'+self.sym+'.csv'
        self.quote_csvpath = 'data/bitfinex_quotes_'+self.sym+'.csv'

    def initialize_trade_csv(self):
        # Remove previous files
        try:
            os.remove(self.trade_csvpath)
        except OSError:
            pass

        # Create csv file to store trades data
        with open(self.trade_csvpath, 'a') as file:
            writer = csv.writer(file, delimiter = ',')
            writer.writerow(['ID', 'Timestamp', 'Amount', 'Price'])

    def initialize_quote_csv(self):
        # Remove previous files
        try:
            os.remove(self.quote_csvpath)
        except OSError:
            pass

        # Create csv file to store orders data
        with open(self.quote_csvpath, 'a') as file:
            writer = csv.writer(file, delimiter = ',')
            writer.writerow(['Price', 'Count', 'Amount'])

    def initialize_sql_db(self):
        try:
            # Create a mysql connection
            self.conn = pymysql.connect(host=self.host, user=self.uname,
                                        port=self.port, passwd=self.pw)

            # Create a cursor object
            self.cur = self.conn.cursor()

            # Execute the sqlQuery
            self.cur.execute('SHOW DATABASES')

            # Fetch all the rows
            databaseList = self.cur.fetchall()

            if (self.dbname, ) not in databaseList:
                # Execute the create database SQL statment through the cursor
                # instance
                self.cur.execute('CREATE DATABASE ' + dbname)
                print('Database created.')
            else:
                print('Database already exists.')
        except Exception as e:
            print('Exception occured:()'.format(e))

    def initialize_trade_sql(self):
        self.conn = pymysql.connect(host=self.host, user=self.uname,
                                    port=self.port, passwd=self.pw,
                                    db=self.dbname)

        self.cur = self.conn.cursor()

        self.cur.execute('SHOW TABLES')

        tableList = self.cur.fetchall()

        if (self.trade_tname,) not in tableList:
            self.cur.execute('CREATE TABLE '+self.trade_tname+'(ID VARCHAR(10),\
             Timestamp VARCHAR(20), Amount float, Price float)')
        else:
            self.cur.execute('TRUNCATE TABLE '+self.trade_tname)

    def initialize_quote_sql(self):
        self.conn = pymysql.connect(host=self.host, user=self.uname,
                                    port=self.port, passwd=self.pw,
                                    db=self.dbname)

        self.cur = self.conn.cursor()

        self.cur.execute('SHOW TABLES')

        tableList = self.cur.fetchall()

        if (self.quote_tname,) not in tableList:
            self.cur.execute('CREATE TABLE '+self.quote_tname+'(Price float, \
                Count int, Amount float)')
        else:
            self.cur.execute('TRUNCATE TABLE '+self.quote_tname)

    def create_order_book(self, snapshot):
        for row in snapshot[0][0]:
            self.order_book[row[0]] = row[1:]

    def create_quote_csv(self, snapshot):
        for row in snapshot[0][0]:
            with open(self.quote_csvpath, 'a') as file:
                writer = csv.writer(file, delimiter = ',')
                writer.writerow(row)

    def create_quote_sql(self, snapshot):
        for row in snapshot[0][0]:
            insertStatement = 'INSERT INTO '+self.quote_tname+' (Price, Count, \
                Amount) VALUES ('+str(row[0])+','+str(row[1])+','+str(row[2])+')'
            self.cur.execute(insertStatement)

    def update_trade_csv(self, new_trade):
        if new_trade[0][0] == 'te': # keep only real-time data
            with open(self.trade_csvpath, 'a') as file:
                writer = csv.writer(file, delimiter = ',')
                writer.writerow(new_trade[0][1])

    def update_trade_sql(self, new_trade):
        if new_trade[0][0] == 'te': # keep only real-time data
            insertStatement = 'INSERT INTO '+self.trade_tname+' (ID, Timestamp,\
             Amount, Price) VALUES ('+str(new_trade[0][1][0])+','+ \
             str(new_trade[1])+','+str(new_trade[0][1][2])+','+ \
             str(new_trade[0][1][3])+')'
            self.cur.execute(insertStatement)

    def update_quote_csv(self, quote_chg):
        price = quote_chg[0][0][0]
        count = quote_chg[0][0][1]
        amount = quote_chg[0][0][2]

        if count > 0:
            self.order_book[price] = quote_chg[0][0][1:]
        elif count == 0:
            if price in self.order_book.keys():
                del self.order_book[price]

        os.remove(self.quote_csvpath)

        with open(self.quote_csvpath, 'a') as file:
            writer = csv.writer(file, delimiter = ',')
            writer.writerow(['Price', 'Count', 'Amount'])

        for key, value in self.order_book.items():
            with open(self.quote_csvpath, 'a') as file:
                writer = csv.writer(file, delimiter = ',')
                writer.writerow([key, value[0], value[1]])

    def update_quote_sql(self, quote_chg):
        price = quote_chg[0][0][0]
        count = quote_chg[0][0][1]
        amount = quote_chg[0][0][2]



    def terminate_sql(self):
        self.conn.close()
