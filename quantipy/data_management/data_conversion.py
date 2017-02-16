import csv
import datetime
from quantipy.basics.data import StocksData, FuturesData, OptionsData


class BaseConversion(object):
    def __init__(self):
        self.stock_mapping = {}
        self.futures_mapping = {}
        self.options_mapping = {}
        self.stocks = StocksData()
        self.futures = FuturesData()
        self.options = OptionsData()
        self.create_stock_mapping()
        self.create_futures_mapping()
        self.create_options_mapping()


    def create_stock_mapping(self):
        for index, key in enumerate(self.stocks.__dict__.keys()):
            self.stock_mapping[key] = index

    def create_futures_mapping(self):
        for index, key in enumerate(self.futures.__dict__.keys()):
            self.futures_mapping[key] = index

    def create_options_mapping(self):

        for index, key in enumerate(self.options.__dict__.keys()):
            self.options_mapping[key] = index

    def _map_data(self, data, mapping):
        data_mapped = []
        for key, value in mapping.items():
            try:
                data_mapped.append(data[value])
            except IndexError:
                continue
        return data_mapped

    def _enhance_data(self, data):
        return data

    def _data_cleansing(self, data):
        return data

    def import_csv(self, filename, delimiter=","):
        pass


class OptionVueConversion(BaseConversion):

    def __init__(self):
        super().__init__()
        self.id_field = 0
        self.type_field = 16

        self.stock_mapping = {
            "symbol": 37,
            "date": 10,
            "time": 7,
            "description": 12,
            "open": 18,
            "high": 3,
            "low": 4,
            "close": 39,
            "last": 1,
            "prev_close": 32,
            "volume": 5,
            "change": 2,
            "change_pct": 40,
            "open_interest": 19,
            "bid": 9,
            "ask": 8,
            "market_price": 17,
            "atm_sv": 36
        }

        self.options_mapping = {
            "base_symbol": 37,
            "exp_date": 13,
            "date": 10,
            "time": 7,
            "strike": 34,
            "p_c": 26,
            "dte": 41,
            "bid": 9,
            "ask": 8,
            "market_price": 17,
            "volume": 5,
            "open_interest": 19,
            "iv": 15,
            "delta": 11,
            "theta": 6,
            "gamma": 14,
            "vega": 24,
            "rho": 33
        }

        self.futures_mapping = {
            "symbol": 37,
            "exp_date": 13,
            "date": 10,
            "time": 7,
            "description": 12,
            "dte": 41,
            "open": 18,
            "high": 3,
            "low": 4,
            "close": 39,
            "prev_close": 32,
            "last": 1,
            "volume": 5,
            "change": 2,
            "change_pct": 40,
            "open_interest": 19,
            "bid": 9,
            "ask": 8,
            "market_price": 17,
            "atm_sv": 36
        }


    def _enhance_data(self, data):
        data = self._data_cleansing(data)
        if data:
            # Extract Symbol
            symbol = data[self.id_field].split()
            if len(symbol[0]) != 3:
                # This is a future contract, only /ES will be imported right now
                # Todo: Extract the future symbol from the ID
                data.append("ES")
            else:
                data.append(symbol[0])
            self.stock_mapping["symbol"] = len(data) - 1
            self.futures_mapping["symbol"] = len(data) - 1
            self.options_mapping["base_symbol"] = len(data) - 1

            # Add close data to current data
            close = data[self.stock_mapping["market_price"]]
            data.append(close)
            self.futures_mapping["close"] = len(data) - 1
            self.stock_mapping["close"] = len(data) - 1

            # Add percent change
            if close and data[self.stock_mapping["prev_close"]]:
                change_pct = float(close) - float(data[self.stock_mapping["prev_close"]])
                change_pct /= float(data[self.stock_mapping["prev_close"]])
            else:
                change_pct = 999
            data.append(change_pct)
            self.futures_mapping["change_pct"] = len(data) - 1
            self.stock_mapping["change_pct"] = len(data) - 1

            # Add "days to expiration" DTE
            if data[self.options_mapping["date"]] and data[self.options_mapping["exp_date"]]:
                current_date = datetime.datetime.strptime(data[self.options_mapping["date"]], "%Y%m%d")
                expiration_date = datetime.datetime.strptime(data[self.options_mapping["exp_date"]], "%Y%m%d")
                data.append((expiration_date-current_date).days)
            else:
                data.append(999)
            self.options_mapping["dte"] = len(data) - 1
            self.futures_mapping["dte"] = len(data) - 1

        return data

    def _type_conversion(self, data, mapping, obj):
        for key, value in mapping.items():
            if type(obj.__getattribute__(key)) is int:
                try:
                    if not data[value]:
                        data[value] = 0
                    else:
                        data[value] = int(data[value])
                except IndexError:
                    pass
            elif type(obj.__getattribute__(key)) is float:
                try:
                    if not data[value]:
                        data[value] = 0.0
                    else:
                        data[value] = float(data[value])
                except IndexError:
                    pass
            else:
                try:
                    if not data[value]:
                        data[value] = ""
                    else:
                        data[value] = str(data[value])
                except IndexError:
                    pass
        return data

    def _data_cleansing(self, data):
        if float(data[self.stock_mapping["market_price"]]) <= 0:
            return []

        data = self._type_conversion(data, self.stock_mapping, self.stocks)
        data = self._type_conversion(data, self.futures_mapping, self.futures)
        data = self._type_conversion(data, self.options_mapping, self.options)

        # Add century to date format yyyyMMdd
        if data[self.stock_mapping["date"]]:
            data[self.stock_mapping["date"]] = "20" + data[self.stock_mapping["date"]]
        if data[self.options_mapping["exp_date"]]:
            data[self.options_mapping["exp_date"]] = "20" + data[self.options_mapping["exp_date"]]

        return data

    def import_csv(self, filename, delimiter=","):
        stock_data = []
        option_data = []
        future_data = []
        with open(filename, "r") as inp_file:
            csv_data = csv.reader(inp_file, delimiter=delimiter)
            # Skip Header
            next(csv_data)
            for data in csv_data:
                data = self._enhance_data(data)
                if data:
                    if data[self.type_field] == "S":
                        stock_data.append(self._map_data(data, self.stock_mapping))
                    elif data[self.type_field] == "F":
                        future_data.append(self._map_data(data, self.futures_mapping))
                    elif data[self.type_field] in ["O", "G"]:
                        option_data.append(self._map_data(data, self.options_mapping))

        return stock_data, future_data, option_data
