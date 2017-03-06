import quantipy.portfolio.base as base
import quantipy.event.event as q_event
import quantipy.statistics.SimpleStatistic as SimpleStatistic
import pandas as pd


class SimplePortfolio(base.AbstractPortfolio):
    def __init__(self, event_queue, data_handler, systems, portfolio_params=[]):
        self.data_handler = data_handler
        self.event_queue = event_queue
        self.portfolio_params = portfolio_params
        self.positions = pd.DataFrame(columns=["symbol", "trade_id", "seq_no", "status", "system_id", "calc_price",
                                               "volume", "max_risk", "current_price", "filled_price", "gain_loss"])
        self.positions.set_index(["symbol", "trade_id", "seq_no"],inplace=True)
        self.open_positions = self.positions
        self.closed_positions = self.positions
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
        # Todo: Create position file with constant for position status
        position = {
            "status": "CREA",
            "system_id": order["system_id"],
            "calc_price": order["calc_price"],
            "volume": order["amount"],
            "max_risk": order["calc_price"] * order["amount"],
            "current_price": order["calc_price"],
            "filled_price": 0,
            "gain_loss": 0
        }
        self.positions.loc[order["symbol"], str(order["trade_id"]), order["seq_no"]] = position
        self.positions.sort_index(inplace=True)
        return order

    def _fill_position(self, data):
        self.positions.loc[(data["symbol"], str(data["trade_id"]), data["seq_no"]), "filled_price"] = data["filled_price"]
        self.positions.loc[(data["symbol"], str(data["trade_id"]), data["seq_no"]), "status"] = "OPEN"
        #self._update_position(data)

    def _update_position(self, data):
        if not self.open_positions.empty:
            for key, row in self.positions.ix[self.open_positions.index.values].iterrows():
                if (key[0] == "BA"):
                    df.at[key, "xpz"] = row["y"] + row["z"]
            self.positions.at[data["symbol"], "current_price"] = data["market_price"]
            self.positions.at[data["symbol"], "gain_loss"] = self.positions.ix[[data["symbol"]], "current_price"] - \
                                                             self.positions.ix[[data["symbol"]], "filled_price"]

    def _update_statistic(self):
        if not self.positions.empty:
            total_gain_loss = self.positions["gain_loss"].sum()
            total_cost = self.positions["filled_price"].sum()
            self.statistic.calculate(total_cost, total_gain_loss)
