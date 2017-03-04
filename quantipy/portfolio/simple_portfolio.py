import quantipy.portfolio.base as base
import quantipy.event.event as q_event
import quantipy.statistics.SimpleStatistic as SimpleStatistic
import pandas as pd


class SimplePortfolio(base.AbstractPortfolio):
    def __init__(self, event_queue, data_handler, systems, portfolio_params=[]):
        self.data_handler = data_handler
        self.event_queue = event_queue
        self.portfolio_params = portfolio_params
        self.positions = pd.DataFrame(columns=["system_id", "trade_id", "seq_no", "symbol", "calc_price",
                                               "max_risk", "current_price", "filled_price", "gain_loss"])
        self.systems = systems
        self.statistic = SimpleStatistic.SimpleStatistic()

    def get_statistics(self):
        self.statistic.output("xx")

    def handle_event(self, event):
        if event.type == q_event.MARKET_EVENT_STOCKS:
            self._update_position(event.data)
            self._update_statistic()
            for system in self.systems:
                #system.update_statistic(event.data)
                system.calculate(event.data)
        elif event.type == q_event.MARKET_EVENT_OPTIONS:
            return
        elif event.type == q_event.MARKET_EVENT_FUTURES:
            return
        elif event.type == q_event.FILL_EVENT:
            self._fill_position(event.data)
            self._update_statistic()

    def size_order(self, order):
        order["calc_price"] = order["market_price"]
        position = {
            "system_id": order["system_id"],
            "trade_id": order["trade_id"],
            "seq_no": order["seq_no"],
            "symbol": order["symbol"],
            "calc_price": order["calc_price"],
            "max_risk": order["calc_price"] * order["amount"],
            "current_price": order["calc_price"],
            "filled_price": 0,
            "gain_loss": 0
        }
        self.positions = self.positions.append(position, ignore_index=True)
        self.positions.set_index(["symbol"])
        self.positions.sort_index(inplace=True)
        return order

    def _fill_position(self, data):
        #self.positions.set_value((self.positions["trade_id"] == data["trade_id"]), "filled_price", data["filled_price"])
        self.positions.set_index(["symbol"])
        self.positions.sort_index(inplace=True)
        print(self.positions)
        df =self.positions.at[data["symbol"]]
        df.ix[df["trade_id"] == data["trade_id"], "filled_price"] = data["filled_price"]
        self._update_position(data)

    def _update_position(self, data):
        self.positions.at[data["symbol"], "current_price"] = data["market_price"]
        print("------------")
        print(self.positions.at[data["symbol"], "current_price"])
        print(self.positions.at[data["symbol"], "filled_price"])
        self.positions.at[data["symbol"], "gain_loss"] = self.positions.at[data["symbol"], "current_price"] - self.positions.at[data["symbol"], "filled_price"]
        # self.positions.loc[data["symbol"], "gain_loss"] = self.positions.loc[data["symbol"],"current_price"] - \
        #                                                         self.positions.loc[data["symbol"],"filled_price"]

        # self.positions.ix[self.positions["symbol"] == data["symbol"], "current_price"] = data["market_price"]
        # self.positions.ix[self.positions["symbol"] == data["symbol"], "gain_loss"] = self.positions["current_price"] - \
        #                                                                              self.positions["filled_price"]

    def _update_statistic(self):
        total_gain_loss = self.positions["gain_loss"].sum()
        total_cost = self.positions["filled_price"].sum()

        self.statistic.calculate(total_cost, total_gain_loss)
