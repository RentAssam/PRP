def calculate_prp(basic, da, company_rating, individual_rating, employee_type, profit_met):
    # Core calculation logic
    multipliers = {
        'company': {'Good': 1.0, 'Very Good': 1.2, 'Excellent': 1.5},
        'individual': {1: 0.0, 2: 0.5, 3: 1.0, 4: 1.3, 5: 1.5}
    }
    
    if profit_met != 'Yes':
        return 0.0
    
    total = basic + da
    company = multipliers['company'][company_rating]
    individual = multipliers['individual'][individual_rating]
    cap = 0.5 if employee_type == 'Executive' else 0.3
    
    return round(min(total * company * individual, total * cap), 2)

def tax_impact(prp):
    return round(prp * 0.8 * 0.7, 2)  # 20% exemption + 30% tax

def retirement_projections(prp, years):
    return [round(prp * (1.05 ** year), 2) for year in range(1, years+1)]