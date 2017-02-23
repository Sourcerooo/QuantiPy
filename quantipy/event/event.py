MARKET_EVENT_STOCKS = "MARKET_STOCKS"
MARKET_EVENT_OPTIONS = "MARKET_OPTIONS"
MARKET_EVENT_FUTURES = "MARKET_FUTURES"
TRADE_EVENT = "TRADE"
ORDER_EVENT = "ORDER"
FILL_EVENT = "FILL"

BUY = "buy"
SELL = "sell"


class Event(object):
    """" Base class to provide the necessary interface for all events that can be triggered within QuantiPy"""
    def __init__(self, type, data):
        self.type = type
        self.data = data


class MarketEventStocks(Event):
    def __init__(self, market_data):
        global MARKET_EVENT_STOCKS
        super().__init__(MARKET_EVENT_STOCKS, market_data)


class MarketEventOptions(Event):
    def __init__(self, market_data):
        global MARKET_EVENT_OPTIONS
        super().__init__(MARKET_EVENT_OPTIONS, market_data)


class MarketEventFutures(Event):
    def __init__(self, market_data):
        global MARKET_EVENT_FUTURES
        super().__init__(MARKET_EVENT_FUTURES, market_data)


class TradeEvent(Event):
    def __init__(self, buy_sell_indicator, trade_data):
        self.buy_sell_indicator = buy_sell_indicator
        global TRADE_EVENT
        super().__init__(TRADE_EVENT, trade_data)


class OrderEvent(Event):
    def __init__(self, order_data):
        global ORDER_EVENT
        super().__init__(ORDER_EVENT, order_data)


class FillEvent(Event):
    def __init__(self, fill_data):
        global FILL_EVENT
        super().__init__(FILL_EVENT, fill_data)


