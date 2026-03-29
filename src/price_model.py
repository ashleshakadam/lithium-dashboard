import pandas as pd

from src.cost_model import load_data as load_cost_data, calculate_costs
from src.supply_model import build_supply_model
from src.demand_model import calculate_demand


def _segment_price(curve: pd.DataFrame, demand: float, alpha: float = 1.0):
    curve = curve.sort_values("aisc_lce").reset_index(drop=True).copy()
    curve["cum_supply"] = curve["risk_supply"].cumsum()

    eligible = curve[curve["cum_supply"] >= demand]

    if eligible.empty:
        # 🔴 SHORTAGE
        marginal_row = curve.iloc[-1]

        available_supply = max(curve["cum_supply"].max(), 1.0)
        shortage_ratio = demand / available_supply

        shortage_ratio_capped = min(shortage_ratio, 4.0)
        premium_multiplier = 1 + alpha * (shortage_ratio_capped - 1) ** 0.7

        price = marginal_row["aisc_lce"] * premium_multiplier
        price = max(price, marginal_row["aisc_lce"])

        shortage = True

    else:
        # 🟢 BALANCED
        marginal_row = eligible.iloc[0]

        available_supply = curve["cum_supply"].max()
        shortage_ratio = demand / max(available_supply, 1.0)

        price = marginal_row["aisc_lce"]
        shortage = False

    return {
        "price": float(price),
        "marginal_asset": marginal_row["asset_name"],
        "shortage": shortage,
        "shortage_ratio": float(shortage_ratio),
        "available_supply": float(available_supply),
    }


def build_price_model(year=2025, ev_sales=None, lfp_share=None):
    # -----------------------------
    # Load cost data
    # -----------------------------
    assets, costs = load_cost_data()
    cost_df = calculate_costs(assets, costs)

    # -----------------------------
    # Build supply + demand
    # -----------------------------
    supply_df = build_supply_model()
    demand_df = calculate_demand(ev_sales=ev_sales, lfp_share=lfp_share)

    # -----------------------------
    # Filter demand for year
    # -----------------------------
    demand_row = demand_df[demand_df["year"] == year]
    if demand_row.empty:
        raise ValueError(f"No demand data found for year {year}")
    demand_row = demand_row.iloc[0]

    # -----------------------------
    # Filter supply for year
    # -----------------------------
    supply_year = supply_df[supply_df["year"] == year].copy()
    if supply_year.empty:
        raise ValueError(f"No supply data found for year {year}")

    # -----------------------------
    # Merge cost + supply
    # -----------------------------
    pricing_df = supply_year.merge(
        cost_df[
            [
                "asset_id",
                "asset_name",
                "company",
                "country",
                "refined_product",
                "aisc_lce",
            ]
        ],
        on=["asset_id", "asset_name", "company", "country", "refined_product"],
        how="left",
    )

    if pricing_df["aisc_lce"].isna().any():
        missing = pricing_df[pricing_df["aisc_lce"].isna()][["asset_id", "asset_name"]]
        raise ValueError(f"Missing cost data:\n{missing}")

    # -----------------------------
    # Demand split
    # -----------------------------
    lfp_demand = float(demand_row["lfp_demand"])
    nmc_demand = float(demand_row["nmc_demand"])
    total_demand = lfp_demand + nmc_demand

    # -----------------------------
    # Split curves
    # -----------------------------
    carbonate_curve = pricing_df[
        pricing_df["refined_product"] == "carbonate"
    ].copy()

    hydroxide_curve = pricing_df[
        pricing_df["refined_product"] == "hydroxide"
    ].copy()

    # -----------------------------
    # Pricing
    # -----------------------------
    carbonate_result = _segment_price(carbonate_curve, lfp_demand)
    hydroxide_result = _segment_price(hydroxide_curve, nmc_demand)

    blended_price = (
        carbonate_result["price"] * (lfp_demand / total_demand)
        + hydroxide_result["price"] * (nmc_demand / total_demand)
    )

    total_risk_supply = float(pricing_df["risk_supply"].sum())
    weighted_shortage_ratio = total_demand / max(total_risk_supply, 1.0)

    return {
        "year": int(year),
        "carbonate_price": carbonate_result["price"],
        "hydroxide_price": hydroxide_result["price"],
        "blended_price": float(blended_price),
        "carbonate_marginal_asset": carbonate_result["marginal_asset"],
        "hydroxide_marginal_asset": hydroxide_result["marginal_asset"],
        "carbonate_shortage": carbonate_result["shortage"],
        "hydroxide_shortage": hydroxide_result["shortage"],
        "carbonate_shortage_ratio": carbonate_result["shortage_ratio"],
        "hydroxide_shortage_ratio": hydroxide_result["shortage_ratio"],
        "weighted_shortage_ratio": float(weighted_shortage_ratio),
        "total_risk_supply": total_risk_supply,
        "lfp_demand": lfp_demand,
        "nmc_demand": nmc_demand,
        "total_demand": float(total_demand),
    }
