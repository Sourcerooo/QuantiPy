import csv
import datetime
from quantipy.basics.data import StocksData, FuturesData, OptionsData


class BaseImport(object):
    def __init__(self):
        self.stock_mapping = {}
        self.futures_mapping = {}
        self.options_mapping = {}
        self.stocks = StocksData()
        self.futures = FuturesData()
        self.options = OptionsData()
        self._create_stock_mapping()
        self._create_futures_mapping()
        self._create_options_mapping()

    def _create_stock_mapping(self):
        for index, key in enumerate(self.stocks.__dict__.keys()):
            self.stock_mapping[key] = index

    def _create_futures_mapping(self):
        for index, key in enumerate(self.futures.__dict__.keys()):
            self.futures_mapping[key] = index

    def _create_options_mapping(self):
        for index, key in enumerate(self.options.__dict__.keys()):
            self.options_mapping[key] = index

    def _type_conversion(self, data, import_type="S"):
        obj = 0
        if import_type == "S":
            obj = self.stocks
        elif import_type == "F":
            obj = self.futures
        elif import_type == "O":
            obj = self.options

        if obj:
            for index, key in enumerate(obj.__dict__.keys()):
                value = obj.__getattribute__(key)
                if type(value) is int:
                    try:
                        if not data[index]:
                            data[index] = 0
                        else:
                            data[index] = int(data[index])
                    except IndexError:
                        pass
                elif type(value) is float:
                    try:
                        if not data[index]:
                            data[index] = 0.0
                        else:
                            data[index] = float(data[index])
                    except IndexError:
                        pass
                else:
                    try:
                        if not data[index]:
                            data[index] = ""
                        else:
                            data[index] = str(data[index])
                    except IndexError:
                        pass

        return data

    def _map_data(self, data, import_type="S"):
        obj = 0
        mapping = {}
        if import_type == "S":
            obj = self.stocks
            mapping = self.stock_mapping
        elif import_type == "F":
            obj = self.futures
            mapping = self.futures_mapping
        elif import_type == "O":
            obj = self.options
            mapping = self.options_mapping

        data_mapped = []
        for key in obj.__dict__.keys():
            try:
                data_mapped.append(data[mapping[key]])
            except IndexError:
                data_mapped.append("NaN")
                continue
            except KeyError:
                data_mapped.append("")
                continue
        return data_mapped

    def _enhance_data(self, data):
        return data

    def _data_cleansing(self, data):
        return data

    def import_data(self, data, import_type="S"):
        data = self._data_cleansing(data)
        data = self._enhance_data(data)
        if import_type == "S":
            data = self._map_data(data, import_type)
            data = self._type_conversion(data, "S")
        elif import_type == "F":
            data = self._map_data(data, import_type)
            data = self._type_conversion(data, "F")
        elif import_type == "O":
            data = self._map_data(data, import_type)
            data = self._type_conversion(data, "O")
        return data


class BaseCSVImport(BaseImport):
    def __init__(self):
        super().__init__()

    def import_csv(self, filename, skip_header=False, delimiter=",", import_type="S"):
        result_data = []
        with open(filename, "r") as inp_file:
            csv_data = csv.reader(inp_file, delimiter=delimiter)
            if skip_header:
                next(csv_data)
            for data in csv_data:
                data = self.import_data(data, import_type)
                if data:
                    result_data.append(data)

        return result_data


class OptionVueImport(BaseCSVImport):

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
            "p_c": 26,
            "strike": 34,
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

    def _data_cleansing(self, data):
        if float(data[self.stock_mapping["market_price"]]) <= 0:
            return []

        # Add century to date format yyyyMMdd
        if data[self.stock_mapping["date"]]:
            data[self.stock_mapping["date"]] = "20" + data[self.stock_mapping["date"]]
        if data[self.options_mapping["exp_date"]]:
            data[self.options_mapping["exp_date"]] = "20" + data[self.options_mapping["exp_date"]]

        return data

    def import_csv(self, filename, skip_header=False, delimiter=",", import_type="OV"):
        stock_data = []
        option_data = []
        future_data = []
        with open(filename, "r") as inp_file:
            csv_data = csv.reader(inp_file, delimiter=delimiter)
            if skip_header:
                next(csv_data)
            for data in csv_data:
                data = self._enhance_data(data)
                if data:
                    if data[self.type_field] == "S":
                        data = self._type_conversion(self._map_data(data, "S"), "S")
                        stock_data.append(data)
                    elif data[self.type_field] == "F":
                        data = self._type_conversion(self._map_data(data, "F"), "F")
                        future_data.append(data)
                    elif data[self.type_field] in ["O", "G"]:
                        data = self._type_conversion(self._map_data(data, "O"), "O")
                        option_data.append(data)

        return stock_data, future_data, option_data
