import quantipy.event.event as qEvent
from quantipy.system.base import AbstractSystem
import uuid


class BuyAndHoldSystem(AbstractSystem):
    def __init__(self, event_queue, symbols, data_handler):
        self.system_id = uuid.uuid4()
        self.data_handler = data_handler
        self.event_queue = event_queue
        self.symbols = symbols
        self.buy_indicator = self._reset_buy_indicator(self.symbols)

    def _reset_buy_indicator(self, symbols):
        bought = {}
        for symbol in symbols:
            bought[symbol] = False
        return bought

    def update_statistic(self, data):
        # Todo: Implement statistics per system
        pass

    def calculate(self, data):
        if data.symbol not in self.symbols:
            return

        if not self.buy_indicator[data.symbol]:
            self.buy_indicator[data.symbol] = True
            trade_data = {"system_id": self.system_id,
                          "trade_id": uuid.uuid4(),
                          "seq_no": 1,
                          "symbol": data.symbol,
                          "amount": 1,
                          "market_price": data.market_price,
                          "bid": data.bid,
                          "ask": data.ask,
                          "buy_sell_indicator": qEvent.BUY}
            trade = qEvent.TradeEvent(qEvent.BUY, trade_data)
            self.event_queue.put(trade)
