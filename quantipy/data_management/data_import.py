import os
import datetime
import pickle
import requests
import bs4 as bs
import pandas as pd
import pandas_datareader as web
from quantipy.basics.data_struct import StocksData, OptionsData, FuturesData

class BaseImport(object):
    mapping = {}
    datatypes = {}

    def __init__(self):
        self.dataframe = pd.DataFrame()

    def _enhance_data(self):
        pass

    def _data_cleansing(self):
        pass

    def _remap(self, mapping):
        self.dataframe.rename(columns=mapping, inplace=True)

    def import_data(self, **kwargs):
        if "datasource" not in kwargs:
            if self.dataframe.empty:
                return
        else:
            self.dataframe = kwargs["datasource"]

        if "mapping" in kwargs:
            self._remap(kwargs["mapping"])
        else:
            self._remap(self.mapping)

        self._data_cleansing()
        self._enhance_data()

        return self.dataframe


class BaseCSVImport(BaseImport):
    def __init__(self):
        super().__init__()
        self.datatypes = {}
        self.mapping = {}

    def import_data(self, filename, delimiter=",", **kwargs):
        if "datatypes" in kwargs:
            self.datatypes = kwargs["datatypes"]

        if "mapping" in kwargs:
            self.mapping = kwargs["mapping"]

        self.dataframe = pd.read_csv(filename, delimiter=delimiter, dtype=self.datatypes)
        super().import_data(mapping=self.mapping)
        return self.dataframe


class OptionVueImport(BaseCSVImport):
    """" Import data from a CSV file that was exported in OptionVue

         Todo: Futures import does not work correctly. Also the OptionVue export does not supply an expiration date
               for futures contracts as of 17.FEB.2017.
    """

    def __init__(self):
        super().__init__()
        self.datatypes = {
            "Time": "str",
            "Date": "str",
            "Exp.Date": "str"
        }
        self.mapping = {"Symbol": "symbol",
                           "Item Type": "type",
                           "Last": "last",
                           "Change": "change",
                           "High": "high",
                           "Low": "low",
                           "Volume": "volume",
                           "Theta": "theta",
                           "Time": "time",
                           "Asked": "ask",
                           "Bid": "bid",
                           "Date": "date",
                           "Delta": "delta",
                           "Description": "description",
                           "Exp.Date": "exp_date",
                           "Gamma": "gamma",
                           "Mid IV": "iv",
                           "Market Price": "market_price",
                           "Open": "open",
                           "Open Interest": "open_interest",
                           "Vega": "vega",
                           "Call/Put": "p_c",
                           "Previous Close": "prev_close",
                           "Rho": "rho",
                           "Strike Price": "strike",
                           "SV": "atm_sv"}

    def _data_cleansing(self):
        #drop columns that are not needed
        self.dataframe.drop(["Original Price", "Prob.Finish.ITM", "Projected Volty", "Time Premium", "Ask IV",
                             "At Price", "Existing Posn.", "Bid IV", "Pcnt To Double", "Percent O/U", "Th.Price",
                             "Trade"], axis=1, inplace=True)

        #fill NaN values for columns and set datatypes
        self.dataframe["volume"].fillna(0, inplace=True)
        self.dataframe["volume"].astype(int)
        self.dataframe["open_interest"].fillna(0, inplace=True)
        self.dataframe["open_interest"].astype(int)
        self.dataframe["exp_date"].fillna("", inplace=True)

        # Filter out all rows that don't have a market price, these couldn't be traded
        self.dataframe = self.dataframe[self.dataframe["market_price"] > 0.0]

        # If date columns are filled, prefix them with the century and convert to datetime object
        self.dataframe.loc[self.dataframe["date"] != "", "date"] = "20" + self.dataframe["date"]
        self.dataframe.loc[self.dataframe["exp_date"] != "", "exp_date"] = "20" + self.dataframe["exp_date"]
        self.dataframe["date"] = pd.to_datetime(self.dataframe["date"])
        self.dataframe["exp_date"] = pd.to_datetime(self.dataframe["exp_date"])

    def _enhance_dataframe(self):
        # Extract Symbol
        self.dataframe["symbol"] = self.dataframe["symbol"].str.split(' ').str[0]
        # Add close data to current data
        self.dataframe["close"] = self.dataframe["market_price"]
        # Add percent change
        self.dataframe["change_pct"] = (self.dataframe["close"]
                                        - self.dataframe["prev_close"]) / self.dataframe["prev_close"]
        self.dataframe["dte"] = (self.dataframe["exp_date"] - self.dataframe["date"]).dt.days

    def import_data(self, filename, delimiter=",", **kwargs):
        """ Import CSV files exported from OptionVue. These files contain stocks, futures and options data
            in the same file. The export structure is dynamic, depending on the list selected in OptionVue
        """
        super().import_data(filename, delimiter, **kwargs)

        #self.dataframe.to_csv("./Data/OptionVue/conv.csv", index=False, float_format='%.12g')

        stock_data = self.dataframe[self.dataframe["type"] == "S"]
        option_data = self.dataframe[self.dataframe["type"] == "G"].append(self.dataframe[self.dataframe["type"] == "O"])
        future_data = self.dataframe[self.dataframe["type"] == "F"]

        return stock_data, future_data, option_data


class YahooStockImport(BaseImport):
    _symbol_pickle_filename = "./Data/Yahoo/sp500tickers.pkl"
    _stock_dir = "./Data/Yahoo/Stocks"

    def __init__(self):
        super().__init__()
        # This is the mapping from Yahoo's web-data to the fieldnames used internally in QuantiPy
        self.mapping = {
            "Date": "date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Volume": "volume",
            "Close": "close",
            "Description": "description",
            "Symbol": "symbol"
        }

    def _enhance_data(self):
        # Last data = close
        self.dataframe["last"] = self.dataframe["close"]
        # Previous close from previously processed data
        self.dataframe["prev_close"] = self.dataframe["close"].shift(1)
        # Open Interest, yahoo doesn't have this info so set to 0
        self.dataframe["open_interest"] = 0
        # Market price is set to close, because no bid/ask available
        self.dataframe["market_price"] = self.dataframe["close"]
        # Bid/ask is set to close
        self.dataframe["bid"] = self.dataframe["close"]
        self.dataframe["ask"] = self.dataframe["close"]
        # Time is always EOD
        self.dataframe["time"] = datetime.time(22, 0)
        # Create change and change percent from previous
        self.dataframe["change"] = self.dataframe["close"] - self.dataframe["prev_close"]
        self.dataframe["change_pct"] = self.dataframe["change"] / self.dataframe["prev_close"]

    def _web_load_symbols(self):
        resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        soup = bs.BeautifulSoup(resp.text, "lxml")
        table = soup.find('table', {'class': 'wikitable sortable'})
        tickers = []
        for row in table.findAll('tr')[1:]:
            ticker, description = row.findAll('td')[0].text, row.findAll('td')[1].text
            tickers.append((ticker, description))

        with open(self._symbol_pickle_filename, "wb") as f:
            pickle.dump(tickers, f)
        return tickers

    def _load_symbols(self):
        if os.path.exists(self._symbol_pickle_filename):
            with open(self._symbol_pickle_filename, "rb") as f:
                tickers = pickle.load(f)
        else:
            tickers = self._web_load_symbols()
        return tickers

    def import_data(self, stock_symbol=[], from_date="2001-01-01", to_date="2099-01-01",
                    reload_sp500_symbols=False, reload_data=False, **kwargs):
        if not os.path.exists(self._stock_dir):
            os.makedirs(self._stock_dir)

        symbols = []
        if stock_symbol:
            symbols = stock_symbol
        else:
            if reload_sp500_symbols:
                symbols = self._web_load_symbols()
            else:
                symbols = self._load_symbols()

        if not symbols:
            return

        start_date = datetime.datetime.strptime(from_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(to_date, "%Y-%m-%d")

        del self.dataframe
        self.dataframe = pd.DataFrame()

        for symbol in symbols:
            if type(symbol) == str:
                symbol_to_load, description = symbol, symbol
            else:
                symbol_to_load, description = symbol[0], symbol[1]

            df = pd.DataFrame()
            if reload_data or not os.path.exists(self._stock_dir + "/{}.csv".format(symbol_to_load)):
                try:
                    df = web.DataReader(symbol_to_load, 'yahoo', start_date, end_date)
                    df["Description"] = description
                    df["Symbol"] = symbol_to_load
                    df.to_csv(self._stock_dir + "/{}.csv".format(symbol_to_load))
                    df.reset_index(inplace=True)
                except:
                    continue
            else:
                with open(self._stock_dir + "/{}.csv".format(symbol_to_load)) as datafile:
                    df = pd.read_csv(self._stock_dir + "/{}.csv".format(symbol_to_load), parse_dates=True)
                    # Filter all dates that are not within the selected period. Filtering a vector should be faster than
                    # Looping through csv
                    df = df[(df["Date"] >= from_date) & (df["Date"] <= to_date)]

            self.dataframe = self.dataframe.append(df)

        super().import_data()
        return self.dataframe
