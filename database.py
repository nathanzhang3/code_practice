import pymysql

HOST = "carloudydbtest.cqofkkppbnkd.us-east-2.rds.amazonaws.com"
PORT = 3306
DBNAME = "ForRPython"
USERNAME = "codetester"
PASSWORD = "getonrocket"


class DataBase(object):

    def __init__(self, host=HOST, port=PORT, dbname=DBNAME, uname=USERNAME,
                 pw=PASSWORD):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.uname = uname
        self.pw = pw

        # Create a connection
        self.conn = pymysql.connect(self.host, user=self.uname, port=self.port,
                                    passwd=self.pw)

        # Create a cursor object
        self.cur = self.conn.cursor()

    def create_db(self, dbname = 'test_db'):
        try:
            # Execute the sqlQuery
            self.cur.execute('SHOW DATABASES')

            #Fetch all the rows
            databaseList = self.cur.fetchall()

            if (dbname, ) in databaseList:
                # Execute the create database SQL statment through the cursor
                # instance
                self.cur.execute('CREATE DATABASE' + dbname)

            else:
                print('Database exists.')

    def
