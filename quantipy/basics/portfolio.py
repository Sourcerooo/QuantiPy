from abc import ABCMeta, abstractmethod
from quantipy.basics.event import FillEvent, OrderEvent

class Portfolio(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def update_trade_event(self, event):
        raise NotImplementedError

    def update_fill_event(self, event):
        raise NotImplementedError


class SimplePortfolio(Portfolio):
    def __init__(self, data_handler, event_queue, portfolio_params=[]):
        self.data_handler = data_handler
        self.event_queue = event_queue
        self.portfolio_params = portfolio_params

        self.all_positions = self.construct_all_positions()
        self.current_positions =