# 🔎 AI Anomaly Agent — Data Analyst Portfolio Project

An end-to-end Streamlit portfolio project that detects unusual transactions with **Isolation Forest** and presents analyst-friendly explanations.

## 🚀 Live deployment

This project is designed to deploy on **Streamlit Community Cloud** from a public GitHub repository.

### Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

### Deploy to Streamlit Community Cloud

1. Create a **public GitHub repository**.
2. Upload the contents of this folder so `app.py` and `requirements.txt` are at the repository root.
3. Open Streamlit Community Cloud and connect your GitHub account.
4. Create an app using:
   - Repository: `YOUR_USERNAME/ai-anomaly-agent`
   - Branch: `main`
   - Main file: `app.py`
5. Deploy.

The app includes a bundled synthetic dataset, so it works immediately after deployment. Users can also upload their own CSV.

## 📄 CSV format

Uploaded files must contain these columns:

```text
transaction_id
timestamp
amount
merchant
category
country
device
```

Example:

```text
transaction_id,timestamp,amount,merchant,category,country,device
TXN00001,2026-01-01 10:30:00,120.50,Amazon,Shopping,IN,Android
```

## 🧠 How it works

```text
CSV
 ↓
Validation & cleaning
 ↓
Feature engineering
 ↓
Isolation Forest
 ↓
Anomaly label + anomaly score
 ↓
Risk ranking
 ↓
Analyst explanation
 ↓
Interactive Streamlit dashboard
```

### ML features

The current Isolation Forest uses:

- `amount`
- transaction `hour`
- `day_of_week`
- `log_amount`

The current explanation layer is **rule-based**, not an LLM call. The `openai` package was removed from the deployment requirements because it is not used by the current implementation.

## ⚠️ Important

An anomaly is **not proof of fraud**. Production use should validate thresholds using labelled historical cases and domain expertise.

## 📁 Project structure

```text
ai_anomaly_agent/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── transactions.csv
├── sql/
│   └── analysis.sql
└── src/
    └── model_notes.md
```

## 🔮 Future upgrades

- PostgreSQL integration
- Scheduled ingestion
- Customer-level behavioral baselines
- Merchant/device features
- Alerting through email/Slack
- SHAP/model explainability
- Model monitoring
- Optional production LLM agent
