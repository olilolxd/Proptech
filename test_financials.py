import pytest
from financial_model import calculate_mortgage_payment, calculate_celiapp_benefit, calculate_profitability

def test_calculate_mortgage_payment():
    # Emprunt de 400000 à 5% sur 25 ans
    pmt = calculate_mortgage_payment(400000, 0.05, 25)
    assert round(pmt, 2) == 2338.36

def test_calculate_celiapp():
    # 8000 par an pendant 3 ans au taux marginal de 40%
    res = calculate_celiapp_benefit(8000, 3, 0.40)
    assert res["celiapp_total"] == 24000
    assert res["tax_return"] == 9600
    assert res["total_extra_down_payment"] == 33600

    # Test dépassement de limite 40k
    res2 = calculate_celiapp_benefit(8000, 6, 0.30)
    assert res2["celiapp_total"] == 40000 # Max cap

def test_calculate_profitability():
    res = calculate_profitability(price=500000, down_payment=100000, monthly_rent=2500, annual_rate=0.05)
    # Principal = 400000, Mortgage = 2338.36
    # Revenues = 30000
    # Taxes = 500000 * 0.007 + 500000 * 0.001 = 3500 + 500 = 4000
    # Maintenance = 500000 * 0.01 = 5000
    # Ins = 1200
    # Total expenses = 10200
    # NOI = 30000 - 10200 = 19800
    assert res["noi"] == 19800
    assert round(res["cap_rate"], 2) == 3.96
    # Cash flow = 19800 - (2338.36 * 12) = 19800 - 28060.32 = -8260.32
    assert round(res["annual_return"], 2) == -8260.34 # due to float precision
