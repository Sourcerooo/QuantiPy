import datetime

import quantipy.execution_handler.base as base
from quantipy.event.event import FillEvent


class SimulatedExecutionHandler(base.AbstractExecutionHandler):
    """ Execution is simulated, no real broker or logic is attached. The order are just passed through as
        they are generated. Every order will result in a successful FillEvent at the desired price.

        Todo: Design-Decision-> Either implement slippage here or in portfolio class. There is a difference between:
            a) Unconcious slippage: caused by bad fills when executing market orders, these should be implemented here
            b) Concious slippage: If executing limit orders and diverging the price from midprice to get a fill.
        In general, these two forms of slippage exclude each other
    """

    def __init__(self, event_queue):
        self.event_queue = event_queue

    def execute_order(self, event):
        fill_data = event.data
        fill_data["filled_at"] = datetime.datetime.now()
        fill_event = FillEvent(fill_data)
        self.event_queue.put(fill_event)

