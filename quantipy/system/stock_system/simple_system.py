import quantipy.event.event as qEvent
from quantipy.system.base import AbstractSystem
import uuid


class BuyAndHoldSystem(AbstractSystem):
    def __init__(self, event_queue, symbols, data_handler):
        self.data_handler = data_handler
        self.event_queue = event_queue
        self.symbols = symbols
        self.buy_indicator = self._reset_buy_indicator(self.symbols)

    def _reset_buy_indicator(self, symbols):
        bought = {}
        for symbol in symbols:
            bought[symbol] = False
        return bought

    def calculate(self, event):
        if event.type != qEvent.MARKET_EVENT_STOCKS:
            return
        else:
            symbol = event.data["symbol"]
            if symbol not in self.symbols:
                return

            if not self.buy_indicator[symbol]:
                self.buy_indicator[symbol] = True
                trade_data = {"trade_id": uuid.uuid4(),
                              "market_price": event.data["market_price"],
                              "bid": event.data["bid"],
                              "ask": event.data["ask"],
                              "buy_sell_indicator": qEvent.BUY}
                trade = qEvent.TradeEvent(qEvent.BUY, trade_data)
                self.event_queue.put(trade)
