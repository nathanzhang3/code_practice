from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import numpy as np

class Settlement(object):
    """
    This is the settlement.
    It has methods to calculate the settlement price, settlement obligation
    and settlement balance.
    """
    def __init__(self):
        pass

    def settlement_price(self, one_hour_data):
        """
        Calculate the volume weighted average price based on the last one hour
        trade data in USD

        :param one_hour_data:
            A list od dict
        :return:
            A float
        """
        price, quantity = zip(*[[float(data['price']),
                        float(data['quantity'])] for data in one_hour_data])
        vwap = np.dot(price, quantity) / np.sum(quantity)
        return round(vwap, 2)

    def settlement_obligation(self, one_trade_data, settlement_price):
        """
        Calculate the settlement obligation using formula:
            settlement obligation = abs(settlement price - trade price) *
                                                                quantity
        If the trader is buy side, and the price is greater than stl price,
        or the trader is sell side, and the price is lower than stl price,
        the currency is from trader to counter-party; otherwise,
        the currency is from counter-party to trader

        :param one_trade_data:
            A dict
        :param settlement_price:
            A float
        :return:
            A dict
        """
        side = one_trade_data['side']
        trade_price = float(one_trade_data['price'])
        quantity = float(one_trade_data['quantity'])
        trader_id = one_trade_data['trader_id']
        counterparty = one_trade_data['counterparty']
        stl_obligation = round(abs(settlement_price - trade_price) *
                               quantity, 2)
        stl_data = {'id': one_trade_data['id'], 'currency': stl_obligation}
        if ((side == 'buy') and (trade_price >= settlement_price)) or \
            ((side == 'sell') and (trade_price <= settlement_price)):
            stl_data.update({'from_participant': trader_id,
                             'to_participant': counterparty})
        else:
            stl_data.update({'from_participant': counterparty,
                             'to_participant': trader_id})
        return stl_data

    def settlement_balance(self, from_bal, to_bal, currency):
        """
        Update a trader's balance according to currency

        :param from_bal:
            A float
        :param to_bal:
            A float
        :param currency:
            A float
        :return:
            A dict
        """
        from_bal -= currency
        to_bal += currency
        return {'from_trader_bal': from_bal, 'to_trader_bal': to_bal}