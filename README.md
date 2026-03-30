# Lithium Market Intelligence Dashboard

## Overview
A market intelligence application for analyzing lithium supply, demand, cost competitiveness, and price formation across global assets.

The system is designed to approximate how commodity research and market strategy teams evaluate lithium markets under changing EV adoption, production expansion, and cost curve scenarios.

## Business Problem
Lithium prices are driven by more than aggregate supply and demand. In practice, pricing depends on the marginal producer, the shape of the global cost curve, processing concentration, and the pace of downstream battery demand growth.

Most public analysis is fragmented across static charts and disconnected datasets, making it difficult to evaluate how incremental changes in production or demand alter market balance and pricing.

## Solution
This project integrates asset-level production, cost normalization, EV-driven demand assumptions, and market-clearing logic into a single analytical dashboard.

It allows users to:
- compare supply and demand trajectories
- inspect cost curve positioning by asset or region
- estimate marginal supply pressure
- simulate pricing implications under different market scenarios

<img width="1367" height="796" alt="image" src="https://github.com/user-attachments/assets/54674f19-ad0b-4b2b-b49b-aa8af963575c" />
<img width="1336" height="840" alt="image" src="https://github.com/user-attachments/assets/88218c18-66da-4e64-ab89-a2742ef24e60" />
<img width="1336" height="758" alt="image" src="https://github.com/user-attachments/assets/0b409e62-5992-4530-a568-931ab55c05b5" />

#### Streamlit App URL: https://lithium-dashboard-hizexmjjqbfus8zpfrvmyy.streamlit.app/

## Architecture
The application is organized as a modular analytics system:

- `app/app.py` handles the Streamlit interface and orchestration
- `src/cost_model.py` normalizes production economics into LCE terms
- `src/supply_model.py` aggregates asset-level supply
- `src/demand_model.py` models EV-linked demand growth
- `src/price_model.py` estimates market-clearing prices
- `data/` stores structured model inputs
- `outputs/` stores generated summaries and scenario outputs

## Methodology

### Supply Modeling
Production is aggregated at the asset level and can be segmented by region, extraction type, and scenario assumptions.

### Cost Modeling
Asset economics are normalized into Lithium Carbonate Equivalent to create a comparable cost basis across operations.

### Demand Modeling
Demand is projected using EV adoption assumptions and downstream lithium intensity logic.

### Price Formation
The model estimates market-clearing behavior by identifying where demand intersects the supply stack and which producers become marginal under each scenario.

## Results
Key findings from the model include:
- marginal supply is more important for pricing than headline production totals
- tight market balances can produce disproportionately large pricing moves
- steep cost curves amplify volatility
- regional concentration in refining and conversion increases systemic risk

## Tech Stack
Python, Pandas, NumPy, Streamlit

## Repository Structure
```text
lithium-dashboard/
├── app/
│   └── app.py
├── src/
│   ├── cost_model.py
│   ├── supply_model.py
│   ├── demand_model.py
│   └── price_model.py
├── data/
├── outputs/
├── main.py
├── requirements.txt
└── README.md
```

## How to Run
```text
git clone https://github.com/ashleshakadam/lithium-dashboard.git
cd lithium-dashboard
pip install -r requirements.txt
streamlit run app/app.py
```

## Future Improvements
	•	incorporate real-time pricing and trade data
	•	add battery chemistry segmentation such as LFP and NMC
	•	introduce Monte Carlo scenario simulation
	•	add geopolitical and refining bottleneck overlays

## Author
Ashlesha Kadam
