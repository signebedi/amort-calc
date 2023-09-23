import datetime
from dateutil.relativedelta import relativedelta

class MaxPaymentException(Exception):
    pass
    
def amortization_calculator(loan_value, interest, term, down_payment=0, start_date=None, property_taxes=0, home_insurance=0, hoa_fees=0, pmi=0):
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
    
    # Additional monthly costs
    additional_costs = property_taxes / 12 + home_insurance / 12 + hoa_fees / 12 + pmi / 12
    
    # Total monthly payment including optional costs
    total_monthly_payment = monthly_payment + additional_costs
    
    amortization_schedule = []
    
    for month in range(1, n_payments + 1):
        interest_payment = loan_amount * monthly_interest_rate
        principal_payment = monthly_payment - interest_payment
        loan_amount -= principal_payment
        
        payment_date = start_date + relativedelta(months=month - 1)
        
        amortization_schedule.append({
            'Month': payment_date.strftime('%Y-%m'),
            'Monthly Payment': round(monthly_payment, 2),
            'Principal': round(principal_payment, 2),
            'Interest': round(interest_payment, 2),
            'Remaining Balance': round(loan_amount, 2),
            'Total Monthly Payment': round(total_monthly_payment, 2)
        })
    
    return amortization_schedule

def adjusted_amortization_schedule(loan_value, interest, term, max_monthly_payment=None, down_payment=0, start_date=None, property_taxes=0, home_insurance=0, hoa_fees=0, pmi=0):
    schedule = amortization_calculator(loan_value, interest, term, down_payment, start_date, property_taxes, home_insurance, hoa_fees, pmi)
    
    if max_monthly_payment is not None:
        total_monthly_payment = schedule[0]['Total Monthly Payment']
        if max_monthly_payment <= total_monthly_payment:
            raise MaxPaymentException(f"The max monthly payment of ${max_monthly_payment} is not greater than the total monthly payment (PITI) of ${total_monthly_payment}.")
        
        new_schedule = []
        loan_amount = loan_value - down_payment
        for month in range(1, len(schedule) + 1):
            interest_payment = loan_amount * (interest / 12 / 100)
            principal_payment = max_monthly_payment - interest_payment - (total_monthly_payment - schedule[0]['Monthly Payment'])
            loan_amount -= principal_payment
            
            if loan_amount <= 0:
                loan_amount = 0
                principal_payment += loan_amount  # Adjust the final principal payment
                payment_date = start_date + relativedelta(months=month - 1)
                new_schedule.append({
                    'Month': payment_date.strftime('%Y-%m'),
                    'Monthly Payment': round(principal_payment + interest_payment, 2),
                    'Principal': round(principal_payment, 2),
                    'Interest': round(interest_payment, 2),
                    'Remaining Balance': round(loan_amount, 2),
                    'Total Monthly Payment': round(max_monthly_payment, 2)
                })
                break  # Exit the loop as the loan is paid off
            
            payment_date = start_date + relativedelta(months=month - 1)
            new_schedule.append({
                'Month': payment_date.strftime('%Y-%m'),
                'Monthly Payment': round(principal_payment + interest_payment, 2),
                'Principal': round(principal_payment, 2),
                'Interest': round(interest_payment, 2),
                'Remaining Balance': round(loan_amount, 2),
                'Total Monthly Payment': round(max_monthly_payment, 2)
            })
        
        return new_schedule
    
    return schedule  # Return original schedule if max_monthly_payment is not provided
