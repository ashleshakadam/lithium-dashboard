from src.supply_model import prepare_supply, supply_summary
from src.demand_model import calculate_demand
from src.price_model import build_price_model

# Supply
supply_df = prepare_supply()
print("\nSUPPLY:\n", supply_summary(supply_df))

# Demand
demand_df = calculate_demand()
print("\nDEMAND:\n", demand_df)

# Price
price, asset, shortage = build_price_model()

print(f"\nPRICE: {price}")
print(f"MARGINAL PRODUCER: {asset}")

if shortage:
    print("⚠️ Market in SUPPLY DEFICIT → scarcity pricing active")
else:
    print("✅ Market balanced → marginal cost pricing")
