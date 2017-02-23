from abc import ABCMeta, abstractmethod

class AbstractPortfolio(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def update_trade_event(self, event):
        raise NotImplementedError

    @abstractmethod
    def update_fill_event(self, event):
        raise NotImplementedError


class AbstractPortfolioHandler(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def update_trade_event(self, event):
        raise NotImplementedError

    @abstractmethod
    def update_fill_event(self, event):
        raise NotImplementedError