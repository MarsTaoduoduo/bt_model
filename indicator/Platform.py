import backtrader as bt

class Platform(bt.Indicator):
    lines = ("up","down")

    def __init__(self):
        self.addminperiod(6)   #5天的平台

    def next(self):
        self.up[0]= max(self.data.high.get(ago = -1,size =5))
        self.down[0] = min(self.data.low.get(ago=-1, size=5))