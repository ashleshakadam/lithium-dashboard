## Lithium Market Intelligence Dashboard

A production-grade analytical application that models lithium cost curves, supply-demand dynamics, and price formation across global assets. Designed to replicate how commodity research teams evaluate lithium markets under varying demand and technology scenarios.

#### Overview

The lithium market is structurally complex, driven by:
	•	Fragmented upstream supply (brine vs hard rock)
	•	Concentrated refining capacity (China dominance)
	•	Rapidly evolving demand from EV adoption
	•	Shifting battery chemistries (LFP vs NMC)

This project builds a bottom-up, asset-level model to simulate how these forces interact and determine:
	•	Market balance (deficit/surplus)
	•	Marginal producers
	•	Price formation

#### Core Question This Project Answers

##### What actually determines lithium prices — total supply or marginal supply?

This dashboard demonstrates that:
	•	Marginal supply (highest-cost required production) drives pricing
	•	Not total capacity, but which assets are needed to meet demand

#### Key Features
	•	Global Cost Curve
	•	Ranks lithium assets by AISC (LCE basis)
	•	Identifies marginal producers
	•	Supply–Demand Balance
	•	Tracks deficits/surpluses across years
	•	Shows structural tightness in the market
	•	Price Formation Engine
	•	Market price = marginal cost + scarcity premium
	•	Dynamically adjusts based on imbalance
	•	Scenario Modeling
	•	EV adoption (volume-driven demand)
	•	Battery chemistry mix (LFP vs NMC)
	•	Executive Insights Layer
	•	Converts raw outputs into business-readable conclusions

#### Live Application

### https://lithium-dashboard-hizexmjjqbfus8zpfrvmyy.streamlit.app/


#### Tech Stack
	•	Python (Pandas, NumPy)
	•	Plotly (interactive visualization)
	•	Streamlit (frontend)
	•	Modular architecture:
	•	cost_model.py
	•	supply_model.py
	•	demand_model.py
	•	price_model.py

#### Project Architecture
```text
lithium-dashboard/
│
├── app/
│   └── app.py                  # UI and orchestration
│
├── src/
│   ├── cost_model.py          # Cost normalization (AISC to LCE)
│   ├── supply_model.py        # Production aggregation
│   ├── demand_model.py        # EV-driven demand
│   └── price_model.py         # Market clearing logic
│
├── data/
│   ├── asset_registry.csv
│   ├── cost_inputs.csv
│   ├── demand_assumptions.csv
│   └── production_profiles.csv
│
├── outputs/
│   ├── supply_balance.csv
│   ├── supply_summary.csv
│   └── regional_concentration.csv
```

#### Methodology

###### 1. Cost Modeling
	•	Converts asset-level operating costs into Lithium Carbonate Equivalent (LCE)
	•	Standardizes across:
	•	Brine operations
	•	Hard rock (spodumene) operations

##### Output: Comparable global cost curve


#### 2. Supply Modeling
	•	Aggregates production at the asset level
	•	Builds cumulative supply curve

##### Key idea:
Supply is not uniform — it is cost-layered

#### 3. Demand Modeling

Demand is driven by:
	•	EV sales (volume)
	•	Battery chemistry mix:
	•	LFP → lower lithium intensity
	•	NMC → higher lithium intensity

##### Converts EV demand into LCE requirement

#### 4. Price Formation Logic

Market-clearing price is determined by:

Price = Marginal Cost of Supply + Scarcity Premium

Cases:
	•	Balanced Market
	•	Price = marginal asset cost
	•	Deficit Market
	•	Demand exceeds supply
	•	Price increases beyond marginal cost
	•	Shortage ratio applied

##### This reflects real commodity pricing behavior


#### Key Insights from the Model

##### 1. Marginal Supply Drives Price (NOT Total Supply)

Even if total supply appears sufficient:
	•	Prices are set by the highest-cost asset needed
	•	This explains price spikes during tight markets

##### 2. Structural Deficits Keep Prices Elevated

The model shows:
	•	Persistent deficits under high EV adoption
	•	Supply growth lags demand expansion

#### Result:
Prices remain structurally high

#### 3. Battery Chemistry is a Hidden Demand Lever
	•	Increasing LFP share reduces lithium intensity
	•	Slows demand growth without reducing EV adoption

##### Critical for forecasting long-term demand

#### 4. Supply is Geographically Concentrated
	•	Brine → South America (Chile, Argentina)
	•	Hard rock → Australia
	•	Refining → China

##### Creates:
	•	Supply chain risk
	•	Pricing power concentration

#### 5. Refining Bottlenecks Matter (Even if Not Modeled Fully)

Even if mining capacity exists:
	•	Lack of refining capacity constrains usable supply

##### Real-world implication:
Countries with reserves but no refining remain dependent


#### 6. Market Tightness is Non-Linear

Small changes in demand:
	•	Can push market into deficit
	•	Cause disproportionate price increases


Example Interpretation (2025 Scenario)
	•	Market is in deficit
	•	Demand driven by:
	•	~18M EV sales
	•	~45% LFP share
	•	Marginal producers:
	•	Higher-cost operations required

##### Implication:
Prices remain elevated due to structural imbalance

#### Business Value of This Model

This framework can be used by:
	•	Commodity analysts (price forecasting)
	•	Investment teams (asset valuation)
	•	Supply chain strategists (risk analysis)
	•	Policymakers (resource planning)

Limitations
	•	Does not fully model refining bottlenecks
	•	No inventory/stockpile dynamics
	•	Static cost assumptions (no inflation curves)
	•	No geopolitical disruption modeling


#### Future Enhancements
	•	Add refining capacity layer
	•	Include regional pricing spreads
	•	Introduce inventory cycles
	•	Add Monte Carlo scenario simulation
	•	Expand to multi-year forecasting

#### How to Run Locally

pip install -r requirements.txt
streamlit run app/app.py


#### Author

###### Ashlesha Kadam
###### MS Business Analytics & AI – UT Dallas
