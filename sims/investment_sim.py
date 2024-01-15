from money_rate import MoneyRate, Rate

class InvestmentSim:
    def __init__(self, savings:float, stock_market_return:MoneyRate, sale_loss:float):
        self._stock_market_return = stock_market_return.to_monthly()
        self._stock_value = savings
        self._contributions = savings
        self._sale_loss = sale_loss

    def iterate_month(self, input_money):
        self._contributions += input_money   
        self._stock_value = self._stock_market_return.into(input_money + self._stock_value)

    def gains(self):
        return self._stock_value - self._contributions

    def net_worth(self):
        return self._stock_value

    def net_worth_if_sold(self):
        stock_taxes = (1-self._sale_loss)*self.gains()
        print("stock taxes:", stock_taxes, "stock value:", self._stock_value)
        return self._stock_value - stock_taxes
