from money_rate import MoneyRate, Rate
from sims.investment_sim import InvestmentSim
from sims.mortgage_loan_sim import MortgageLoanSim
from sims.home_ownership_sim import HomeOwnershipSim
from sims.rent_sim import RentSim

def print_mort_sim(name, mort_sim:HomeOwnershipSim, inv_sim_with_home:InvestmentSim, rent_sim:RentSim=None):
        print("\t\t{} - home netw [${:,.2f}] stocks netw val [${:,.2f}] home val [${:,.2f}] monthly exp [${:,.2f}] monthly payment [${:,.2f}] "
              "owed [${:,.2f}] tot int [${:,.2f}] tot rent [${:,.2f}] pmi paid [${:,.2f}]"
              .format(name, mort_sim.net_worth(), inv_sim_with_home.net_worth(),
                      mort_sim.home_value(), mort_sim.monthly_burden(), mort_sim.min_monthly_payment(),
                      mort_sim.principal_owed(), mort_sim.interest_paid(), rent_sim.total_rent() if rent_sim is not None else 0,
                      mort_sim.pmi_paid()))

def main():
    savings = 90_000
    monthly_investment = 7_000
    monthly_mortgage_investment = 7_000

    house_market_return = MoneyRate(0.1, Rate.ANNUAL)
    # mortgage sims
    mort_sim_3br = HomeOwnershipSim(down=savings,
        principal=750_000,
        mortgage_rate=MoneyRate(0.065, Rate.ANNUAL),
        insurance=MoneyRate(1_000, Rate.ANNUAL),
        property_tax=MoneyRate(0.01, Rate.ANNUAL),
        maintenance=MoneyRate(10_000, Rate.ANNUAL),
        hoa=MoneyRate(200, Rate.MONTHLY),
        housing_market_return=house_market_return,
        pmi=MoneyRate(0.0046, Rate.ANNUAL),
        sale_loss=0.09,
        purchase_loss=0.04,
        cosigners=0,
        only_pay_minimum=False)
    mort_sim_2br = HomeOwnershipSim(down=savings,
        principal=650_000,
        mortgage_rate=MoneyRate(0.06, Rate.ANNUAL),
        insurance=MoneyRate(800, Rate.ANNUAL),
        property_tax=MoneyRate(0.01, Rate.ANNUAL),
        maintenance=MoneyRate(8_000, Rate.ANNUAL),
        hoa=MoneyRate(50, Rate.MONTHLY),
        housing_market_return=house_market_return,
        pmi=MoneyRate(0.0046, Rate.ANNUAL),
        sale_loss=0.09,
        purchase_loss=0.04,
        cosigners=0,
        only_pay_minimum=False)
    condo_mort_sim = HomeOwnershipSim(down=savings,
        principal=500_000,
        mortgage_rate=MoneyRate(0.065, Rate.ANNUAL),
        insurance=MoneyRate(700, Rate.ANNUAL),
        property_tax=MoneyRate(0.01, Rate.ANNUAL),
        maintenance=MoneyRate(5_000, Rate.ANNUAL),
        hoa=MoneyRate(1000, Rate.MONTHLY),
        housing_market_return=house_market_return,
        pmi=MoneyRate(0.0046, Rate.ANNUAL),
        sale_loss=0.09,
        purchase_loss=0.04,
        cosigners=0,
        only_pay_minimum=True)

    market_return = MoneyRate(0.09, Rate.ANNUAL)
    # investment sims for in combo with mortgage
    inv_sim_3br = InvestmentSim(0,
        stock_market_return=market_return,
        sale_loss=0.09)
    inv_sim_2br = InvestmentSim(0,
        stock_market_return=market_return,
        sale_loss=0.09)
    inv_sim_with_condo = InvestmentSim(0,
        stock_market_return=market_return,
        sale_loss=0.09)
    
    # rent-based investment sim
    inv_sim_rent = InvestmentSim(savings, 
        stock_market_return=market_return,
        sale_loss = 0.09)

    # rent sim for my rent while investing in stock market
    rent_sim_self = RentSim(1300, MoneyRate(0.02, Rate.ANNUAL))
    # rent sim for a tenant in a house
    rent_sim_tenant_3br = RentSim(2400, MoneyRate(0.02, Rate.ANNUAL))
    # rent sim for 2br
    rent_sim_tenant_2br = RentSim(1200, MoneyRate(0.02, Rate.ANNUAL))

    savings = 0
    month_counter = 0
    while(month_counter < (12*5)):
        # mortgage simulation
        amount_left_3br = mort_sim_3br.iterate_month(monthly_mortgage_investment)
        amount_left_2br = mort_sim_2br.iterate_month(monthly_mortgage_investment)
        amount_left_condo = condo_mort_sim.iterate_month(monthly_mortgage_investment)
        amount_left_3br += rent_sim_tenant_3br.current_rent()
        amount_left_2br += rent_sim_tenant_2br.current_rent()

        inv_sim_3br.iterate_month((amount_left_3br if amount_left_3br > 0 else 0) + (monthly_investment-monthly_mortgage_investment))
        inv_sim_2br.iterate_month((amount_left_2br if amount_left_2br > 0 else 0) + (monthly_investment-monthly_mortgage_investment))
        inv_sim_with_condo.iterate_month((amount_left_condo if amount_left_condo > 0 else 0) + (monthly_investment-monthly_mortgage_investment))
        inv_sim_rent.iterate_month(monthly_investment-rent_sim_self.current_rent())

        # rent simulation
        rent_sim_self.iterate_month()
        rent_sim_tenant_2br.iterate_month()
        rent_sim_tenant_3br.iterate_month()

        # progress printing
        if month_counter%12 == 0:
            print("Year {}".format(month_counter//12+1))
        print("\tMonth {}".format(month_counter%12+1))
        print_mort_sim("3br Home", mort_sim_3br, inv_sim_3br, rent_sim_tenant_3br)
        print_mort_sim("2br Home", mort_sim_2br, inv_sim_2br, rent_sim_tenant_2br)
        print_mort_sim("Condo Home", condo_mort_sim, inv_sim_with_condo)
        
        print("\t\trent - netw [${:,.2f}] gains [${:,.2f}]".format(inv_sim_rent.net_worth(), inv_sim_rent.gains()))

        month_counter += 1
    print("Final 3br home: [${:,.2f}] Final 2br home: [${:,.2f}] Final condo: [${:,.2f}] Final rent: [${:,.2f}]"
          .format(mort_sim_3br.net_worth_if_sold() + inv_sim_3br.net_worth_if_sold(),
                  mort_sim_2br.net_worth_if_sold() + inv_sim_2br.net_worth_if_sold(),
                  condo_mort_sim.net_worth_if_sold() + inv_sim_with_condo.net_worth_if_sold(),
                  inv_sim_rent.net_worth_if_sold()))

if __name__ == "__main__":
    main()
