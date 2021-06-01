import backtrader as bt
import sys
sys.path.append("..")
from indicator.Platform import *

class AceStrategy_SMA(bt.Strategy):
    params = (
        ('maperiod_3', 3),
        ('maperiod_5',5)
    )

    def __init__(self):
        #print(f'init___{self.datas[0].datetime.date(0)}')
        self.dataclose = self.datas[0].close
        self.sma_3 = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod_3)
        self.sma_5 = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod_5)
        self.order = None
        # self.sma_3.plotinfo.plot = False
        # self.sma_5.plotinfo.plot = False

    def start(self):
        pass

    def prenext(self):
        pass

    def nextstart(self):
        pass

    # def notify_order(self, order):
    #     if order.status in [order.Submitted, order.Accepted]:
    #         return
    #     if order.status in [order.Completed]:
    #         pass
    #         self.bar_executed = len(self)
    #     elif order.status in [order.Canceled, order.Margin, order.Rejected]:
    #         pass
    #     self.order = None # 无挂起

    def next(self):
        # if self.order:
        #     return
        if not self.position:
            if self.sma_3[0]>self.sma_5[0]:
                self.order = self.buy(size=1000)
                #print(f"{self.datas[0].datetime.date(0)},买入！价格为{self.dataclose[0]}")
        else:
            if self.sma_3[0]<self.sma_5[0]:
                self.order = self.sell(size=1000)
                #print(f"{self.datas[0].datetime.date(0)},卖出！价格为{self.dataclose[0]}")

    def stop(self):
        pass


class AceStrategy_Platform(bt.Strategy):

    def notify_order(self, order):


        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                print(f"{self.datas[0].datetime.datetime()},买入价格：{order.executed.price}，买入总额：{order.executed.value}，买入佣金:{order.executed.comm}")
                self.buyexecuted = order.executed.price
                self.commexecuted = order.executed.comm

            elif order.issell():
                print(f"{self.datas[0].datetime.datetime()},卖出价格：{order.executed.price}，卖出总额：{order.executed.value}，卖出佣金:{order.executed.comm}")
            self.bar_executed = len(self)

        # elif order.status in [order.Canceled, order.Margin, order.Rejected]
        elif order.status in [order.Canceled]:
            print("订单取消\n")

        elif order.status in [order.Margin]:
            print("订单超时\n")

        elif order.status in [order.Rejected]:
            print("订单拒绝\n")

        self.order = None

    def notify_trade(self, trade):
        if trade.isclosed:
            print(f"{self.datas[0].datetime.datetime()},毛收益：{round(trade.pnl, 2)}，本次交易买卖佣金总额：{round(trade.commission, 2)}，净收益：{round(trade.pnlcomm,2)}\n")


    def __init__(self):
        self.platform = Platform(self.data)
        self.buy_signal = bt.indicators.CrossOver(self.datas[0].close,self.platform.up)
        self.sell_signal = bt.indicators.CrossDown(self.data.close, self.platform.down)
        # self.order = None
        self.buy_signal.plotinfo.plot = False
        self.sell_signal.plotinfo.plot = False
        self.platform.plotinfo.plotmaster = self.data  #类似通达信的 是否在主图显示
        # self.卖出信号.plotinfo.plot = False

    def start(self):
        pass

    def prenext(self):
        pass

    def nextstart(self):
        pass

    def next(self):
        # if self.order:
        #     return
        if not self.position:
            if self.buy_signal[0] == 1:
                self.order = self.buy(size=1000)
                print(f"{self.datas[0].datetime.datetime()},决定买入！当时价格为：{self.data.close[0]}")
        else:
            if self.sell_signal[0] == 1:
                self.order = self.sell(size=1000)
                print(f"{self.datas[0].datetime.datetime()},决定卖出！当时价格为：{self.data.close[0]}")
        pass

    # def stop(self):
    #     if  self.position:
    #         self.order = self.sell(size=1000)
    #         print(f"{self.datas[0].datetime.date(0)},卖出！价格为{self.data.close[0]}")