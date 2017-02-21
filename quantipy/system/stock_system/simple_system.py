from quantipy.system.base_system import BaseSystem
import quantipy.basics.event as qEvent


class BuyAndHoldSystem(BaseSystem):
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
            data = self.data_handler.get_latest_data(symbol=symbols, no=1)
            data.set_index(columns=["symbol","date"])
            for symbol in self.symbols:
                if self.buy_indicator[symbol]:
                    continue
                else:
                    self.buy_indicator[symbol] = True
                    signal = qEvent.SignalEvent(data.loc[symbol][0], qEvent.BUY)
                    self.event_queue.put(signal)
