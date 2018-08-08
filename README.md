# Code Test Project

The goal of the project is to write a Python program to stream and save a crypto currency’s trading activities on an exchange into a csv file and a SQL database.


How to run:
	1. Packages:
		The code is written in Python3.6 and requires several third-party packages: pymysql, btfxWss, and plivo. Make sure you have the correct Python version. The packages can be installed with following commands in console:

		$ pip install pymysql
		$ pip install btfxWss
		$ pip install plivo

		Despite of its incomplitness, the tests files will require Pytest package, which can be installed with the command:

		$pip install pytest

		Alternatively, you can locate to the project folder and use the reuirements.txt file:

		$ pip install -r requirements.txt
	
	2. Linux command:
		Running the python files with following command in console:
		python main.py

		If your default version is python2.*, then try this:
		python3 main.py


Project files:

	1. main.py:
		The main function to start and execute

	2. market.py:
		A Market object that interact with Bitfinex Websocket API and backend database.

		1) __init__: 
			Initialize the market of the crypto and subscribe to trades and order books. Data is stored as Queues;

		2) check_connection:
			Check connection with Bitfinex API. If consecutively failing to connect, the program will send an alert message;

		3) initialize_api:
			Initialize the API for the crypto market and subscribe to trades and order books. Data is stored as Queues;

		4) create_database:
			This function will build connection with Bitfinex Websocket API and AWS 
	        MySQL DB. Then initialize the csv files and sql databases for trades and orderbook;
	 	
	 	5) stream_data:
	 		This function access the live data with established Bitfinex API, and 
	        keep streaming new trade and quote data. Then update the csv files and 
	        sql databases accordingly;

	3. database.py
		A DataBase object that keep trade data and order book, and save streamed data into csv and sql databases.

		1) __init__:
			Initialize the database for the given pair;

		2) initialize_trade_csv:
			Initialize the trade CSV file with column names;

		3) initialize_quote_csv:
			Initialize the quote CSV file with column names;

		4) initialize_sql_db:
			Connect with sql database and create a cursor object. Intialize a database if not already exist;

		5) initialize_trade_sql:
			Connect with created database and create a corresponding cursor object.
	        Intialize a trade table if not already exist;

	    6) initialize_quote_sql:
	    	Connect with created database and create a corresponding cursor object.
	        Intialize a quote table if not already exist;

	    7) create_order_book:
	    	Create the initial order book from the snapshot from exchange;

	    8) create_quote_csv:
	    	Create the csv file for the order book;

	   	9) create_quote_sql:
	   		Create the sql db for the order book;

	   	10) update_trade_csv:
	   		Add the real-time trade data with timestamp to trade csv file;

	   	11) update_trade_sql:
	   		Add the real-time trade data with timestamp to trade sql db;

	   	12) update_quote_csv:
	   		Add the quote update to quote csv file;

	   	13) update_quote_sql: 
	   		Add the quote update to quote sql db;

	   	14) terminate_sql:
	   		Terminate the connection with sql db;


Data:
	Data can be found in the data directory. There will be four csv files: quotes data and trades data for each of BTCUSD and ETHUSD pairs. There are some sample data provided.

	The bitfinex_quotes files contains the most up to date order book from Bitfinex;
	The bitfinex_trades files contain the information of most recent trades.

	The same data are stored in AWS MYSQL DB in the given link (carloudydbtest.cqofkkppbnkd.us-east-2.rds.amazonaws.com).


Log:
	The logs can be found in the same directory with the python files, after running the main.py file.


Tests:
	The test section has not finished. Pytest is intended to be utilized for the tests.


Problems:
	1. Initially I wanted to have it running on given AWS cloud and have uploaded files. However I could not install pymysql on the cloud due to "EnvironmentError: [Errno 13] Permission denied: '/usr/local/lib/python3.5/dist-packages/PyMySQL-0.9.2.dist-info'"

	2. Despite of following the Plivo documentation, I could not get a test message I sent to myself. So I believe even though the check_connection function in Market object is supposed to send the notification, it is highly likely that user will not successfully receive this notification.

