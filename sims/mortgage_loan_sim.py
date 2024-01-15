from money_rate import MoneyRate, Rate

class MortgageLoanSim:
    def __init__(self, principal:float, mortgage_rate: MoneyRate):
        self._principal_original = principal
        self._principal_owed = principal
        self._mortgage_rate_m = mortgage_rate.to_monthly(simple=True)
        self._interest_paid = 0

    def iterate_month(self, input_money):
        interest = self._mortgage_rate_m.amount * self._principal_owed
        self._interest_paid += interest
        input_money -= interest
        self._principal_owed -= input_money
        if self._principal_owed < 0:
            ret_amt = -self._principal_owed
            self._principal_owed = 0
            return ret_amt
        else:
            return 0

    def principal_owed(self):
        return self._principal_owed

    def interest_paid(self):
        return self._interest_paid