import backtrader as bt
import sys
sys.path.append("..")
from indicator.KDJs import *


class KDJStrategy(bt.Strategy):
    params = (
        ('period', 9),
        ('period_dfast', 3),
        ('period_dslow', 3),
    )

    def __init__(self):

        # use self defind a KDJ indicator
        self.kd = KDJ(
            self.data0,
            period=self.p.period,
            period_dfast=self.p.period_dfast,
            period_dslow=self.p.period_dslow,
        )

        self.crossover = bt.indicators.CrossOver(self.kd.K, self.kd.D, plot=False)
        # self.above = bt.And(self.macd.macd>0.0, self.macd.macdsignal>0.0)

        self.buy_signal = (self.crossover == 1)
        self.sell_signal = (self.crossover == -1)
        # To keep track of pending orders
        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        if order.status in [order.Completed, order.Canceled, order.Margin, order.Rejected]:
            # Write down: no pending order
            self.order = None

    def next(self):
        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            # Not yet ... we MIGHT BUY if ...
            if self.buy_signal[0]:
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy(size=1000)
        else:
            # Already in the market ... we might sell
            if self.sell_signal[0]:
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell(size=1000)