from pathlib import Path

from src.supply_model import prepare_supply, supply_summary, regional_concentration
from src.demand_model import calculate_demand
from src.price_model import build_price_model
from src.balance_model import build_balance_table

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def main():
    supply_df = prepare_supply()
    demand_df = calculate_demand()
    balance_df = build_balance_table()

    print("\nSUPPLY SUMMARY:\n")
    print(supply_summary(supply_df))

    print("\nDEMAND:\n")
    print(demand_df)

    print("\nBASE YEAR PRICE (2025):\n")
    base_price = build_price_model(year=2025)
    print(base_price)

    print("\nREGIONAL CONCENTRATION:\n")
    print(regional_concentration(supply_df))

    print("\nMULTI-YEAR BALANCE:\n")
    print(
        balance_df[
            [
                "year",
                "carbonate_supply",
                "hydroxide_supply",
                "lfp_demand",
                "nmc_demand",
                "total_supply",
                "total_lithium_demand",
                "total_balance",
                "carbonate_price",
                "hydroxide_price",
                "blended_price",
            ]
        ]
    )

    print("\nSCENARIOS:\n")
    for label, ev_sales, lfp_share in [
        ("BASE", None, None),
        ("HIGH EV", 30, None),
        ("HIGH LFP", None, 0.70),
        ("HIGH EV + HIGH LFP", 35, 0.75),
    ]:
        scenario_balance = build_balance_table(ev_sales=ev_sales, lfp_share=lfp_share)
        print(f"\n--- {label} ---")
        print(
            scenario_balance[
                ["year", "total_lithium_demand", "total_supply", "total_balance", "blended_price"]
            ]
        )

    supply_summary(supply_df).to_csv(OUTPUT_DIR / "supply_summary.csv", index=False)
    regional_concentration(supply_df).to_csv(OUTPUT_DIR / "regional_concentration.csv", index=False)
    balance_df.to_csv(OUTPUT_DIR / "supply_balance.csv", index=False)


if __name__ == "__main__":
    main()
