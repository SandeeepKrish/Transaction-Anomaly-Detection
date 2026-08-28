# 🔎 AI Anomaly Agent 

An end-to-end Streamlit portfolio project that detects unusual transactions with **Isolation Forest** and presents analyst-friendly explanations.

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
