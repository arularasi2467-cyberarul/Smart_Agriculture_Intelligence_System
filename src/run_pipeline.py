
from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "generated"
OUT = ROOT / "outputs"

# Keep the existing database filename for compatibility
DB = ROOT / "data" / "instamart_demo.db"


def main():

    # 1. Check required agriculture data files
    required = [
        "customers.csv",
        "orders.csv",
        "tickets.csv"
    ]

    missing = [
        x for x in required if not (DATA / x).exists()
    ]

    if missing:
        raise SystemExit(
            "Agriculture data missing. Run first: "
            "python -m src.generate_data"
        )

    # 2. Load and remove duplicate records
    farmers = pd.read_csv(
        DATA / "customers.csv"
    ).drop_duplicates("customer_id")

    activities = pd.read_csv(
        DATA / "orders.csv"
    ).drop_duplicates("order_id")

    complaints = pd.read_csv(
        DATA / "tickets.csv"
    ).drop_duplicates("ticket_id")

    # 3. Clean farm activity data
    activities["order_date"] = pd.to_datetime(
        activities["order_date"],
        errors="coerce"
    )

    activities["order_value"] = pd.to_numeric(
        activities["order_value"],
        errors="coerce"
    )

    activities = activities.dropna(
        subset=[
            "customer_id",
            "order_date",
            "order_value"
        ]
    )

    activities = activities[
        activities["order_value"] >= 0
    ]

    # 4. Clean farmer complaints
    complaints = complaints.dropna(
        subset=[
            "ticket_id",
            "customer_id",
            "category"
        ]
    )

    # 5. Create output folder
    OUT.mkdir(parents=True, exist_ok=True)

    # 6. Store cleaned data in SQLite database
    with sqlite3.connect(DB) as conn:

        farmers.to_sql(
            "customers",
            conn,
            if_exists="replace",
            index=False
        )

        activities.assign(
            order_date=activities[
                "order_date"
            ].dt.strftime("%Y-%m-%d")
        ).to_sql(
            "orders",
            conn,
            if_exists="replace",
            index=False
        )

        complaints.to_sql(
            "tickets",
            conn,
            if_exists="replace",
            index=False
        )

    # 7. Generate agriculture data quality summary
    summary = {
        "total_farmers": len(farmers),
        "total_farm_activities": len(activities),
        "total_farmer_complaints": len(complaints),

        "missing_farmer_ids_in_activities": int(
            (~activities["customer_id"].isin(
                farmers["customer_id"]
            )).sum()
        ),

        "total_farm_activity_value": round(
            float(activities["order_value"].sum()),
            2
        )
    }

    pd.Series(
        summary,
        name="value"
    ).to_csv(
        OUT / "data_quality_summary.csv",
        header=True
    )

    # 8. Generate monthly agriculture activity report
    monthly = (
        activities.assign(
            month=activities["order_date"]
            .dt.to_period("M")
            .astype(str)
        )
        .groupby("month", as_index=False)["order_value"]
        .sum()
    )

    monthly.to_csv(
        OUT / "monthly_revenue.csv",
        index=False
    )

    print("Smart Agriculture Data Pipeline completed!")
    print(pd.Series(summary))
    print(f"SQLite database: {DB}")


if __name__ == "__main__":
    main()
