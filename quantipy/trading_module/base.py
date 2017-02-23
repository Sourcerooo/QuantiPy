from abc import ABCMeta, abstractmethod


class AbstractTradingModule(object):
    """" A module is an entity that encapsulates all other necessary module that are needed to trade. This can
         either be a realtime module used to trade specific strategies or a back tester to run a portfolio backtest"""

    __metaclass__ = ABCMeta

    def run(self):
        raise NotImplementedError
