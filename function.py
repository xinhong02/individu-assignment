import pandas as pd
import os

def verify_user(ic_number, password):
    """Verify IC number format and password."""
    return len(ic_number) == 12 and password == ic_number[-4:]

def calculate_tax(income, tax_relief):
    """Calculate tax payable based on Malaysian tax rates."""
    chargeable_income = income - tax_relief
    if chargeable_income <= 0:
        return 0.0
    
    # Example progressive tax rates (update with real ones if needed)
    tax = 0.0
    if chargeable_income <= 5000:
        tax = chargeable_income * 0.01
    elif chargeable_income <= 20000:
        tax = 5000 * 0.01 + (chargeable_income - 5000) * 0.03
    elif chargeable_income <= 35000:
        tax = 5000 * 0.01 + 15000 * 0.03 + (chargeable_income - 20000) * 0.08
    else:
        tax = 5000 * 0.01 + 15000 * 0.03 + 15000 * 0.08 + (chargeable_income - 35000) * 0.13
    return round(tax, 2)

def save_to_csv(data, filename):
    """Save user data to a CSV file."""
    file_exists = os.path.isfile(filename)
    df = pd.DataFrame([data], columns=["IC Number", "Income", "Tax Relief", "Tax Payable"])
    if file_exists:
        df.to_csv(filename, mode='a', index=False, header=False)
    else:
        df.to_csv(filename, index=False)

def read_from_csv(filename):
    """Read tax data from CSV file."""
    if os.path.isfile(filename):
        return pd.read_csv(filename)
    return None