import quantipy.trading_module.backtest as backtest
import quantipy.system.stock_system.simple_system as simple_system
import quantipy.execution_handler.simulated_execution as sim_exec
import quantipy.data_management.data_handler as data_handler
import quantipy.portfolio.simple_portfolio as simple_portfolio
import quantipy.portfolio.portfolio_handler as pf_handler
import queue
import timeit

symbols = ["BA"]
event_queue = queue.Queue()
yahoo_handler = data_handler.YahooHistoricalHandler(event_queue, symbols, "2016-01-01", "2016-01-05")
exec_handler = sim_exec.SimulatedExecutionHandler(event_queue)
simple_algo = simple_system.BuyAndHoldSystem(event_queue, symbols, yahoo_handler)
portfolio = simple_portfolio.SimplePortfolio(event_queue, yahoo_handler, [simple_algo])
portfolio_handler = pf_handler.PortfolioHandler(event_queue, portfolio, exec_handler)

backtester = backtest.BacktestModule(event_queue, yahoo_handler, portfolio_handler)
start = timeit.default_timer()
backtester.run()
stop = timeit.default_timer()
print("----------------------------")
print("Backtest took {} seconds".format(stop-start))

