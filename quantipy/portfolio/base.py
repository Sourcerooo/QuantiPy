from abc import ABCMeta, abstractmethod


class AbstractPortfolio(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def handle_event(self, event):
        raise NotImplementedError

    @abstractmethod
    def size_order(self,order):
        raise NotImplementedError

class AbstractPortfolioHandler(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def handle_event(self, event):
        raise NotImplementedError

