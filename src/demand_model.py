import pandas as pd

# lithium intensity (kg per kWh)
LFP_INTENSITY = 0.8
NMC_INTENSITY = 0.9

def load_demand():
    return pd.read_csv("data/demand_assumptions.csv")

def calculate_demand():
    df = load_demand()

    df["total_gwh"] = df["ev_sales_millions"] * 1e6 * df["avg_kwh_per_ev"] / 1000

    df["lfp_demand"] = df["total_gwh"] * df["lfp_share"] * LFP_INTENSITY
    df["nmc_demand"] = df["total_gwh"] * df["nmc_share"] * NMC_INTENSITY

    df["total_lithium_demand"] = df["lfp_demand"] + df["nmc_demand"]

    return df

if __name__ == "__main__":
    print(calculate_demand())
