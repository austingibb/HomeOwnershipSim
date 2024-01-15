from money_rate import MoneyRate, Rate

class RentSim:
    def __init__(self, initial_rent:float, rent_increase:MoneyRate):
        self._current_rent = initial_rent
        self._rent_increase = rent_increase.to_monthly()

    def iterate_month(self):
        self._current_rent = self._rent_increase.into(self._current_rent)

    def current_rent(self):
        return self._current_rent