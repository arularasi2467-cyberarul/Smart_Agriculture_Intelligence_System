from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "generated" / "refund_policy.txt"


def assess(message, farmer_id=""):
    text = str(message).lower()

    if not farmer_id.strip():
        return {
            "status": "NEEDS_INFO",
            "reason": "Farmer ID is required before reviewing the complaint.",
            "action": "Ask farmer for Farmer ID"
        }

    if any(x in text for x in [
        "disease", "pest", "fungus", "insect",
        "yellow leaves", "crop damage"
    ]):
        return {
            "status": "EXPERT_REVIEW",
            "reason": "Crop disease or pest issue needs expert assessment.",
            "action": "Refer farmer to an agriculture expert"
        }

    if any(x in text for x in [
        "irrigation", "water", "pump", "drip",
        "canal", "dry field"
    ]):
        return {
            "status": "SUPPORT_REQUIRED",
            "reason": "An irrigation-related issue was identified.",
            "action": "Check the irrigation system and water supply"
        }

    if any(x in text for x in [
        "seed", "seeds", "germination", "sowing"
    ]):
        return {
            "status": "GUIDANCE_REQUIRED",
            "reason": "The farmer needs seed-related information.",
            "action": "Provide suitable seed information and refer to local agriculture support"
        }

    if any(x in text for x in [
        "fertilizer", "fertiliser", "manure",
        "compost", "urea", "nutrient"
    ]):
        return {
            "status": "GUIDANCE_REQUIRED",
            "reason": "The farmer needs fertilizer-related information.",
            "action": "Refer to an agriculture expert for soil-based fertilizer guidance"
        }

    if any(x in text for x in [
        "payment", "upi", "charged", "money"
    ]):
        return {
            "status": "ESCALATE",
            "reason": "Payment-related issue requires human review.",
            "action": "Route to the support team"
        }

    return {
        "status": "NOT_ENOUGH_INFORMATION",
        "reason": "The complaint needs more details.",
        "action": "Ask the farmer a clarifying question"
    }


def main():
    if not POLICY.exists():
        raise SystemExit(
            "Run python -m src.generate_data first."
        )

    print("Smart Agriculture Farmer Support Agent")
    print("Demo guidance only - no real service request is submitted.")

    message = input("Farmer complaint: ")
    farmer_id = input("Farmer ID (example: F0001): ")

    print("\nFarmer Support Assessment:")
    print(assess(message, farmer_id))


if __name__ == "__main__":
    main()
