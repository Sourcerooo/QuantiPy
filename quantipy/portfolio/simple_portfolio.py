import quantipy.portfolio.base as base


class SimplePortfolio(base.AbstractPortfolio):
    def __init__(self, event_queue, data_handler, portfolio_params=[]):
        self.data_handler = data_handler
        self.event_queue = event_queue
        self.portfolio_params = portfolio_params

    #   self.all_positions = self.construct_all_positions()

    #    self.current_positions =