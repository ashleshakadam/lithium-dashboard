import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from src.supply_model import build_supply_model, regional_concentration
from src.cost_model import load_data, calculate_costs
from src.demand_model import calculate_demand
from src.price_model import build_price_model


# -------------------------
# Page config
# -------------------------
st.set_page_config(
    page_title="Lithium Cost Curve Dashboard",
    layout="wide"
)


# -------------------------
# Colors
# -------------------------
PRIMARY = "#1F3A75"
SECONDARY = "#2F5DAA"
LIGHT_BLUE = "#8FB3E8"
LIGHT_GREY = "#EAEAEA"
MUTED_GREY = "#BFBFBF"
GRID = "#E5E5E5"
DEFICIT_RED = "#D62728"
# Cost curve colors
LOW = "#D6D6D6"
MID1 = "#A7C0E0"
MID2 = "#3E6BA5"
HIGH = "#0B1F3A"


# -------------------------
# Helpers
# -------------------------
def format_tonnes(x):
    if pd.isna(x):
        return "N/A"
    x = float(x)
    if abs(x) >= 1_000_000:
        return f"{x/1_000_000:.1f}M t"
    elif abs(x) >= 1_000:
        return f"{x/1_000:.0f}k t"
    return f"{x:.0f} t"


def build_cost_curve_chart(curve: pd.DataFrame, price_line: float):
    fig = go.Figure()

    # Robust percentile-based coloring so the curve never becomes all grey
    p75 = curve["cost"].quantile(0.75)
    p90 = curve["cost"].quantile(0.90)

    for _, row in curve.iterrows():
        cost = float(row["cost"]) if pd.notnull(row["cost"]) else 0.0

        if cost >= p90:
            color = HIGH   # dark navy
        elif cost >= p75:
            color = MID2
        elif cost >= p75 * 0.7:
            color = MID1
        else:
            color = LOW

        fig.add_trace(
            go.Bar(
                x=[row["cumulative_supply"]],
                y=[cost],
                width=row["capacity"] * 0.95,
                marker_color=color,
                hovertext=row.get("asset_name", "Asset"),
                hovertemplate=(
                    "<b>%{hovertext}</b><br>"
                    "Cost: %{y:,.0f} $/t LCE<br>"
                    "Cumulative supply: %{x:,.0f} t<extra></extra>"
                ),
                showlegend=False,
            )
        )

    fig.add_hline(
        y=price_line,
        line_dash="dash",
        line_color=PRIMARY,
        line_width=3,
        annotation_text="Blended Price (Market Clearing)",
        annotation_position="top left",
    )

    fig.update_layout(
        title="Global Lithium Cost Curve ($/t LCE)",
        xaxis_title="Cumulative Supply (t LCE)",
        yaxis_title="Cost ($/t LCE)",
        height=460,
        template="plotly_white",
        plot_bgcolor="white",
        margin=dict(l=30, r=30, t=60, b=30),
    )

    fig.update_yaxes(tickprefix="$", gridcolor=GRID, separatethousands=True)
    fig.update_xaxes(gridcolor=GRID, separatethousands=True)

    return fig


def build_market_balance_chart(balance_df: pd.DataFrame):
    fig = go.Figure()

    # Supply first
    fig.add_trace(
        go.Scatter(
            x=balance_df["year"],
            y=balance_df["risk_supply"],
            name="Supply",
            mode="lines+markers",
            line=dict(color=MUTED_GREY, width=2),
        )
    )

    # Demand second
    fig.add_trace(
        go.Scatter(
            x=balance_df["year"],
            y=balance_df["total_lithium_demand"],
            name="Demand",
            mode="lines+markers",
            line=dict(color=PRIMARY, width=3),
        )
    )

    # Deficit shading
    fig.add_trace(
        go.Scatter(
            x=balance_df["year"],
            y=balance_df["risk_supply"],
            mode="lines",
            line=dict(width=0),
            showlegend=False,
            hoverinfo="skip",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=balance_df["year"],
            y=balance_df["total_lithium_demand"],
            mode="lines",
            fill="tonexty",
            fillcolor="rgba(214,39,40,0.12)",
            line=dict(width=0),
            showlegend=False,
            hoverinfo="skip",
        )
    )

    latest = balance_df.iloc[-1]
    imbalance = latest["total_lithium_demand"] - latest["risk_supply"]

    fig.add_annotation(
        x=latest["year"],
        y=latest["total_lithium_demand"],
        text=f"Deficit: {format_tonnes(imbalance)}",
        showarrow=True,
        font=dict(color=DEFICIT_RED),
    )

    fig.update_layout(
        title="Market Balance",
        yaxis_title="Tonnes (LCE)",
        height=380,
        template="plotly_white",
        plot_bgcolor="white",
        margin=dict(l=30, r=30, t=60, b=30),
    )

    fig.update_yaxes(gridcolor=GRID, separatethousands=True)
    fig.update_xaxes(gridcolor=GRID)

    return fig


# -------------------------
# Sidebar
# -------------------------
st.sidebar.header("Scenario controls")

selected_year = st.sidebar.selectbox("Year", [2025, 2026, 2027], index=0)
ev_sales = st.sidebar.slider("EV sales (millions)", 10, 40, 18)
lfp_share = st.sidebar.slider("LFP share", 0.20, 0.80, 0.45)


# -------------------------
# Title
# -------------------------
st.title("Lithium Cost Curve, Market Balance & Price Outlook Dashboard")
st.markdown(
    "Asset-level costs, risk-adjusted supply, chemistry-linked demand, and scenario-based price outlook."
)


# -------------------------
# Build models
# -------------------------
supply_df = build_supply_model()
regional_df = regional_concentration(supply_df)

assets, costs = load_data()
cost_df = calculate_costs(assets, costs)

# Demand for current scenario
demand_df = calculate_demand(ev_sales=ev_sales, lfp_share=lfp_share)

# Price for selected year / current scenario
price_row = build_price_model(
    year=selected_year,
    ev_sales=ev_sales,
    lfp_share=lfp_share
)

# Cost curve for selected year only
supply_year = supply_df[supply_df["year"] == selected_year].copy()

cost_curve = supply_year.merge(
    cost_df[["asset_id", "aisc_lce"]],
    on="asset_id",
    how="left"
)

cost_curve = cost_curve.rename(columns={"aisc_lce": "cost"})
cost_curve["cost"] = pd.to_numeric(cost_curve["cost"], errors="coerce")
cost_curve = cost_curve.dropna(subset=["cost"]).sort_values("cost").reset_index(drop=True)
cost_curve["capacity"] = pd.to_numeric(cost_curve["risk_supply"], errors="coerce").fillna(0.0)
cost_curve["cumulative_supply"] = cost_curve["capacity"].cumsum()

# Market balance dataframe
balance_df = demand_df.merge(
    supply_df.groupby("year", as_index=False)["risk_supply"].sum(),
    on="year",
    how="left"
)


# -------------------------
# KPIs
# -------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Blended Price", f"${price_row['blended_price']:,.0f}/t")
col2.metric("Carbonate Price", f"${price_row['carbonate_price']:,.0f}/t")
col3.metric("Hydroxide Price", f"${price_row['hydroxide_price']:,.0f}/t")
col4.metric("Shortage Ratio", f"{price_row['weighted_shortage_ratio']:.2f}x")

st.caption("Prices = marginal cost + scarcity premium under risk-adjusted supply.")


# -------------------------
# Marginal producers
# -------------------------
st.markdown("### Marginal Producers")
m1, m2 = st.columns(2)
m1.write(f"Carbonate marginal: **{price_row['carbonate_marginal_asset']}**")
m2.write(f"Hydroxide marginal: **{price_row['hydroxide_marginal_asset']}**")


# -------------------------
# Market balance
# -------------------------
st.plotly_chart(
    build_market_balance_chart(balance_df),
    use_container_width=True
)


# -------------------------
# Executive summary
# -------------------------
st.markdown("### Executive Summary")

total_balance = price_row["total_demand"] - price_row["total_risk_supply"]
market_condition = "deficit" if total_balance > 0 else "surplus"
price_trend = "elevated" if price_row["weighted_shortage_ratio"] > 1 else "stable"

st.markdown(
    f"""
<div style="
background-color:#F5F7FA;
padding:20px;
border-radius:8px;
border-left:6px solid {PRIMARY};
">
<b>{selected_year} Market View</b><br><br>

The lithium market is in a <b>{market_condition}</b>, with imbalance of <b>{format_tonnes(total_balance)}</b>.<br><br>

Demand is driven by EV adoption (<b>{ev_sales}M vehicles</b>) and chemistry mix (<b>LFP: {lfp_share:.0%}</b>).<br><br>

Supply remains concentrated in Australia and South America.<br><br>

Prices remain <b>{price_trend}</b> due to supply-demand imbalance.
</div>
""",
    unsafe_allow_html=True,
)


# -------------------------
# Cost curve
# -------------------------
st.plotly_chart(
    build_cost_curve_chart(cost_curve, price_row["blended_price"]),
    use_container_width=True
)
st.caption("Darker bars indicate marginal and near-marginal producers that set global lithium prices.")


# -------------------------
# Regional concentration
# -------------------------
st.markdown("### Regional Supply Concentration")

regional_filtered = regional_df[regional_df["year"] == selected_year].copy()

fig_region = go.Figure()
fig_region.add_trace(
    go.Bar(
        x=regional_filtered["region"],
        y=regional_filtered["regional_share"],
        text=[f"{x:.1%}" for x in regional_filtered["regional_share"]],
        textposition="outside",
        marker_color=PRIMARY,
    )
)

fig_region.update_layout(
    height=360,
    template="plotly_white",
    yaxis_title="Regional share",
    plot_bgcolor="white",
    margin=dict(l=30, r=30, t=30, b=30),
)
fig_region.update_yaxes(tickformat=".0%", gridcolor=GRID)
fig_region.update_xaxes(gridcolor=GRID)

st.plotly_chart(fig_region, use_container_width=True)


# -------------------------
# Methodology
# -------------------------
st.markdown("### Methodology")
st.markdown(
    """
- Supply is risk-adjusted using utilization and project-stage weights  
- Demand is driven by EV sales and chemistry split  
- Carbonate maps to LFP; hydroxide maps to NMC  
- Prices follow marginal cost plus scarcity premium  
- Blended price reflects chemistry-linked demand mix  
"""
)
