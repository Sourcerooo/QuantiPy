from abc import ABCMeta, abstractmethod
import pandas as pd
from quantipy.event.event import MarketEventStocks
from quantipy.data_management.data_import import YahooStockImport


class DataHandler(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_latest_data(self,N=1):
        raise NotImplementedError("get_latest_data() not implemented")

    @abstractmethod
    def update_data(self):
        raise NotImplementedError("update_data() not implemented")


class OptionVueCSVHandler(DataHandler):
    """ Todo: Implementation not finished yet """
    def __init__(self, event_queue, filename):
        self.event_queue = event_queue
        self.filename = filename

        self.data = {}
        self.latest_data = {}
        self.continue_backtest = True

        #self.datastream = OptionVueImport()
        #self.stocks_data, self.futures_data, self.options_data = self.datastream.import_data(self.filename)

class YahooHistoricalHandler(DataHandler):
    def __init__(self, event_queue, symbols, start_date=0, end_date=0):
        self.event_queue = event_queue
        self.symbols = symbols

        self.data = pd.DataFrame()
        self.latest_data = {}
        self.continue_update = True

        self.datastream = YahooStockImport()
        if start_date != 0 and end_date != 0:
            self.data = self.datastream.import_data(self.symbols, from_date=start_date, to_date=end_date)
        else:
            self.data = self.datastream.import_data(self.symbols)
        self.data.reset_index(inplace=True)
        self.data.set_index(["date"], inplace=True)
        self.data.sort_index(inplace=True)
        self.dates = list(self.data.index.unique())
        self.iter_dates = iter(self.dates)


    def get_latest_data(self, no=1, symbol=[]):
        pass

    def update_data(self):
        #Get next date in dataframe
        try:
            current_date = next(self.iter_dates)
        except StopIteration:
            self.continue_update = False
            return
        except Exception as e:
            #something went terribly wrong here
            return

        df = self.data.loc[current_date]
        for symbol in self.symbols:
            try:
                if isinstance(df, pd.DataFrame):
                    ep1 = df[df.symbol == symbol]
                    ep1 = ep1.iloc[0]
                elif isinstance(df, pd.Series):
                    ep1 = df
                else:
                    continue
            except:
                continue
            else:
                if not ep1.empty:
                    self.latest_data[symbol] = ep1
                    self.event_queue.put(MarketEventStocks(ep1))
