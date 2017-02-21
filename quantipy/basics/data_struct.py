import datetime
import pandas as pd
from abc import ABCMeta, abstractmethod


class AbstractData(object):
    __metaclass__ = ABCMeta

    def to_pandas_df(self):
        dict1 = dict((key,self.__getattribute__(key)) for key in self.__dict__.keys())
        df = pd.DataFrame(data=[dict1])
        return df


class StocksData(AbstractData):
    def __init__(self):
        self.symbol = ""
        self.date = datetime.date.today()
        self.time = datetime.datetime.now().time()
        self.description = ""
        self.open = 0.0
        self.high = 0.0
        self.low = 0.0
        self.close = 0.0
        self.last = 0.0
        self.prev_close = 0.0
        self.volume = 0
        self.change = 0.0
        self.change_pct = 0.0
        self.open_interest = 0
        self.bid = 0.0
        self.ask = 0.0
        self.market_price = 0.0
        self.atm_iv = 0.0
        self.atm_sv = 0.0

        self.dtype = {"symbol": type(self.symbol),
                      "date": type(self.date)
                      }

    def to_pandas_df(self):
        df = super().to_pandas_df()
        df.set_index(["symbol", "date"], inplace=True)
        return df

    def set_data(self, data):
        keys = self.__dict__.keys()
        if len(keys) == len(data):
            for index, key in enumerate(keys):
                self.__setattr__(key, data[index])
        else:
            raise IndexError


class OptionsData(AbstractData):

    def __init__(self):
        self.base_symbol = ""
        self.exp_date = datetime.date.today()
        self.date = datetime.date.today()
        self.time = datetime.datetime.now().time()
        self.strike = 0.0
        self.p_c = ""
        self.dte = 0
        self.bid = 0.0
        self.ask = 0.0
        self.market_price = 0.0
        self.volume = 0
        self.open_interest = 0
        self.iv = 0.0
        self.delta = 0.0
        self.theta = 0.0
        self.gamma = 0.0
        self.vega = 0.0
        self.rho = 0.0

    def to_pandas_df(self):
        df = super().to_pandas_df()
        df.set_index(["base_symbol", "exp_date", "date", "time", "strike", "p_c"], inplace=True)
        return df

    def set_data(self, data):
        keys = self.__dict__.keys()
        if len(keys) == len(data):
            for index, key in enumerate(keys):
                self.__setattr__(key, data[index])
        else:
            raise IndexError


class FuturesData(AbstractData):
    def __init__(self):
        self.symbol = ""
        self.exp_date = datetime.date.today()
        self.date = datetime.date.today()
        self.time = datetime.datetime.now().time()
        self.description = ""
        self.dte = 0
        self.open = 0.0
        self.high = 0.0
        self.low = 0.0
        self.close = 0.0
        self.prev_close = 0.0
        self.last = 0.0
        self.volume = 0
        self.change = 0.0
        self.change_pct = 0.0
        self.open_interest = 0
        self.bid = 0.0
        self.ask = 0.0
        self.market_price = 0.0
        self.atm_iv = 0.0
        self.atm_sv = 0.0

    def to_pandas_df(self):
        df = super().to_pandas_df()
        df.set_index(["symbol", "exp_date", "date", "time"], inplace=True)
        return df

    def set_data(self, data):
        keys = self.__dict__.keys()
        if len(keys) == len(data):
            for index, key in enumerate(keys):
                self.__setattr__(key, data[index])
        else:
            raise IndexError
