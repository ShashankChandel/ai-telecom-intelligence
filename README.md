# Telecom Revenue & Network Intelligence

An interactive telecom analytics dashboard built with Python, Pandas, NumPy, Plotly, and Streamlit to explore revenue performance, billing patterns, collections, and potential operational anomalies.

## Project Overview

This project demonstrates how analytics and rule-based monitoring can help telecom teams investigate billing discrepancies, monitor collections, assess regional performance, and identify potential revenue assurance risks.

The dashboard uses a synthetic telecom dataset to simulate an analytical workflow from data exploration to anomaly investigation and CSV export.

## Business Use Cases

- Revenue assurance and billing discrepancy monitoring
- Collection performance analysis
- Regional and service-level performance tracking
- Activation delay monitoring
- Prioritisation of records for further investigation

## Key Features

- Interactive filters for region, service type, and alert priority
- Revenue and billed amount comparison
- Monthly revenue trend analysis
- Regional anomaly monitoring
- Priority-based investigation table
- CSV export of filtered alert records

## Technology Stack

- **Language:** Python
- **Data processing:** Pandas, NumPy
- **Visualisation:** Plotly
- **Dashboard:** Streamlit
- **Exploration:** Jupyter Notebook

## Dataset

The project uses 5,000 synthetically generated records. No real customer information or confidential company data is included.

## Rule-Based Anomaly Detection

The current implementation uses illustrative rules to flag records for review:

| Anomaly type | Rule |
|---|---|
| Billing anomaly | Billed amount is below 50% of monthly revenue |
| Activation anomaly | Activation delay exceeds 10 days |
| Collection anomaly | Collection amount is zero despite a positive billed amount |

These rules are intended to demonstrate exception monitoring. A flagged record is not proof of revenue loss, fraud, or an operational failure.

## Getting Started

### Prerequisites

Install a compatible Python version and ensure that `pip` is available.

### Installation

Clone or download this repository, then open a terminal in the project directory.

Install dependencies:

```bash
pip install -r requirements.txt
```

### Run the Dashboard

```bash
streamlit run app.py
```

The local Streamlit URL will appear in the terminal after the application starts.

## Project Structure

```text
ai-telecom-intelligence/
├── app.py
├── 01_data_generation.ipynb
├── requirements.txt
└── README.md
```

*Note: This structure lists the current known project files. Include any additional dataset or supporting files if they exist in your repository.*

## Limitations

- The dataset is synthetic and does not represent actual telecom performance.
- Anomaly detection is rule-based rather than a trained machine-learning model.
- Thresholds are illustrative and may require business validation before operational use.

## Disclaimer

This is an independent portfolio demonstration built with synthetic data. It is not an official product or representation of any telecom operator. Findings are illustrative and should not be interpreted as actual business performance or confirmed revenue losses.
