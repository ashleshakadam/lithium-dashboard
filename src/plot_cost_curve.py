import pandas as pd
import plotly.graph_objects as go
from cost_model import load_data, calculate_costs, build_cost_curve

# -----------------------------
# LOAD + PREP DATA
# -----------------------------
assets, costs = load_data()
df = calculate_costs(assets, costs)
curve = build_cost_curve(df)

curve = curve.sort_values("aisc_lce").reset_index(drop=True)

# cumulative supply
curve["cum_start"] = curve["capacity_t_lce"].cumsum() - curve["capacity_t_lce"]
curve["cum_end"] = curve["capacity_t_lce"].cumsum()

# -----------------------------
# BUILD COST CURVE
# -----------------------------
fig = go.Figure()

for _, row in curve.iterrows():
    fig.add_shape(
        type="rect",
        x0=row["cum_start"],
        x1=row["cum_end"],
        y0=0,
        y1=row["aisc_lce"],
        fillcolor="rgba(0, 0, 255, 0.7)" if row["product_type"] == "carbonate"
        else "rgba(255, 0, 0, 0.7)",
        line=dict(color="black", width=1)
    )

# -----------------------------
# HOVER POINTS (cleaner)
# -----------------------------
fig.add_trace(go.Scatter(
    x=(curve["cum_start"] + curve["cum_end"]) / 2,
    y=curve["aisc_lce"],
    mode="markers",
    marker=dict(size=6, color="black"),
    hovertext=[
        f"""
<b>{row['asset_name']}</b><br>
Company: {row['company']}<br>
Country: {row['country']}<br>
Cost: {int(row['aisc_lce'])} $/t<br>
Capacity: {int(row['capacity_t_lce'])}
"""
        for _, row in curve.iterrows()
    ],
    hoverinfo="text",
    showlegend=False
))

# -----------------------------
# PRICE LINE
# -----------------------------
price_line = curve["aisc_lce"].median()

fig.add_hline(
    y=price_line,
    line_dash="dash",
    line_color="black",
    annotation_text=f"Price ~ {int(price_line)}",
    annotation_position="top left"
)

# -----------------------------
# LEGEND (manual)
# -----------------------------
fig.add_trace(go.Scatter(
    x=[None], y=[None],
    mode='markers',
    marker=dict(size=10, color="blue"),
    name="Carbonate (Brine)"
))

fig.add_trace(go.Scatter(
    x=[None], y=[None],
    mode='markers',
    marker=dict(size=10, color="red"),
    name="Spodumene (Hard Rock)"
))

# -----------------------------
# LAYOUT
# -----------------------------
fig.update_layout(
    title="Global Lithium Cost Curve ($/t LCE)",
    xaxis_title="Cumulative Supply (t LCE)",
    yaxis_title="Cost ($/t LCE)",
    template="plotly_white",
    hovermode="closest"
)

fig.update_xaxes(range=[0, curve["cum_end"].max() * 1.05])
fig.update_yaxes(range=[0, curve["aisc_lce"].max() * 1.15])

fig.show()
