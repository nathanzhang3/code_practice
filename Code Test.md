Code Test (Data Analyst)
 
The goal of the code test project is to write a Python program to stream and save a crypto currency’s trading activities 
on an exchange into a csv file and a database with details as following:
 
 
 
1.      You should use the Bitfinex’s websocket API to subscribe to
 
https://bitfinex.readme.io/v2/reference#ws-public-order-books
 
https://bitfinex.readme.io/v2/reference#ws-public-trades
 
 
2.      Stream the trades and top 100 levels of order book events (bids and offers changes) of BTC/USD and ETH/USD symbols 
using the websocket API and save the result into a two separate csv files, one for trades, one for bids and offers. Also 
create two separate tables with names bitfinex_quotes,bitfinex_trades in the database and save the same results into 
database.
 
 
 
3.      This data streamer should keep running on the server. But there might be server connection disruption or other 
scenarios that stop your script from running. So you want to write a separate checker python script on the server to 
check if the streamer is still alive and pumping out data, if not we want to send a SMS text message (not multiple ones) 
to a phone number we provide to warn that something is wrong and need to be fixed, we also want to send a text message 
once the problem is fixed and the streamer is streaming and saving data again.
 
 
 
4.      Each order book event is a change to a specific price layer and its size, we are interested in keeping and 
reconstructing the entire order book based on each individual change. A snapshot of the initial order book status 
will be provided to you as a first result from the websocket order book subscription.
 
Then you can use the change events and trade events to update the snapshot.
 
   Write the top 100 layers of order book to a csv file and a database table whenever there is a change (in price or 
   size) within these layers.
 
 
 
The goal of the code test is to evaluate one’s Python coding skills in real world setting. You are given a handful 
of resources including:
 
 
 
An AWS EC2 instance with root access:
 
ssh codetester@ec2-52-14-130-177.us-east-2.compute.amazonaws.com
 
password: getonrocket
 
 
 
 
 
MYSQL DB Instance:
 
Endpoint:  carloudydbtest.cqofkkppbnkd.us-east-2.rds.amazonaws.com
 
 
 
      Port:   3306
 
      Same username/password as AWS EC2 instance
 
 
 
SMS API and account from Plivo:
 
https://developers.plivo.com/getting-started/messages/
 
 
 
AUTH ID: MAZTQ5MZHLYMIXZDG2NT
 
AUTH TOKEN:  YjhlZWU1ZjEzZmM2OTcyM2MwZjhjNzQ5ZWYxY2Fk
 
 
 
We are interested in the completeness of the exercise and your coding style. Based on your particular skill set, 
consider adding any of the following features (or expand on the core requirements with your own flair):
 
1.    Handles all data streams, including errors and unavailable data streams (restarting the websocket connection 
after sporadic disconnections)
 
2.    Logging relevant disconnections and other errors and timestamps of those errors
 
3.    Contains 90% or more test coverage, including edge case tests
 
The task should take 4 - 6 hours to complete. We ask that candidates send us their submissions within 24 hours.
