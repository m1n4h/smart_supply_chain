import os
import pandas as pd
import numpy as np
import joblib
import django

# Initialize Django environment within standalone module script
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_supply_chain_core.settings')
django.setup()

# from models import Product, SalesHistory, MODEL_FILE
from forecasting.models import Product, SalesHistory
MODEL_FILE = "demand_rf_model.pkl"


CSV_FILE_NAME = "smart_logistics_dataset.csv"

def run_etl_and_training():
    print(f"[Pipeline] Verifying data source asset: '{CSV_FILE_NAME}'...")
    if not os.path.exists(CSV_FILE_NAME):
        raise FileNotFoundError(f"Could not find {CSV_FILE_NAME} in workspace root directory.")

    # 1. Clear old dummy records
    print("[Pipeline] Flushing temporary seed data values from PostgreSQL database...")
    SalesHistory.objects.all().delete()

    # 2. Enforce active baseline distribution product
    product, _ = Product.objects.get_or_create(
        name="Azam Fresh Milk 1L",
        defaults={"category": "Dairy", "current_stock": 180, "unit_price_tzs": 2500.0}
    )

    # 3. Read raw Kaggle data using pandas chunks or entire dataset frame
    print("[Pipeline] Extracting raw lines from Kaggle dataset CSV...")
    raw_df = pd.read_csv(CSV_FILE_NAME)

    # Drop potential empty string anomalies or missing data rows
    raw_df = raw_df.dropna(subset=['Timestamp', 'Demand_Forecast'])

    print(f"[Pipeline] Transforming {len(raw_df)} Kaggle records into structured database layout...")
    
    records_to_save = []
    for _, row in raw_df.iterrows():
        # Transform strings into standard clean features
        is_heavy_traffic = 1 if str(row.get('Traffic_Status')).strip().lower() == 'heavy' else 0
        is_weather_delay = 1 if str(row.get('Logistics_Delay_Reason')).strip().lower() == 'weather' else 0
        
        # Parse datetime into standard python date
        parsed_date = pd.to_datetime(row['Timestamp']).date()
        
        # We use the dataset's Demand_Forecast column as our quantity metric!
        qty = int(float(row['Demand_Forecast']))

        records_to_save.append(SalesHistory(
            product=product,
            date=parsed_date,
            quantity_sold=max(1, qty),
            traffic_heavy=is_heavy_traffic,
            weather_delay=is_weather_delay
        ))

    # Bulk insert for speed optimization
    print("[Pipeline] Streaming clean entries directly to PostgreSQL...")
    SalesHistory.objects.bulk_create(records_to_save, batch_size=1000)
    print("✅ Database successfully seeded with real Kaggle data!")

    # 4. Train the Random Forest Regressor
    print("[Pipeline] Fetching processed entries back from DB to train Machine Learning Model...")
    queryset = SalesHistory.objects.all().values('quantity_sold', 'traffic_heavy', 'weather_delay', 'date')
    training_df = pd.DataFrame(list(queryset))

    training_df['date'] = pd.to_datetime(training_df['date'])
    training_df['Month'] = training_df['date'].dt.month
    training_df['DayOfWeek'] = training_df['date'].dt.dayofweek

    X = training_df[['traffic_heavy', 'weather_delay', 'Month', 'DayOfWeek']]
    y = training_df['quantity_sold']

    print("[Pipeline] Training Random Forest Regressor Model on real Kaggle distribution trends...")
    from sklearn.ensemble import RandomForestRegressor
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Export model file matrix binary binary matrix to disk
    joblib.dump(model, MODEL_FILE)
    print(f"🧠 SUCCESS: Custom ML model trained on Kaggle data saved to '{MODEL_FILE}'")

if __name__ == "__main__":
    run_etl_and_training()