
from pathlib import Path
import random
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "generated"
OUT.mkdir(parents=True, exist_ok=True)

random.seed(42)
np.random.seed(42)


def main():
    # 1. Generate farmer profile data
    n_farmers = 300

    farmers = pd.DataFrame({
        "customer_id": [
            f"F{i:04d}" for i in range(1, n_farmers + 1)
        ],
        "city": np.random.choice(
            ["Coimbatore", "Madurai", "Thanjavur",
             "Salem", "Trichy", "Erode"],
            n_farmers
        ),
        "signup_date": pd.to_datetime(
            np.random.choice(
                pd.date_range("2023-01-01", "2025-12-31"),
                n_farmers
            )
        ).strftime("%Y-%m-%d"),
        "loyalty_tier": np.random.choice(
            ["small_farm", "medium_farm", "large_farm"],
            n_farmers,
            p=[0.50, 0.35, 0.15]
        ),
    })

    # 2. Generate farm activity and crop sales data
    farm_activities = []

    crops = [
        "Rice", "Wheat", "Sugarcane",
        "Cotton", "Maize", "Vegetables"
    ]

    for i in range(1, 1801):
        farmer_id = f"F{random.randint(1, n_farmers):04d}"

        activity_date = (
            pd.Timestamp("2025-01-01")
            + pd.Timedelta(days=random.randint(0, 364))
        )

        farm_activities.append({
            "order_id": f"A{i:05d}",
            "customer_id": farmer_id,
            "order_date": activity_date.strftime("%Y-%m-%d"),
            "order_value": round(
                max(80, np.random.gamma(3.0, 180.0)), 2
            ),
            "status": random.choices(
                ["sold", "cancelled", "returned"],
                [0.88, 0.08, 0.04]
            )[0],
            "items_count": random.randint(1, 15),
            "crop_type": random.choice(crops)
        })

    farm_activities = pd.DataFrame(farm_activities)

    # 3. Generate farmer support complaints
    categories = [
        "crop_disease",
        "irrigation_issue",
        "seed_request",
        "fertilizer_query",
        "payment_issue",
        "other"
    ]

    messages = {
        "crop_disease":
            "My crop is damaged and affected by a disease.",
        "irrigation_issue":
            "Water supply and irrigation are not working properly.",
        "seed_request":
            "I need information about good quality seeds.",
        "fertilizer_query":
            "I need help choosing fertilizer for my crops.",
        "payment_issue":
            "I was charged but my agriculture payment is unclear.",
        "other":
            "I need help with my farming activities."
    }

    tickets = []

    for i in range(1, 501):
        category = random.choice(categories)

        tickets.append({
            "ticket_id": f"T{i:05d}",
            "customer_id": f"F{random.randint(1, n_farmers):04d}",
            "created_at": (
                pd.Timestamp("2025-01-01")
                + pd.Timedelta(days=random.randint(0, 364))
            ).strftime("%Y-%m-%d"),
            "category": category,
            "message": messages[category],
            "status": random.choice(
                ["open", "open", "in_progress", "closed"]
            )
        })

    # 4. Save farmer data
    farmers.to_csv(OUT / "customers.csv", index=False)

    # 5. Save farm activity data
    farm_activities.to_csv(OUT / "orders.csv", index=False)

    # 6. Save farmer complaints
    pd.DataFrame(tickets).to_csv(
        OUT / "tickets.csv", index=False
    )

    # 7. Create agriculture demo policy
    policy_text = (
        "Demo Agriculture Policy (fictional practice content only). "
        "Farmers should verify crop disease symptoms before applying "
        "pesticides or other treatments. "
        "Irrigation problems should be checked by a qualified agriculture "
        "or water management expert. "
        "Seed and fertilizer selection should consider crop type and "
        "local soil conditions. "
        "Government scheme eligibility must be verified through official "
        "government sources. "
        "Financial benefit requests require document verification and "
        "human review. This is not an official government policy.\n"
    )

    (OUT / "refund_policy.txt").write_text(
        policy_text,
        encoding="utf-8"
    )

    print("Smart Agriculture demo data created successfully!")
    print(f"Farmers: {len(farmers)}")
    print(f"Farm activities: {len(farm_activities)}")
    print(f"Farmer complaints: {len(tickets)}")
    print(f"Files saved in: {OUT}")


if __name__ == "__main__":
    main()
