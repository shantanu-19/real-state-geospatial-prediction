def calculate_investment_metrics(current_price, predicted_appreciation_rate, annual_rent):
    # 1. 5-Year Price Projection
    # Future Value = Present Value * (1 + r)^n
    projections = {
        'year_1': current_price * (1 + predicted_appreciation_rate),
        'year_3': current_price * (1 + predicted_appreciation_rate)**3,
        'year_5': current_price * (1 + predicted_appreciation_rate)**5
    }
    
    # 2. Rental Yield
    gross_yield = (annual_rent / current_price) * 100
    
    # 3. Deal Rating
    # If the model says it's worth 1Cr but it's listed at 85L, it's 'Undervalued'
    return projections, gross_yield

def get_deal_score(listing_price, model_predicted_price):
    ratio = listing_price / model_predicted_price
    if ratio < 0.85: return "🔥 High Value (Undervalued)"
    elif 0.85 <= ratio <= 1.15: return "⚖️ Fair Market Price"
    else: return "🚩 Overpriced"