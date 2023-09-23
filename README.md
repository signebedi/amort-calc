# amort-calc
a python amortization calculator


### Examples

```python
from calc import amortization_calculator, adjusted_amortization_schedule
# Example 1 using amortization_calculator
loan_value = 300000
term = 30
interest = 9.5
down_payment = 150000
property_taxes = 7000
insurance = 2000
pmi = 0
hoa = 0

schedule_1 = amortization_calculator(
    loan_value=loan_value,
    interest=interest,
    term=term,
    down_payment=down_payment,
    property_taxes=property_taxes,
    home_insurance=insurance,
    hoa_fees=hoa,
    pmi=pmi
)

# Print first 12 months of amortization schedule
for payment in schedule_1[:12]:
    print(payment)

### Example 2:
max_monthly_payment = 2500

schedule_2 = adjusted_amortization_schedule(
    loan_value=loan_value,
    interest=interest,
    term=term,
    max_monthly_payment=max_monthly_payment,
    down_payment=down_payment,
    property_taxes=property_taxes,
    home_insurance=insurance,
    hoa_fees=hoa,
    pmi=pmi
)

# Print first 12 months of adjusted amortization schedule
for payment in schedule_2[:12]:
    print(payment)

```
