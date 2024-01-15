from enum import Enum

class Rate(Enum):
    DAILY = 1
    MONTHLY = 2
    WEEKLY = 3
    ANNUAL = 4

class MoneyRate:
    def __init__(self, amount: float, rate: Rate):
        self.amount = amount
        self.rate = rate

    def _to_monthly_simple(self):
        if self.rate == Rate.ANNUAL:
            return MoneyRate(self.amount/12, Rate.MONTHLY)
        elif self.rate == Rate.DAILY:
            return MoneyRate(self.amount*30.5, Rate.MONTHLY)
        elif self.rate == Rate.WEEKLY:
            return MoneyRate(self.amount*4.345, Rate.MONTHLY)
        else:
            return self

    def to_monthly(self, simple=False):
        if simple:
            return self._to_monthly_simple()

        if self.rate == Rate.ANNUAL:
            return MoneyRate((1+self.amount)**(1/12) -1, Rate.MONTHLY)
        elif self.rate == Rate.DAILY:
            return MoneyRate((1+self.amount)**(30.5)-1, Rate.MONTHLY)
        elif self.rate == Rate.WEEKLY:
            return MoneyRate((1+self.amount)**(4.345)-1, Rate.MONTHLY)
        else:
            return self

    def _to_annual_simple(self):
        if self.rate == Rate.MONTHLY:
            return MoneyRate(self.amount*12, Rate.ANNUAL)
        elif self.rate == Rate.DAILY:
            return MoneyRate(self.amount*365, Rate.ANNUAL)
        elif self.rate == Rate.WEEKLY:
            return MoneyRate(self.amount*52, Rate.ANNUAL)
        else:
            return self

    def to_annual(self, simple=False):
        if simple:
            return self._to_annual_simple()

        if self.rate == Rate.MONTHLY:
            return MoneyRate((1+self.amount)**(12) -1, Rate.ANNUAL)
        elif self.rate == Rate.DAILY:
            return MoneyRate((1+self.amount)**(365)-1, Rate.ANNUAL)
        elif self.rate == Rate.WEEKLY:
            return MoneyRate((1+self.amount)**(52)-1, Rate.ANNUAL)
        else:
            return self

    def into(self, other_amount):
        return (self.amount + 1)*other_amount

    def __str__(self):
        return "({}, {})".format(self.amount, self.rate._name_)

    def __repr__(self):
        return self.__str__()