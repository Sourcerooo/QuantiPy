from abc import ABCMeta, abstractmethod

class AbstractExecutionHandler(object):
    """" Execution Handler will transform orders created by the portfolio and transform them into
         actual executable orders and will execute them via a given interface to either a real
         broker or a simulated environment.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def handle_event(self, event):
        """ Order events are processed and real orders will be created from the data supplied to the event.
            Once an actual order is filled a FillEvent will be triggered and put into the queue

            Parameters:
                event - Contains the event object with necessary data to create a transaction
        """
        raise NotImplementedError
