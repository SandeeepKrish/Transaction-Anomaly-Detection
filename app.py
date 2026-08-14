import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from pathlib import Path
from sklearn.ensemble import IsolationForest

st.set_page_config(
    page_title="AI Anomaly Agent",
    page_icon="🔎",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATA = BASE_DIR / "data" / "transactions.csv"
REQUIRED_COLUMNS = {
    "transaction_id",
    "timestamp",
    "amount",
    "merchant",
    "category",
    "country",
    "device",
}


@st.cache_data
def load_default_data():
    return pd.read_csv(DEFAULT_DATA, parse_dates=["timestamp"])


def validate_and_prepare(df):
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(
            "Missing required columns: " + ", ".join(sorted(missing))
        )

    data = df.copy()
    data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")
    data["amount"] = pd.to_numeric(data["amount"], errors="coerce")

    data = data.dropna(subset=["timestamp", "amount"]).reset_index(drop=True)

    if data.empty:
        raise ValueError("No valid rows remain after cleaning the uploaded file.")

    if (data["amount"] < 0).any():
        raise ValueError("Amount must not contain negative values.")

    return data


def detect_anomalies(df, contamination=0.025):
    x = df.copy()
    x["hour"] = x["timestamp"].dt.hour
    x["day_of_week"] = x["timestamp"].dt.dayofweek
    x["log_amount"] = np.log1p(x["amount"])

    features = x[["amount", "hour", "day_of_week", "log_amount"]]

    model = IsolationForest(
        n_estimators=300,
        contamination=contamination,
        random_state=42,
    )

    x["anomaly_label"] = model.fit_predict(features)
    x["anomaly_score"] = -model.decision_function(features)

    x["risk"] = pd.qcut(
        x["anomaly_score"].rank(method="first"),
        4,
        labels=["Low", "Medium", "High", "Critical"],
    )

    return x


def explain(row):
    reasons = []

    if row["amount"] > 250:
        reasons.append(f"unusually high amount (₹{row['amount']:,.0f})")

    if row["hour"] < 5 or row["hour"] >= 23:
        reasons.append(f"unusual transaction time ({row['hour']:02d}:00)")

    if not reasons:
        reasons.append(
            "the transaction is statistically different from normal behavior"
        )

    return "Flagged because " + " and ".join(reasons) + "."


st.title("🔎 AI Anomaly Agent")
st.caption(
    "Transaction anomaly detection using Isolation Forest + analyst-friendly explanations"
)

with st.sidebar:
    st.header("Dataset")
    uploaded_file = st.file_uploader(
        "Upload a transaction CSV",
        type=["csv"],
        help=(
            "Required columns: transaction_id, timestamp, amount, merchant, "
            "category, country, device"
        ),
    )

    st.divider()
    st.subheader("Model")
    st.write("**Algorithm:** Isolation Forest")
    st.write("**Contamination:** 2.5%")
    st.write("**Features:** amount, hour, day_of_week, log_amount")

    st.divider()
    st.caption(
        "An anomaly is an unusual observation, not proof of fraud. "
        "Analysts should validate flagged transactions."
    )

try:
    if uploaded_file is not None:
        raw_df = pd.read_csv(uploaded_file)
        df = validate_and_prepare(raw_df)
        source_label = "Uploaded dataset"
    else:
        df = validate_and_prepare(load_default_data())
        source_label = "Bundled demo dataset"
except Exception as exc:
    st.error(f"Could not load the dataset: {exc}")
    st.stop()

df = detect_anomalies(df)

st.success(f"{source_label} loaded successfully — {len(df):,} transactions.")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Transactions", f"{len(df):,}")
c2.metric("Anomalies", f"{(df.anomaly_label == -1).sum():,}")
c3.metric(
    "Anomaly Rate",
    f"{(df.anomaly_label == -1).mean() * 100:.2f}%",
)
c4.metric("Max Amount", f"₹{df.amount.max():,.2f}")

st.divider()

left, right = st.columns(2)

with left:
    fig = px.histogram(
        df,
        x="amount",
        nbins=60,
        title="Transaction Amount Distribution",
        labels={"amount": "Amount (₹)", "count": "Transactions"},
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    daily = (
        df.set_index("timestamp")
        .resample("D")["amount"]
        .sum()
        .reset_index()
    )
    fig2 = px.line(
        daily,
        x="timestamp",
        y="amount",
        title="Daily Transaction Value",
        labels={"timestamp": "Date", "amount": "Total Amount (₹)"},
    )
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("🚨 Highest-risk transactions")

anoms = (
    df[df.anomaly_label == -1]
    .copy()
    .sort_values("anomaly_score", ascending=False)
)

anoms["explanation"] = anoms.apply(explain, axis=1)

display_columns = [
    "transaction_id",
    "timestamp",
    "amount",
    "merchant",
    "category",
    "device",
    "risk",
    "anomaly_score",
    "explanation",
]

st.dataframe(
    anoms[display_columns].head(30),
    use_container_width=True,
    hide_index=True,
)

if not anoms.empty:
    st.subheader("🤖 Analyst explanation")

    selected = st.selectbox(
        "Choose a flagged transaction",
        anoms["transaction_id"].head(50).tolist(),
    )

    row = anoms[anoms.transaction_id == selected].iloc[0]

    st.info(
        f"**{row.transaction_id}** — {explain(row)} "
        f"The model anomaly score is **{row.anomaly_score:.3f}**. "
        "Recommended action: review the transaction and compare it "
        "with the customer's recent baseline."
    )

st.subheader("📊 Anomalies by merchant")

merchant_counts = (
    anoms.groupby("merchant")
    .size()
    .reset_index(name="anomalies")
    .sort_values("anomalies", ascending=False)
)

if not merchant_counts.empty:
    fig3 = px.bar(
        merchant_counts,
        x="merchant",
        y="anomalies",
        title="Flagged Transactions by Merchant",
        labels={"merchant": "Merchant", "anomalies": "Anomalies"},
    )
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("No anomalies were found in the current dataset.")

st.download_button(
    "📥 Download flagged transactions",
    anoms.to_csv(index=False),
    "flagged_transactions.csv",
    "text/csv",
)

st.caption(
    "Demo data is synthetic. Model flags should be investigated rather than "
    "treated as confirmed fraud."
)
