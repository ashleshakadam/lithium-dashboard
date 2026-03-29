import pandas as pd

# lithium intensity (kg per kWh)
LFP_INTENSITY = 0.8
NMC_INTENSITY = 0.9

def build_demand_model():
    return pd.read_csv("data/demand_assumptions.csv")

def calculate_demand(ev_sales=None, lfp_share=None):
    import pandas as pd

    df = pd.read_csv("data/demand_assumptions.csv")

    # -----------------------------
    # SCENARIO OVERRIDES
    # -----------------------------
    if ev_sales is not None:
        df["ev_sales_millions"] = ev_sales

    if lfp_share is not None:
        df["lfp_share"] = lfp_share
        df["nmc_share"] = 1 - lfp_share

    # -----------------------------
    # DEMAND CALCULATION
    # -----------------------------
    df["total_gwh"] = df["ev_sales_millions"] * 1e6 * df["avg_kwh_per_ev"] / 1000

    df["lfp_demand"] = df["total_gwh"] * df["lfp_share"] * 0.8
    df["nmc_demand"] = df["total_gwh"] * df["nmc_share"] * 0.9

    df["total_lithium_demand"] = df["lfp_demand"] + df["nmc_demand"]

    return df

if __name__ == "__main__":
    print(calculate_demand())
