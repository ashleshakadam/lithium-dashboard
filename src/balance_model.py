import pandas as pd

from src.supply_model import prepare_supply
from src.demand_model import calculate_demand
from src.price_model import build_price_model


def build_balance_table(ev_sales=None, lfp_share=None):
    supply_df = prepare_supply()
    demand_df = calculate_demand(ev_sales=ev_sales, lfp_share=lfp_share)

    supply_product = (
        supply_df.groupby(["year", "refined_product"], as_index=False)["risk_supply"]
        .sum()
    )

    carbonate_supply = (
        supply_product[supply_product["refined_product"] == "carbonate"]
        [["year", "risk_supply"]]
        .rename(columns={"risk_supply": "carbonate_supply"})
    )

    hydroxide_supply = (
        supply_product[supply_product["refined_product"] == "hydroxide"]
        [["year", "risk_supply"]]
        .rename(columns={"risk_supply": "hydroxide_supply"})
    )

    supply_total = (
        supply_df.groupby("year", as_index=False)["risk_supply"]
        .sum()
        .rename(columns={"risk_supply": "total_supply"})
    )

    balance = (
        demand_df.merge(carbonate_supply, on="year", how="left")
        .merge(hydroxide_supply, on="year", how="left")
        .merge(supply_total, on="year", how="left")
    )

    balance["carbonate_supply"] = balance["carbonate_supply"].fillna(0.0)
    balance["hydroxide_supply"] = balance["hydroxide_supply"].fillna(0.0)
    balance["total_supply"] = balance["total_supply"].fillna(0.0)

    balance["carbonate_balance"] = balance["carbonate_supply"] - balance["lfp_demand"]
    balance["hydroxide_balance"] = balance["hydroxide_supply"] - balance["nmc_demand"]
    balance["total_balance"] = balance["total_supply"] - balance["total_lithium_demand"]

    price_rows = []
    for year in balance["year"]:
        result = build_price_model(year=int(year), ev_sales=ev_sales, lfp_share=lfp_share)
        price_rows.append(result)

    price_df = pd.DataFrame(price_rows)

    final = balance.merge(
        price_df[
            [
                "year",
                "carbonate_price",
                "hydroxide_price",
                "blended_price",
                "carbonate_marginal_asset",
                "hydroxide_marginal_asset",
                "carbonate_shortage_ratio",
                "hydroxide_shortage_ratio",
                "weighted_shortage_ratio",
            ]
        ],
        on="year",
        how="left",
    )

    return final.sort_values("year").reset_index(drop=True)


if __name__ == "__main__":
    print(build_balance_table())
