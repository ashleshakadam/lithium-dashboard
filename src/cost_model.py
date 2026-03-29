import pandas as pd

# -----------------------------
# LOAD DATA
# -----------------------------
def load_data():
    assets = pd.read_csv("data/asset_registry.csv")
    costs = pd.read_csv("data/cost_inputs.csv")
    return assets, costs


# -----------------------------
# COST CALCULATIONS
# -----------------------------
def calculate_costs(assets, costs):
    df = assets.merge(costs, on="asset_id")

    # C1 Cost
    df["c1_cost"] = (
        df["mining_cost"]
        + df["processing_cost"]
        + df["transport_cost"]
        + df["royalties"]
        + df["g_and_a"]
        - df["byproduct_credit"]
    )

    # AISC
    df["aisc"] = (
        df["c1_cost"]
        + df["sustaining_capex"]
        + df["conversion_cost"]
    )

    # Normalize to LCE ($/t)
    df["aisc_lce"] = df["aisc"] / df["lce_conversion_factor"]

    return df


# -----------------------------
# BUILD COST CURVE
# -----------------------------
def build_cost_curve(df):
    df = df.sort_values("aisc_lce").reset_index(drop=True)

    # cumulative supply
    df["cumulative_supply"] = df["capacity_t_lce"].cumsum()

    return df


# -----------------------------
# MAIN EXECUTION
# -----------------------------
if __name__ == "__main__":
    assets, costs = load_data()

    df = calculate_costs(assets, costs)
    curve = build_cost_curve(df)

    print("\n=== LITHIUM COST CURVE ===\n")
    print(curve[[
        "asset_name",
        "asset_type",
        "product_type",
        "aisc_lce",
        "cumulative_supply"
    ]])
