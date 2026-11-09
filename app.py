from pathlib import Path
import sqlite3
import pandas as pd
import streamlit as st

from src.rag_assistant import answer

ROOT = Path(__file__).resolve().parent
DB = ROOT / "data" / "instamart_demo.db"

st.set_page_config(
    page_title="Smart Agriculture Intelligence System",
    layout="wide"
)

st.title("Smart Agriculture Intelligence System")
st.caption(
    "Agriculture analytics demo using synthetic practice data only. "
    "Not official government or real farmer data."
)

if not DB.exists():
    st.warning(
        "Database not found. Run these commands in the VS Code terminal:\n"
        "1. python -m src.generate_data\n"
        "2. python -m src.run_pipeline"
    )

else:
    with sqlite3.connect(DB) as conn:
        farmers = pd.read_sql_query(
            "SELECT * FROM customers", conn
        )
        activities = pd.read_sql_query(
            "SELECT * FROM orders", conn
        )
        complaints = pd.read_sql_query(
            "SELECT * FROM tickets", conn
        )

    # Dashboard metrics
    c1, c2, c3 = st.columns(3)

    c1.metric("Total Farmers", f"{len(farmers):,}")
    c2.metric("Farm Activities", f"{len(activities):,}")
    c3.metric("Farmer Complaints", f"{len(complaints):,}")

    st.divider()

    # Monthly activity value
    st.subheader("Monthly Farm Activity Value")

    if not activities.empty:
        activities["order_date"] = pd.to_datetime(
            activities["order_date"]
        )

        monthly = (
            activities.assign(
                month=activities["order_date"]
                .dt.to_period("M")
                .astype(str)
            )
            .groupby("month")["order_value"]
            .sum()
        )

        st.line_chart(monthly)

    st.divider()

    # Complaint categories
    st.subheader("Farmer Complaint Categories")

    if not complaints.empty:
        st.bar_chart(
            complaints["category"].value_counts()
        )

    st.divider()

    # Farmer information
    st.subheader("Farmer Data Preview")
    st.dataframe(farmers.head(10), use_container_width=True)

    st.subheader("Farm Activity Data Preview")
    st.dataframe(activities.head(10), use_container_width=True)

    st.subheader("Farmer Complaint Data Preview")
    st.dataframe(complaints.head(10), use_container_width=True)

st.divider()

# Agriculture Knowledge Assistant
st.subheader("Agriculture Knowledge Assistant")

question = st.text_input(
    "Ask an agriculture question"
)

if st.button("Find Answer") and question:
    st.write(answer(question))

st.caption(
    "This is a local keyword-based RAG prototype, not an external LLM. "
    "Demo knowledge is fictional and should not replace expert advice."
)
