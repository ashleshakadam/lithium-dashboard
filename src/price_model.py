import pandas as pd

from src.cost_model import load_data, calculate_costs, build_cost_curve
from src.supply_model import prepare_supply
from src.demand_model import calculate_demand


def build_price_model():
    # -----------------------------
    # LOAD COST CURVE
    # -----------------------------
    assets, costs = load_data()
    df_cost = calculate_costs(assets, costs)
    curve = build_cost_curve(df_cost)

    # Sort by cost (low → high)
    curve = curve.sort_values("aisc_lce").reset_index(drop=True)

    # Build cumulative supply
    curve["cum_supply"] = curve["capacity_t_lce"].cumsum()

    # -----------------------------
    # LOAD SUPPLY + DEMAND
    # -----------------------------
    supply_df = prepare_supply()
    demand_df = calculate_demand()

    # ⚠️ For now: pick first available year
    total_supply = supply_df.groupby("year")["risk_supply"].sum().iloc[0]
    demand = demand_df["total_lithium_demand"].iloc[0]

    # -----------------------------
    # PRICE FORMATION LOGIC
    # -----------------------------
    eligible = curve[curve["cum_supply"] >= demand]

    if len(eligible) == 0:
        # 🔴 SUPPLY DEFICIT → scarcity pricing
        marginal_row = curve.iloc[-1]

        # Apply scarcity premium (simple version)
        price = marginal_row["aisc_lce"] * 1.5

        shortage = True

    else:
        # 🟢 NORMAL MARKET → marginal cost pricing
        marginal_row = eligible.iloc[0]
        price = marginal_row["aisc_lce"]

        shortage = False

    # -----------------------------
    # OUTPUT
    # -----------------------------
    return price, marginal_row["asset_name"], shortage


# -----------------------------
# TEST RUN
# -----------------------------
if __name__ == "__main__":
    price, asset, shortage = build_price_model()

    print(f"\nEstimated Price: {price}")
    print(f"Marginal Producer: {asset}")

    if shortage:
        print("⚠️ Market in SUPPLY DEFICIT → scarcity pricing active")
    else:
        print("✅ Market balanced → marginal cost pricing")
