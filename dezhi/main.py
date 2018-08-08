from trader import Trader, set_up_trader_id
from exchange import Exchange
import time

if __name__ == '__main__':
    """
    This is an example shows how the code work:
    - Create some traders and assign them tradier_id;
    - Create an exchange, and assign the traders and database for it;
    - Initialize the exchange
    - Use method settle_trigger to settle the trade data from the time of 
      initialization till time of first settle_trigger
    - Call method settle_trigger to settle the new trade data since the 
      previous execution
    """
    trader_dict = {'0': Trader(), '1': Trader(),
                     '2': Trader(), '3': Trader(),
                    '4': Trader(), '5': Trader(),
                     '6': Trader(), '7': Trader(),
                     '8': Trader(), '9': Trader()}
    set_up_trader_id(trader_dict)
    exchange = Exchange()
    exchange.assign_traders(trader_dict)
    exchange.assign_database()
    exchange.initialize()
    exchange.settle_trigger(['ETHUSD', 'BTCUSD'])
    time.sleep(60)
    exchange.settle_trigger(['ETHUSD', 'BTCUSD'])

