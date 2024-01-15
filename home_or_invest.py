from money_rate import MoneyRate, Rate
from sims.investment_sim import InvestmentSim
from sims.mortgage_loan_sim import MortgageLoanSim
from sims.home_ownership_sim import HomeOwnershipSim
from sims.rent_sim import RentSim

def print_mort_sim(name, mort_sim:HomeOwnershipSim, inv_sim_with_home:InvestmentSim):
        print("\t{} - home netw [${:,.2f}] stocks netw val [${:,.2f}] home val [${:,.2f}] monthly exp [${:,.2f}] monthly payment [${:,.2f}] "
              "owed [${:,.2f}] tot int [${:,.2f}] pmi paid [${:,.2f}]"
              .format(name, mort_sim.net_worth(), inv_sim_with_home.net_worth(),
                      mort_sim.home_value(), mort_sim.monthly_burden(), mort_sim.min_monthly_payment(),
                      mort_sim.principal_owed(), mort_sim.interest_paid(),
                      mort_sim.pmi_paid()))

def main():
    savings = 75_000
    monthly_investment = 6_000
    monthly_mortgage_investment = 6_000

    house_market_return = MoneyRate(0.1, Rate.ANNUAL)
    # mortgage sims
    split_mort_sim = HomeOwnershipSim(down=savings,
        principal=780_000,
        mortgage_rate=MoneyRate(0.075, Rate.ANNUAL),
        insurance=MoneyRate(1500, Rate.ANNUAL),
        property_tax=MoneyRate(0.01, Rate.ANNUAL),
        maintenance=MoneyRate(4000, Rate.ANNUAL),
        hoa=MoneyRate(200, Rate.MONTHLY),
        housing_market_return=house_market_return,
        pmi=MoneyRate(683, Rate.MONTHLY),
        sale_loss=0.09,
        cosigners=1,
        only_pay_minimum=True)
    condo_mort_sim = HomeOwnershipSim(down=savings,
        principal=400_000,
        mortgage_rate=MoneyRate(0.075, Rate.ANNUAL),
        insurance=MoneyRate(1000, Rate.ANNUAL),
        property_tax=MoneyRate(0.01, Rate.ANNUAL),
        maintenance=MoneyRate(2000, Rate.ANNUAL),
        hoa=MoneyRate(400, Rate.MONTHLY),
        housing_market_return=house_market_return,
        pmi=MoneyRate(400, Rate.MONTHLY),
        sale_loss=0.09,
        only_pay_minimum=True)

    market_return = MoneyRate(0.09, Rate.ANNUAL)
    # investment sims for in combo with mortgage
    inv_sim_with_split = InvestmentSim(0,
        stock_market_return=market_return,
        sale_loss=0.09)
    inv_sim_with_condo = InvestmentSim(0,
        stock_market_return=market_return,
        sale_loss=0.09)
    
    # rent-based investment sim
    inv_sim = InvestmentSim(savings, 
        stock_market_return=market_return,
        sale_loss = 0.09)

    # rent sim for my rent while ivesting in stock market
    rent_sim_self = RentSim(1700, MoneyRate(0.01, Rate.ANNUAL))

    # rent sim for a tenant in a house
    rent_sim_tenant = RentSim(0, MoneyRate(0.01, Rate.ANNUAL))


    savings = 0
    month_counter = 0
    tenant_rent = 0
    while(month_counter < (12*5)):
        # mortgage simulation
        amount_left_split = split_mort_sim.iterate_month(monthly_mortgage_investment)
        amount_left_condo = condo_mort_sim.iterate_month(monthly_mortgage_investment)

        inv_sim_with_split.iterate_month((amount_left_split if amount_left_split > 0 else 0) + (monthly_investment-monthly_mortgage_investment))
        inv_sim_with_condo.iterate_month((amount_left_condo if amount_left_condo > 0 else 0) + (monthly_investment-monthly_mortgage_investment))

        # rent simulation
        rent_sim_self.iterate_month()
        rent_sim_tenant.iterate_month()
        tenant_rent += rent_sim_tenant.current_rent()
        inv_sim.iterate_month(monthly_investment-rent_sim_self.current_rent())

        # progress printing
        if month_counter%12 == 0:
            print("Year {}".format(month_counter//12+1))
        print("\tMonth {}".format(month_counter%12+1))
        print_mort_sim("Split Home", split_mort_sim, inv_sim_with_split)
        print_mort_sim("Condo Home", condo_mort_sim, inv_sim_with_condo)
        
        print("\t\trent - netw [${:,.2f}] gains [${:,.2f}]".format(inv_sim.net_worth(), inv_sim.gains()))

        month_counter += 1
    print("Final home: [${:,.2f}] Final condo: [${:,.2f}] Final rent: [${:,.2f}]"
          .format(split_mort_sim.net_worth_if_sold() + inv_sim_with_split.net_worth_if_sold() + tenant_rent,
                  condo_mort_sim.net_worth_if_sold() + inv_sim_with_condo.net_worth_if_sold() + tenant_rent,
                  inv_sim.net_worth_if_sold()))

if __name__ == "__main__":
    main()
