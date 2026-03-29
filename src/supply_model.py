import pandas as pd

RISK_WEIGHTS = {
    "operating": 1.0,
    "construction": 0.7,
    "feasibility": 0.4
}

def load_data():
    assets = pd.read_csv("data/asset_registry.csv")
    production = pd.read_csv("data/production_profiles.csv")
    return assets, production

def prepare_supply():
    assets, production = load_data()

    df = production.merge(assets, on="asset_id")

    df["stage_weight"] = df["project_stage"].map(RISK_WEIGHTS)

    df["nominal_supply"] = df["capacity"] * df["utilization"]

    df["risk_supply"] = (
        df["capacity"] *
        df["utilization"] *
        df["risk_weight"] *
        df["stage_weight"]
    )

    return df

def supply_summary(df):
    return df.groupby("year")[["nominal_supply", "risk_supply"]].sum()

def supply_by_region(df):
    return df.groupby(["year", "region"])["risk_supply"].sum().reset_index()

def supply_by_product(df):
    return df.groupby(["year", "refined_product"])["risk_supply"].sum().reset_index()


if __name__ == "__main__":
    df = prepare_supply()
    print(supply_summary(df))
    print(supply_by_region(df))
    print(supply_by_product(df))
