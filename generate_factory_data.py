import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

print("⚡ Generating 1 Year of Manufacturing Data (1,200+ Blocks)...")

start_date = datetime(2025, 1, 1)
factory_records = []
tally_records = []

# Product catalogs managed by the factory
foam_products = [
    {"density": 32, "l": 75, "w": 60, "t": 4, "price": 2000},
    {"density": 40, "l": 72, "w": 36, "t": 5, "price": 1800},
    {"density": 32, "l": 78, "w": 72, "t": 6, "price": 4000},
    {"density": 28, "l": 75, "w": 36, "t": 3, "price": 1200}
]

block_counter = 4000
voucher_counter = 100

# Loop through 365 days of production loops
for day in range(365):
    current_date = start_date + timedelta(days=day)
    date_str = current_date.strftime('%Y-%m-%d')
    
    # Factory handles 2 to 4 blocks per daily shift
    daily_blocks = random.randint(2, 4)
    for _ in range(daily_blocks):
        block_counter += 1
        prod = random.choice(foam_products)
        
        # Standard input calculation with variable cutting waste additions
        inch_to_meter = 1.63871e-5
        base_vol = prod['l'] * prod['w'] * prod['t']
        standard_sheets = random.randint(15, 35)
        
        calculated_clean_weight = (base_vol * standard_sheets * inch_to_meter) * prod['density']
        # Chemical inputs include standard 5% to 15% wastage metrics
        waste_multiplier = random.uniform(1.05, 1.15)
        input_chem_weight = round(calculated_clean_weight * waste_multiplier, 1)
        
        output_count = standard_sheets
        
        # 🚨 Inject production anomalies (5% error rate)
        anomaly_trigger = random.random()
        if anomaly_trigger < 0.02:
            output_count = -5  # Supervisor keyboard typo error
        elif anomaly_trigger < 0.05:
            output_count = standard_sheets + 4  # Fabricated output log contradiction
            
        factory_records.append({
            'date': date_str,
            'block_id': f"BLK-{block_counter}",
            'foam_density': prod['density'],
            'input_chemical_weight_kg': input_chem_weight,
            'sliced_length_inches': prod['l'],
            'sliced_width_inches': prod['w'],
            'sliced_thickness_inches': prod['t'],
            'output_sheets_count': output_count
        })
        
        # Ingress accounting sales lines into Tally logs (Simulating slightly lower sales due to stock theft)
        if output_count > 0 and random.random() > 0.08:
            voucher_counter += 1
            qty_sold = max(1, output_count - random.randint(0, 2)) # Structural stock leakage hidden here
            tally_records.append({
                'tally_voucher_no': f"VOUCH-{voucher_counter}",
                'invoice_date': date_str,
                'item_description': f"{prod['density']} Density Foam Sheet - {prod['l']}x{prod['w']}x{prod['t']}",
                'quantity_sold': qty_sold,
                'total_revenue_inr': qty_sold * prod['price']
            })

pd.DataFrame(factory_records).to_csv('factory_production_logs.csv', index=False)
pd.DataFrame(tally_records).to_csv('tally_sales_export.csv', index=False)
print("🚀 Staged 1-Year production databases containing over 1,200 highly realistic entries!")
