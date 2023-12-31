import datetime
from dateutil.relativedelta import relativedelta

class MaxPaymentException(Exception):
    """
    Exception raised for errors in the max monthly payment input.
    """
    pass
    
def amortization_schedule(loan_value, interest, term, down_payment=0, start_date=None, property_taxes=0, home_insurance=0, hoa_fees=0, pmi=0):
    """Calculates the amortization schedule for a loan.

    Args:
        loan_value (float): The total loan amount.
        interest (float): The annual interest rate (as a percentage).
        term (int): The loan term in years.
        down_payment (float, optional): The down payment amount. Defaults to 0.
        start_date (datetime, optional): The start date of the loan. Defaults to today.
        property_taxes (float, optional): The annual property tax amount. Defaults to 0.
        home_insurance (float, optional): The annual home insurance amount. Defaults to 0.
        hoa_fees (float, optional): The monthly HOA fees. Defaults to 0.
        pmi (float, optional): The monthly PMI amount. Defaults to 0.

    Returns:
        list: A list of dictionaries containing the amortization schedule, with each dictionary representing a monthly payment.
    """
    
    # Initialize cumulative sum variables
    total_payments_sum = 0
    interest_sum = 0
    principal_sum = 0
    property_taxes_sum = 0
    home_insurance_sum = 0
    hoa_fees_sum = 0
    pmi_sum = 0

    if start_date is None:
        start_date = datetime.datetime.today()
    
    # Monthly interest rate
    monthly_interest_rate = interest / 12 / 100
    
    # Total number of payments
    n_payments = term * 12
    
    # Loan amount after down payment
    loan_amount = loan_value - down_payment
    
    # Monthly payment calculation
    monthly_payment = loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate)**n_payments) / (((1 + monthly_interest_rate)**n_payments) - 1)
    
    # Monthly breakdown of additional costs
    monthly_property_taxes = property_taxes / 12
    monthly_home_insurance = home_insurance / 12
    monthly_hoa_fees = hoa_fees  # Assuming hoa_fees is already a monthly amount
    monthly_pmi = pmi  # Assuming pmi is already a monthly amount
    
    # Total monthly payment including optional costs
    total_monthly_payment = monthly_payment + monthly_property_taxes + monthly_home_insurance + monthly_hoa_fees + monthly_pmi
    
    amortization_schedule = []
    
    for month in range(1, n_payments + 1):
        interest_payment = loan_amount * monthly_interest_rate
        principal_payment = monthly_payment - interest_payment
        loan_amount -= principal_payment
        
        payment_date = start_date + relativedelta(months=month - 1)
        
        # Update cumulative sum variables
        total_payments_sum += total_monthly_payment
        interest_sum += interest_payment
        principal_sum += principal_payment
        property_taxes_sum += monthly_property_taxes
        home_insurance_sum += monthly_home_insurance
        hoa_fees_sum += monthly_hoa_fees
        pmi_sum += monthly_pmi

        amortization_schedule.append({
            'Month': payment_date.strftime('%Y-%m'),
            'Monthly Payment': round(monthly_payment, 2),
            'Principal': round(principal_payment, 2),
            'Interest': round(interest_payment, 2),
            'Remaining Balance': round(loan_amount, 2),
            'Total Monthly Payment': round(total_monthly_payment, 2),
            'Property Taxes': round(monthly_property_taxes, 2),
            'Home Insurance': round(monthly_home_insurance, 2),
            'HOA Fees': round(monthly_hoa_fees, 2),
            'PMI': round(monthly_pmi, 2),
            'Total Payments Sum': round(total_payments_sum, 2),
            'Interest Sum': round(interest_sum, 2),
            'Principal Sum': round(principal_sum, 2),
            'Property Taxes Sum': round(property_taxes_sum, 2),
            'Home Insurance Sum': round(home_insurance_sum, 2),
            'HOA Fees Sum': round(hoa_fees_sum, 2),
            'PMI Sum': round(pmi_sum, 2)
        })
    
    return amortization_schedule


def adjusted_amortization_schedule(loan_value, interest, term, max_monthly_payment=None, down_payment=0, start_date=None, property_taxes=0, home_insurance=0, hoa_fees=0, pmi=0):
    """Calculates an adjusted amortization schedule based on a max monthly payment.

    Args:
        loan_value (float): The total loan amount.
        interest (float): The annual interest rate (as a percentage).
        term (int): The loan term in years.
        max_monthly_payment (float, optional): The maximum monthly payment amount. If provided, it must be greater than the total monthly payment (PITI). Defaults to None.
        down_payment (float, optional): The down payment amount. Defaults to 0.
        start_date (datetime, optional): The start date of the loan. Defaults to today.
        property_taxes (float, optional): The annual property tax amount. Defaults to 0.
        home_insurance (float, optional): The annual home insurance amount. Defaults to 0.
        hoa_fees (float, optional): The monthly HOA fees. Defaults to 0.
        pmi (float, optional): The monthly PMI amount. Defaults to 0.

    Raises:
        MaxPaymentException: If max_monthly_payment is provided but is not greater than the total monthly payment (PITI).

    Returns:
        list: A list of dictionaries containing the adjusted amortization schedule, with each dictionary representing a monthly payment.
    """
    
    # Monthly breakdown of additional costs
    monthly_property_taxes = property_taxes / 12
    monthly_home_insurance = home_insurance / 12
    monthly_hoa_fees = hoa_fees  # Assuming hoa_fees is already a monthly amount
    monthly_pmi = pmi  # Assuming pmi is already a monthly amount

    # Initialize cumulative sum variables
    total_payments_sum = 0
    interest_sum = 0
    principal_sum = 0
    property_taxes_sum = 0
    home_insurance_sum = 0
    hoa_fees_sum = 0
    pmi_sum = 0

    if start_date is None:
        start_date = datetime.datetime.today()
    
    schedule = amortization_schedule(loan_value, interest, term, down_payment, start_date, property_taxes, home_insurance, hoa_fees, pmi)
    
    if max_monthly_payment is not None:
        total_monthly_payment = schedule[0]['Total Monthly Payment']
        if max_monthly_payment <= total_monthly_payment:
            raise MaxPaymentException(f"The max monthly payment of ${max_monthly_payment} is not greater than the total monthly payment (PITI) of ${total_monthly_payment}.")
        
        new_schedule = []
        loan_amount = loan_value - down_payment
        additional_costs = property_taxes / 12 + home_insurance / 12 + hoa_fees / 12 + pmi / 12  # Monthly additional costs
        
        for month in range(1, len(schedule) + 1):
            interest_payment = loan_amount * (interest / 12 / 100)
            principal_payment = max_monthly_payment - interest_payment - additional_costs  # Corrected principal payment calculation
            loan_amount -= principal_payment
            
            if loan_amount <= 0:
                loan_amount = 0
                principal_payment += loan_amount  # Adjust the final principal payment
                payment_date = start_date + relativedelta(months=month - 1)
                new_schedule.append({
                    'Month': payment_date.strftime('%Y-%m'),
                    'Monthly Payment': round(principal_payment + interest_payment, 2),  # Excluding additional costs
                    'Principal': round(principal_payment, 2),
                    'Interest': round(interest_payment, 2),
                    'Remaining Balance': round(loan_amount, 2),
                    'Total Monthly Payment': round(principal_payment + interest_payment + additional_costs, 2),
                    'Property Taxes': round(monthly_property_taxes, 2),
                    'Home Insurance': round(monthly_home_insurance, 2),
                    'HOA Fees': round(monthly_hoa_fees, 2),
                    'PMI': round(monthly_pmi, 2),
                    'Total Payments Sum': round(total_payments_sum, 2),
                    'Interest Sum': round(interest_sum, 2),
                    'Principal Sum': round(principal_sum, 2),
                    'Property Taxes Sum': round(property_taxes_sum, 2),
                    'Home Insurance Sum': round(home_insurance_sum, 2),
                    'HOA Fees Sum': round(hoa_fees_sum, 2),
                    'PMI Sum': round(pmi_sum, 2)

                })
                break  # Exit the loop as the loan is paid off
            
            payment_date = start_date + relativedelta(months=month - 1)

            # Update cumulative sum variables
            total_payments_sum += max_monthly_payment
            interest_sum += interest_payment
            principal_sum += principal_payment
            property_taxes_sum += monthly_property_taxes
            home_insurance_sum += monthly_home_insurance
            hoa_fees_sum += monthly_hoa_fees
            pmi_sum += monthly_pmi

            new_schedule.append({
                'Month': payment_date.strftime('%Y-%m'),
                'Monthly Payment': round(principal_payment + interest_payment, 2),  # Excluding additional costs
                'Principal': round(principal_payment, 2),
                'Interest': round(interest_payment, 2),
                'Remaining Balance': round(loan_amount, 2),
                'Total Monthly Payment': round(max_monthly_payment, 2),
                'Property Taxes': round(monthly_property_taxes, 2),
                'Home Insurance': round(monthly_home_insurance, 2),
                'HOA Fees': round(monthly_hoa_fees, 2),
                'PMI': round(monthly_pmi, 2),
                'Total Payments Sum': round(total_payments_sum, 2),
                'Interest Sum': round(interest_sum, 2),
                'Principal Sum': round(principal_sum, 2),
                'Property Taxes Sum': round(property_taxes_sum, 2),
                'Home Insurance Sum': round(home_insurance_sum, 2),
                'HOA Fees Sum': round(hoa_fees_sum, 2),
                'PMI Sum': round(pmi_sum, 2)
            })
        
        return new_schedule
    
    return schedule  # Return original schedule if max_monthly_payment is not provided