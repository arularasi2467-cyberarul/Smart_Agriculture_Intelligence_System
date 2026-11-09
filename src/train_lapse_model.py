
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
import joblib

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "generated"
OUT = ROOT / "outputs"
MODEL = ROOT / "data" / "farmer_inactivity_model.joblib"


def main():
    activities_path = DATA / "orders.csv"
    farmers_path = DATA / "customers.csv"

    if not activities_path.exists() or not farmers_path.exists():
        raise SystemExit("Run python -m src.generate_data first.")

    activities = pd.read_csv(
        activities_path,
        parse_dates=["order_date"]
    )
    farmers = pd.read_csv(farmers_path)

    # Last 60 days are used to check farmer inactivity
    cutoff = activities["order_date"].max() - pd.Timedelta(days=60)

    historical = activities[
        activities["order_date"] <= cutoff
    ]

    features = historical.groupby("customer_id").agg(
        activity_count=("order_id", "count"),
        avg_activity_value=("order_value", "mean"),
        last_activity=("order_date", "max")
    ).reset_index()

    features["days_since_last_activity"] = (
        cutoff - features["last_activity"]
    ).dt.days

    # Check whether farmers performed activities in the next 60 days
    future = activities[
        (activities["order_date"] > cutoff) &
        (activities["order_date"] <= cutoff + pd.Timedelta(days=60))
    ]

    active_farmer_ids = set(future["customer_id"])

    features["inactive_60d"] = (
        ~features["customer_id"].isin(active_farmer_ids)
    ).astype(int)

    features = features.merge(
        farmers[["customer_id", "city", "loyalty_tier"]],
        on="customer_id",
        how="left"
    )

    X = features[
        [
            "activity_count",
            "avg_activity_value",
            "days_since_last_activity",
            "city",
            "loyalty_tier"
        ]
    ]

    y = features["inactive_60d"]

    if y.nunique() < 2 or len(features) < 20:
        raise SystemExit(
            "Not enough class diversity for a model. Check the data."
        )

    numeric = [
        "activity_count",
        "avg_activity_value",
        "days_since_last_activity"
    ]

    categorical = ["city", "loyalty_tier"]

    preprocessing = ColumnTransformer([
        (
            "num",
            Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
                ("scale", StandardScaler())
            ]),
            numeric
        ),
        (
            "cat",
            Pipeline([
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("onehot", OneHotEncoder(handle_unknown="ignore"))
            ]),
            categorical
        )
    ])

    model = Pipeline([
        ("prep", preprocessing),
        (
            "clf",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced"
            )
        )
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y
    )

    model.fit(X_train, y_train)

    probabilities = model.predict_proba(X_test)[:, 1]
    predictions = (probabilities >= 0.5).astype(int)

    OUT.mkdir(exist_ok=True)
    MODEL.parent.mkdir(exist_ok=True)

    report = classification_report(
        y_test,
        predictions,
        zero_division=0
    )

    auc = roc_auc_score(y_test, probabilities)

    report_text = (
        "Smart Agriculture Farmer Inactivity Model\n"
        "Educational baseline - synthetic data only\n\n"
        + report
        + f"\nROC-AUC: {auc:.3f}\n"
    )

    (OUT / "farmer_inactivity_report.txt").write_text(
        report_text,
        encoding="utf-8"
    )

    joblib.dump(model, MODEL)

    print(report_text)
    print(f"Saved model: {MODEL}")


if __name__ == "__main__":
    main()

