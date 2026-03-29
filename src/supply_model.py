import pandas as pd

RISK_WEIGHTS = {
    "operating": 1.0,
    "construction": 0.7,
    "feasibility": 0.4,
    "development": 0.2
}


def load_data():
    assets = pd.read_csv("data/asset_registry.csv")
    production = pd.read_csv("data/production_profiles.csv")
    return assets, production


def build_supply_model():
    assets, production = load_data()
    df = production.merge(assets, on="asset_id", how="left")

    df["stage_weight"] = df["project_stage"].map(RISK_WEIGHTS).fillna(0.5)

    df["nominal_supply"] = df["capacity_t_lce"] * df["utilization"]
    df["risk_supply"] = (
        df["capacity_t_lce"] *
        df["utilization"] *
        df["risk_weight"] *
        df["stage_weight"]
    )

    return df


def supply_summary(df):
    return df.groupby("year", as_index=False)[["nominal_supply", "risk_supply"]].sum()


def supply_by_region(df):
    return (
        df.groupby(["year", "region"], as_index=False)["risk_supply"]
        .sum()
        .sort_values(["year", "risk_supply"], ascending=[True, False])
    )


def supply_by_product(df):
    return (
        df.groupby(["year", "refined_product"], as_index=False)["risk_supply"]
        .sum()
        .sort_values(["year", "risk_supply"], ascending=[True, False])
    )


def regional_concentration(df):
    grouped = (
        df.groupby(["year", "region"], as_index=False)["risk_supply"]
        .sum()
    )
    grouped["regional_share"] = grouped.groupby("year")["risk_supply"].transform(
        lambda s: s / s.sum()
    )
    return grouped.sort_values(["year", "regional_share"], ascending=[True, False])


if __name__ == "__main__":
    df = build_supply_model()
    print("\nSUPPLY SUMMARY\n", supply_summary(df))
    print("\nSUPPLY BY REGION\n", supply_by_region(df))
    print("\nSUPPLY BY PRODUCT\n", supply_by_product(df))
    print("\nREGIONAL CONCENTRATION\n", regional_concentration(df))
