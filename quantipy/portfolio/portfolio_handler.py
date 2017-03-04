import quantipy.portfolio.base as base_portfolio
import quantipy.event.event as q_event


class PortfolioHandler(base_portfolio.AbstractPortfolioHandler):

    def __init__(self, event_queue, portfolio, execution_handler, risk_manager=None):
        self.event_queue = event_queue
        self.portfolio = portfolio
        self.execution_handler = execution_handler
        self.risk_manager = risk_manager

    def get_statistics(self):
        self.portfolio.get_statistics()

    def handle_event(self, event):
        if event.type == q_event.MARKET_EVENT_STOCKS:
            self.portfolio.handle_event(event)
        elif event.type == q_event.MARKET_EVENT_OPTIONS:
            return
        elif event.type == q_event.MARKET_EVENT_FUTURES:
            return
        elif event.type == q_event.TRADE_EVENT:
            self._create_order(event)
        elif event.type == q_event.ORDER_EVENT:
            self.execution_handler.handle_event(event)
        elif event.type == q_event.FILL_EVENT:
            self.portfolio.handle_event(event)

    def _create_order(self, event):
        order = event.data
        order = self.portfolio.size_order(order)
        if self.risk_manager is not None:
            order = self.risk_manager.check_position(order)
        if not order:
            return
        order_event = q_event.OrderEvent(order)
        self.event_queue.put(order_event)
