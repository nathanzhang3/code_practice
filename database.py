import pymysql
import os

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

    def initialize_trade_csv(self):
        self.trade_fname = 'bitfinex_trades_'+self.sym+'.csv'

        # Remove previous files
        try:
            os.remove(self.trade_fname)
        except OSError:
            pass

        # Create csv file to store trades data
        with open(trade_fname, 'a') as file:
            writer = csv.writer(file, delimiter = ',')
            writer.writerow(['ID', 'Timestamp', 'Amount', 'Price'])

    def initialize_quote_csv(self):
        self.quote_fname = 'bitfinex_quotes_'+self.sym+'.csv'

        # Remove previous files
        try:
            os.remove(self.quote_fname)
        except OSError:
            pass

        # Create csv file to store orders data
        with open(quote_fname, 'a') as file:
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

    def create_order_book_csv(self, snapshot):
        for row in snapshot[0][0]:
            with open('streaming_orders_'+self.symbol+'.csv', 'a') as file:
                writer = csv.writer(file, delimiter = ',')
                writer.writerow(row)

    def create_sql_db(self, ):
        try:
            # Execute the sqlQuery
            self.cur.execute('SHOW DATABASES')

            #Fetch all the rows
            databaseList = self.cur.fetchall()

            if (dbname, ) in databaseList:
                # Execute the create database SQL statment through the cursor
                # instance
                self.cur.execute('CREATE DATABASE' + dbname)
                print('Database created.')
            else:
                print('Database exists.')
