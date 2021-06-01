import backtrader as bt

class ChinaStockDutyCommissionScheme(bt.CommInfoBase):
    """
    本佣金模式下，买入股票仅支付佣金，卖出股票支付佣金和印花税
    """
    params = (
        ('stamp_duty',0.00025), # 印花税率
        ('commission',0.001), # 佣金率
        ('stocklike', True),
        ('commtype', bt.CommInfoBase.COMM_PERC),  # Apply % Commission
        #('percabs', False),  # pass perc as xx% which is the default
    )

    def _getcommission(self, size, price, pseudoexec):
        """
        If size is greater than 0, this indicates a long / buying of shares.
        If size is less than 0, this indicates a short / selling of shares.
        """
        comm_temp = max(5, abs(size) * self.p.commission * 100 * price)  #self.p.commission会在参数commission基础上除100，因此还原回来

        if size > 0: #买入，不考虑印花税
            return comm_temp
        elif size < 0: #卖出，考虑印花税
            stamp = abs(size) * self.p.stamp_duty * price
            return comm_temp + stamp