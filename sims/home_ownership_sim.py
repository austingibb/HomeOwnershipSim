from money_rate import MoneyRate, Rate
from sims.mortgage_loan_sim import MortgageLoanSim

from amortization.amount import calculate_amortization_amount

class HomeOwnershipSim:
    def __init__(self, down:float, principal:float,
            mortgage_rate: MoneyRate, insurance: MoneyRate, property_tax: MoneyRate, maintenance: MoneyRate,
            hoa:MoneyRate, pmi:MoneyRate, housing_market_return:MoneyRate, sale_loss:float, cosigners:int=0,
            only_pay_minimum:bool=True):
        self._mortgage_rate_m = mortgage_rate.to_monthly(simple=True)
        self._mortgage_rate_a = mortgage_rate.to_annual(simple=True)
        self._insurance_m = insurance.to_monthly(simple=True)
        self._insurance_a = insurance.to_annual(simple=True)
        self._property_tax_m = property_tax.to_monthly()
        self._property_tax_a = property_tax.to_annual()
        self._maintenance_m = maintenance.to_monthly(simple=True)
        self._maintenance_a = maintenance.to_annual(simple=True)
        self._hoa_m = hoa.to_monthly(simple=True)
        self._hoa_a = hoa.to_annual(simple=True)
        self._housing_market_return_m = housing_market_return.to_monthly()
        self._housing_market_return_a = housing_market_return.to_annual()
        self._pmi_m = pmi.to_monthly(simple=True)
        self._pmi_a = pmi.to_annual(simple=True)
        self._pmi_total = 0
        self._sale_loss = sale_loss
        self._loan_sim = MortgageLoanSim(principal - (down*(1+cosigners)), self._mortgage_rate_m)
        self._home_value = principal
        self._min_monthly_payment = calculate_amortization_amount(self._loan_sim.principal_owed(), 
            self._mortgage_rate_a.amount, 30*12)
        self._monthly_burden = None
        self._cosigners = cosigners
        self._only_pay_minimum = only_pay_minimum

    def iterate_month(self, input_money):
        input_money = (1+self._cosigners)*input_money
        monthly_property_tax = self._property_tax_m.amount * self._home_value
        home_expenses = self._insurance_m.amount + monthly_property_tax + self._maintenance_m.amount + self._hoa_m.amount
        if self.is_pmi_active():
            home_expenses += self._pmi_m.amount
            self._pmi_total += self._pmi_m.amount

        self._monthly_burden = home_expenses + (self._min_monthly_payment if not self.is_paid_off() else 0)
        input_money -= home_expenses

        if not self._only_pay_minimum:
            ret_amt = self._loan_sim.iterate_month(input_money)
            ret_amt = ret_amt/(1+self._cosigners)
        else:
            input_money -= self._min_monthly_payment
            leftover = self._loan_sim.iterate_month(self._min_monthly_payment)
            ret_amt = input_money/(1+self._cosigners)
            
        self._home_value = self._housing_market_return_m.into(self._home_value)

        return ret_amt

    def is_pmi_active(self):
        equity = self._home_value - self._loan_sim.principal_owed()
        return equity/self._home_value < 0.2

    def pmi_paid(self):
        return self._pmi_total

    def net_worth_if_sold(self):
        return ((self._home_value * (1-self._sale_loss)) - self._loan_sim.principal_owed())/(1+self._cosigners)

    def net_worth(self):
        return (self._home_value - self._loan_sim.principal_owed())/(1+self._cosigners)

    def principal_owed(self):
        return self._loan_sim.principal_owed()/(1+self._cosigners)

    def home_value(self):
        return (self._home_value)/(1+self._cosigners)

    def interest_paid(self):
        return self._loan_sim.interest_paid()/(1+self._cosigners)

    def monthly_burden(self):
        return self._monthly_burden/(1+self._cosigners)

    def min_monthly_payment(self):
        return self._min_monthly_payment

    def is_paid_off(self):
        return self._loan_sim.principal_owed()//10 == 0