import pymysql
import os
import csv
import logging


HOST = "carloudydbtest.cqofkkppbnkd.us-east-2.rds.amazonaws.com"
PORT = 3306
USERNAME = "codetester"
PASSWORD = "getonrocket"

logger = logging.getLogger(__name__)


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
        """
        Initialize the trade CSV file with column names.
        """
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
        """
        Initialize the quote CSV file with column names.
        """
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
        """
        Connect with sql database and create a cursor object.
        Intialize a database if not already exist.
        """
        try:
            # Create a mysql connection
            self.conn = pymysql.connect(host=self.host, user=self.uname,
                                        port=self.port, passwd=self.pw)

            # Create a cursor object
            self.cur = self.conn.cursor()

            # Execute the sqlQuery to get all database names
            self.cur.execute('SHOW DATABASES')

            # Fetch all the rows
            databaseList = self.cur.fetchall()

            if (self.dbname, ) not in databaseList:
                # Execute the create database SQL statment through the cursor
                # instance
                self.cur.execute('CREATE DATABASE ' + dbname)
            else:
                logger.info('Database already exists.')
        except Exception as e:
            logger.error('Exception occured:()'.format(e))

    def initialize_trade_sql(self):
        """
        Connect with created database and create a corresponding cursor object.
        Intialize a trade table if not already exist.
        """
        # Create a mysql connection
        self.conn = pymysql.connect(host=self.host, user=self.uname,
                                    port=self.port, passwd=self.pw,
                                    db=self.dbname)

        # Create a cursor object
        self.cur = self.conn.cursor()

        # Execute the sqlQuery to get all table names
        self.cur.execute('SHOW TABLES')

        # Fetch all the rows
        tableList = self.cur.fetchall()

        # If the trade table does not already exist, create new one
        if (self.trade_tname,) not in tableList:
            self.cur.execute('CREATE TABLE '+self.trade_tname+'(Id VARCHAR(10) \
                NOT NULL, Timestamp VARCHAR(20), Amount float, Price float, \
                PRIMARY KEY (Id))')
        # If the trade table already exist, remove all existing rows
        else:
            self.cur.execute('TRUNCATE TABLE '+self.trade_tname)

    def initialize_quote_sql(self):
        """
        Connect with created database and create a corresponding cursor object.
        Intialize a quote table if not already exist.
        """
        # Create a mysql connection
        self.conn = pymysql.connect(host=self.host, user=self.uname,
                                    port=self.port, passwd=self.pw,
                                    db=self.dbname)

        # Create a cursor object
        self.cur = self.conn.cursor()

        # Execute the sqlQuery to get all table names
        self.cur.execute('SHOW TABLES')

        # Fetch all the rows
        tableList = self.cur.fetchall()

        # If the quote table does not already exist, create new one
        if (self.quote_tname,) not in tableList:
            self.cur.execute('CREATE TABLE '+self.quote_tname+'(Price float NOT\
                NULL, Count int, Amount float, PRIMARY KEY(Price))')
        # If the quote table already exist, remove all existing rows
        else:
            self.cur.execute('TRUNCATE TABLE '+self.quote_tname)

    def create_order_book(self, snapshot):
        """
        Create the initial order book from the snapshot from exchange.

        :param snapshot:
            a list of lists, containing top 100 levels of bid and ask prices
        """
        for row in snapshot[0][0]:
            self.order_book[row[0]] = row[1:]

    def create_quote_csv(self, snapshot):
        """
        Create the csv file for the order book.

        :param snapshot:
            a list of lists, containing top 100 levels of bid and ask prices
        """
        for row in snapshot[0][0]:
            with open(self.quote_csvpath, 'a') as file:
                writer = csv.writer(file, delimiter = ',')
                writer.writerow(row)

    def create_quote_sql(self, snapshot):
        """
        Create the sql db for the order book.

        :param snapshot:
            a list of lists, containing top 100 levels of bid and ask prices
        """
        for row in snapshot[0][0]:
            # Insert statement to be executed
            insertStatement = 'INSERT INTO '+self.quote_tname+' (Price, Count, \
                Amount) VALUES ('+str(row[0])+','+str(row[1])+','+str(row[2])+')'
            self.cur.execute(insertStatement)

    def update_trade_csv(self, new_trade):
        """
        Add the real-time trade data with timestamp to trade csv file

        :param new_trade:
            a list, containing the information of the newly streamed trades
        """
        if new_trade[0][0] == 'te': # keep only real-time data
            with open(self.trade_csvpath, 'a') as file:
                writer = csv.writer(file, delimiter = ',')
                writer.writerow(new_trade[0][1])

    def update_trade_sql(self, new_trade):
        """
        Add the real-time trade data with timestamp to trade sql db

        :param new_trade:
            a list, containing the information of the newly streamed trades
        """
        # Create a mysql connection
        self.conn = pymysql.connect(host=self.host, user=self.uname,
                                    port=self.port, passwd=self.pw,
                                    db=self.dbname)

        # Create a cursor object
        self.cur = self.conn.cursor()

        # Insert the trade into sql db as a new row
        if new_trade[0][0] == 'te': # keep only real-time data
            insertStatement = 'INSERT INTO '+self.trade_tname+' (ID, Timestamp,\
                Amount, Price) VALUES ('+str(new_trade[0][1][0])+','+ \
                str(new_trade[1])+','+str(new_trade[0][1][2])+','+ \
                str(new_trade[0][1][3])+')'

            # Execute the sqlQuery to insert new row
            self.cur.execute(insertStatement)

    def update_quote_csv(self, quote_chg):
        """
        Add the quote update to quote csv file

        :param quote_chg:
            a list, containing the information of the update
        """
        # Store quote information
        price = quote_chg[0][0][0]
        count = quote_chg[0][0][1]
        amount = quote_chg[0][0][2]

        # When count > 0 then add or update the price level
        if count > 0:
            self.order_book[price] = quote_chg[0][0][1:]
        # When count = 0 then delete the price level.
        elif count == 0:
            if price in self.order_book.keys():
                del self.order_book[price]

        # Remove old order book for updated quotes
        os.remove(self.quote_csvpath)

        # Write column names
        with open(self.quote_csvpath, 'a') as file:
            writer = csv.writer(file, delimiter = ',')
            writer.writerow(['Price', 'Count', 'Amount'])

        # Write rows into new orderbook csv file
        for key, value in self.order_book.items():
            with open(self.quote_csvpath, 'a') as file:
                writer = csv.writer(file, delimiter = ',')
                writer.writerow([key, value[0], value[1]])

    def update_quote_sql(self, quote_chg):
        """
        Add the quote update to quote sql db

        :param quote_chg:
            a list, containing the information of the update
        """
        price = quote_chg[0][0][0]
        count = quote_chg[0][0][1]
        amount = quote_chg[0][0][2]

        # When count > 0 then add or update the price level
        if count > 0:
            self.order_book[price] = quote_chg[0][0][1:]
        # When count = 0 then delete the price level.
        elif count == 0:
            if price in self.order_book.keys():
                del self.order_book[price]

        # Create a mysql connection
        self.conn = pymysql.connect(host=self.host, user=self.uname,
                                    port=self.port, passwd=self.pw,
                                    db=self.dbname)
        # Create a cursor object
        self.cur = self.conn.cursor()

        # Update statement to be executed
        updateStatement = 'INSERT INTO '+self.quote_tname+' (Price, Count, \
            Amount) VALUES ('+str(price)+','+str(count)+','+str(amount)+') ON \
            DUPLICATE KEY UPDATE Count=VALUES(Count), Amount=VALUES(Amount)'
            
        # Excute update sql query
        self.cur.execute(updateStatement)

    def terminate_sql(self):
        """
        Terminate the connection with sql db
        """
        self.conn.close()
