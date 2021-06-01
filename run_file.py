import backtrader as bt
import os,sys
import datetime

from data.tushare_data import *
from strategy.AceStrategy import *
from strategy.KDJStrategy import *
from commission.ChinaStockDuty import *



ts_code = '600036.SH'
start_date = '20000101'
end_date = '20210308'
raw_data = get_data(ts_code, start_date, end_date)



cerebro = bt.Cerebro(stdstats=False)
cerebro.broker.setcash(100000.00)  # 设置初始资金金额

data = bt.feeds.PandasData(dataname=raw_data,
                           fromdate=datetime.datetime(2010, 1, 1),
                           todate=datetime.datetime(2021, 3, 8),
                           #datetime='trade_date'
                          )


cerebro.adddata(data)
cerebro.addstrategy(KDJStrategy)

cerebro.addobserver(bt.observers.Broker)
cerebro.addobserver(bt.observers.Trades)
cerebro.addobserver(bt.observers.BuySell)
cerebro.addobserver(bt.observers.DrawDown)
cerebro.addobserver(bt.observers.Value)
cerebro.addobserver(bt.observers.TimeReturn)

cerebro.addanalyzer(bt.analyzers.PyFolio)

start_value = cerebro.broker.getvalue()
print(f'初始资金:{start_value}')

chinastockcomm = ChinaStockDutyCommissionScheme(stamp_duty=0.00025,commission=0.001)
cerebro.broker.addcommissioninfo(chinastockcomm)

results = cerebro.run()

end_value =  cerebro.broker.getvalue()
print(f'期末资金:{end_value}')

cerebro.plot(style = "candle")



strat = results[0]
pyfoliozer = strat.analyzers.getbyname('pyfolio')
returns, positions, transactions, grosslev = pyfoliozer.get_pf_items()

returns_path = os.path.join(os.path.join(os.getcwd(), "results"), ts_code + "_returns.csv")
returns.to_csv(returns_path)

positions_path = os.path.join(os.path.join(os.getcwd(), "results"), ts_code + "_positions.csv")
positions.to_csv(positions_path)

transactions_path = os.path.join(os.path.join(os.getcwd(), "results"), ts_code + "_transactions.csv")
transactions.to_csv(transactions_path)

grosslev_path = os.path.join(os.path.join(os.getcwd(), "results"), ts_code + "_grosslev.csv")
grosslev.to_csv(grosslev_path)
