import quantipy.trading_module.base as base_system
import queue

class BacktestModule(base_system.AbstractTradingModule):
    """ Shell class to initialize and manage all classes that contain a backtesting system """
    def __init__(self, events_queue, data_handler, systems, execution_handler, portfolio_handler):
        self.events_queue = events_queue
        self.data_handler = data_handler
        self.systems = systems
        self.portfolio_handler = portfolio_handler
        self.data_handler = data_handler
        self.execution_handler = execution_handler

    def load_config(self, filename):
        """ Todo: Method should load a configuration file and create all necessary classes based on the information
            provided in the config file.

            Design decision: Specify file structer and format (JSON, CSV or TXT?)"""
        pass

    def run(self):
        print("Backtest is running...")
        while self.data_handler.continue_update:
            try:
                event = self.events_queue.get(False)
            except queue.Empty:
                self.data_handler.update_data()
            else:
                self.portfolio_handler.update_event(event)

    def get_results(self):
        """ Will return the results of the backtest """
        pass



