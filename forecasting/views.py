import os
import json
import joblib
import pandas as pd
from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import HttpResponse

from train_pipeline import MODEL_FILE
from .models import Product, SalesHistory

def get_forecast_dashboard_context(request_traffic, request_weather):
    if not os.path.exists(MODEL_FILE):
        return None

    model = joblib.load(MODEL_FILE)
    product = Product.objects.first()
    if not product:
        return {"error": "No products found in DB."}
        
    recent_sales = SalesHistory.objects.filter(product=product).order_by('-date')[:7]
    recent_sales = list(recent_sales)[::-1]
    
    tomorrow = datetime.now() + timedelta(days=1)
    
    live_features = pd.DataFrame([{
        'traffic_heavy': int(request_traffic),
        'weather_delay': int(request_weather),
        'Month': tomorrow.month,
        'DayOfWeek': tomorrow.weekday()  
    }])
    
    predicted_demand = int(model.predict(live_features)[0])
    safety_stock_recommendation = int(predicted_demand * 1.15)
    
    if product.current_stock < safety_stock_recommendation:
        status_alert = "UNDERSTOCK RISK: Warehouse stocks dropping lower than expected market requirements. Replenish inventory slots immediately."
        alert_color = "danger"
    elif product.current_stock > (safety_stock_recommendation * 2):
        status_alert = "OVERSTOCK RISK: Surplus accumulation detected. Expired waste threat imminent. Delay supply lines."
        alert_color = "warning"
    else:
        status_alert = "OPTIMAL STORAGE LEVELS: Warehouse volume satisfies consumer demand patterns safely."
        alert_color = "success"
        
    return {
        "product_name": product.name,
        "category": product.category,
        "current_stock": product.current_stock,
        "predicted_demand": predicted_demand,
        "recommended_stock": safety_stock_recommendation,
        "status_alert": status_alert,
        "alert_color": alert_color,
        "chart_labels": [sale.date.strftime('%Y-%m-%d') for sale in recent_sales],
        "chart_data": [sale.quantity_sold for sale in recent_sales],
        "env_weather": "Heavy Rain Gridlock Delay" if request_weather else "Clear Sky Conditions",
        "env_holiday": "Heavy Commuter Gridlock Alert" if request_traffic else "Standard Normal Traffic Flow"
    }

def dynamic_dashboard_view(request):
    # Live browser control! Pull parameter tags straight from address search bar
    # Example: http://127.0.0.1:8000/?traffic=1&weather=0
    request_traffic = int(request.GET.get('traffic', 0))
    request_weather = int(request.GET.get('weather', 0))
    
    context = get_forecast_dashboard_context(request_traffic, request_weather)
    
    if not context or "error" in context:
        return HttpResponse("Error: ML Model or PostgreSQL data layer mismatch.", status=500)
        
    return render(request, 'dashboard.html', context)