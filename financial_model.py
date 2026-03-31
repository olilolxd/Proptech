def calculate_mortgage_payment(principal, annual_rate, years):
    """Calcule le paiement hypothécaire mensuel."""
    if annual_rate == 0:
        return principal / (years * 12)
    r = annual_rate / 12
    n = years * 12
    return principal * r * ((1 + r)**n) / (((1 + r)**n) - 1)

def calculate_celiapp_benefit(contribution_per_year, years, marginal_tax_rate):
    """
    Simule l'effet du CELIAPP sur les années spécifiées.
    Max 8000$/an, limite à vie de 40000$.
    """
    total_celiapp = 0
    total_tax_return = 0
    
    for y in range(int(years)):
        contrib = min(contribution_per_year, 8000)
        # Limite à vie de 40 000 $
        if total_celiapp + contrib > 40000:
            contrib = 40000 - total_celiapp
        
        total_celiapp += contrib
        tax_return = contrib * marginal_tax_rate
        total_tax_return += tax_return
        
    return {
        "celiapp_total": total_celiapp,
        "tax_return": total_tax_return,
        "total_extra_down_payment": total_celiapp + total_tax_return
    }

def calculate_profitability(price, down_payment, monthly_rent, annual_rate=0.045, amort_years=25, 
                            municipal_tax_rate=0.007, school_tax_rate=0.001, 
                            condo_fees=0, insurance=100, maintenance_pct=0.01):
    """
    Calcule la rentabilité d'une propriété (Cap Rate, Cash Flow, Cash-on-Cash).
    """
    principal = price - down_payment
    monthly_mortgage = calculate_mortgage_payment(principal, annual_rate, amort_years)
    
    annual_revenue = monthly_rent * 12
    
    # Dépenses
    municipal_tax = price * municipal_tax_rate
    school_tax = price * school_tax_rate
    maintenance = price * maintenance_pct
    annual_expenses_no_mortgage = municipal_tax + school_tax + (condo_fees * 12) + (insurance * 12) + maintenance
    
    noi = annual_revenue - annual_expenses_no_mortgage
    cap_rate = (noi / price) * 100 if price > 0 else 0
    
    annual_cash_flow = noi - (monthly_mortgage * 12)
    cash_on_cash = (annual_cash_flow / down_payment) * 100 if down_payment > 0 else 0
    
    return {
        "monthly_mortgage": monthly_mortgage,
        "monthly_expenses": annual_expenses_no_mortgage / 12,
        "noi": noi,
        "cap_rate": cap_rate,
        "monthly_cash_flow": annual_cash_flow / 12,
        "cash_on_cash": cash_on_cash,
        "annual_return": annual_cash_flow
    }
