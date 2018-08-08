import random

class Trader(object):
    def __init__(self, trader_id=None):
        self.trader_id = str(trader_id)
        self.balance = round(1000000 + 500000 * random.random(), 2)

def set_up_trader_id(trader_dict):
    """
    Assign trader_id to each trader

    :param trader_dict:
        A list of Trader class
    """
    trader_id = 0
    for name, trader in trader_dict.items():
        trader.trader_id = str(trader_id)
        trader_id += 1
