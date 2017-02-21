from abc import ABCMeta, abstractmethod
import pandas as pd
from quantipy.data_management.data_import import YahooStockImport
from quantipy.basics.event import MarketEventStocks


class DataHandler(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_latest_data(self,N=1):
        raise NotImplementedError("get_latest_data() not implemented")

    @abstractmethod
    def update_data(self):
        raise NotImplementedError("update_data() not implemented")


class OptionVueCSVHandler(DataHandler):
    def __init__(self, event_queue, filename):
        self.event_queue = event_queue
        self.filename = filename

        self.data = {}
        self.latest_data = {}
        self.continue_backtest = True

        #self.datastream = OptionVueImport()
        #self.stocks_data, self.futures_data, self.options_data = self.datastream.import_data(self.filename)

class YahooHistoricalHander(DataHandler):
    def __init__(self, event_queue, symbols):
        self.event_queue = event_queue
        self.symbols = symbols

        self.data = pd.DataFrame()
        self.latest_data = pd.DataFrame()
        self.continue_backtest = True

        self.datastream = YahooStockImport()
        self.data = self.datastream.import_data(self.symbols)
        self.data.reset_index(inplace=True)
        self.data.set_index(["symbol", "date"], inplace=True)
        self.data.sort_index(inplace=True)

        self.iterator = {}
        for symbol, new_df in self.data.groupby(level=0):
            self.iterator[symbol] = self.data.loc[symbol].iterrows()

        #self.generator = self._get_next_data()

    def _get_next_data(self, symbol):
        return self.data[symbol].next()
        # for date, new_df in self.data.groupby(level=0):
        #     yield new_df

    def get_latest_data(self, no=1, symbol=[]):
        pass

    def update_data(self):
        for symbol in self.symbols:
            try:
                df = next(self.iterator[symbol])
            except StopIteration:
                self.continue_backtest = False
            else:
                if df:
                    self.latest_data[symbol] = self.latest_data[symbol].append(df)
                    #self.event_queue.put(MarketEventStocks(df))
