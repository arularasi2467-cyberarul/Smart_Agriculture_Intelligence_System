from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "generated"
OUT = ROOT / "outputs"


def triage(message):
    text = str(message).lower()

    if any(k in text for k in [
        "disease", "crop disease", "leaf", "pest",
        "insect", "fungus", "yellow leaves"
    ]):
        return "crop_disease", "high", "consult_agriculture_expert"

    if any(k in text for k in [
        "irrigation", "water", "pump", "drip",
        "canal", "dry field", "watering"
    ]):
        return "irrigation_issue", "high", "check_irrigation_system"

    if any(k in text for k in [
        "seed", "seeds", "sowing", "seed quality",
        "germination"
    ]):
        return "seed_request", "medium", "provide_seed_information"

    if any(k in text for k in [
        "fertilizer", "fertiliser", "manure",
        "compost", "urea", "nutrient"
    ]):
        return "fertilizer_query", "medium", "provide_fertilizer_guidance"

    if any(k in text for k in [
        "payment", "upi", "charged", "money"
    ]):
        return "payment_issue", "high", "human_review"

    return "other", "normal", "ask_clarifying_question"


def main():
    path = DATA / "tickets.csv"

    if not path.exists():
        raise SystemExit(
            "Run python -m src.generate_data first."
        )

    df = pd.read_csv(path)

    result = df["message"].apply(triage)

    df[
        [
            "predicted_category",
            "priority",
            "recommended_action"
        ]
    ] = pd.DataFrame(result.tolist(), index=df.index)

    OUT.mkdir(exist_ok=True)

    output_path = OUT / "farmer_complaint_triage_results.csv"

    df.to_csv(output_path, index=False)

    print("Smart Agriculture Complaint Classification")
    print("\nFirst 10 farmer complaints:\n")

    print(
        df[
            [
                "ticket_id",
                "predicted_category",
                "priority",
                "recommended_action"
            ]
        ].head(10).to_string(index=False)
    )

    print(f"\nSaved: {output_path}")


if __name__ == "__main__":
    main()
