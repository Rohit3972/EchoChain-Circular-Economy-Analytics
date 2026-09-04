import pandas as pd
from pathlib import Path


# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Input / Output paths
INPUT_FILE = BASE_DIR / "data" / "raw" / "secondary_market_listings.csv"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "secondary_market_cleaned.csv"


def clean_marketplace_data():
    print("Loading marketplace data...")

    df = pd.read_csv(INPUT_FILE)

    print(f"Original shape: {df.shape}")

    # -----------------------------
    # 1. Remove duplicate listings
    # -----------------------------
    df = df.drop_duplicates(subset=["listing_id"])

    # -----------------------------
    # 2. Clean listed price
    # -----------------------------
    df["listed_price"] = (
        df["listed_price"]
        .astype(str)
        .str.replace("₹", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    df["listed_price"] = pd.to_numeric(
        df["listed_price"],
        errors="coerce"
    )

    # -----------------------------
    # 3. Clean listing date
    # -----------------------------
    df["listing_date"] = pd.to_datetime(
        df["listing_date"],
        errors="coerce"
    )

    # -----------------------------
    # 4. Standardize text columns
    # -----------------------------
    text_columns = [
        "listing_title",
        "condition",
        "seller",
        "marketplace"
    ]

    for column in text_columns:
        df[column] = df[column].astype(str).str.strip()

    # -----------------------------
    # 5. Remove invalid records
    # -----------------------------
    df = df.dropna(
        subset=[
            "listing_id",
            "listing_title",
            "listed_price",
            "listing_date"
        ]
    )

    # -----------------------------
    # 6. Save cleaned dataset
    # -----------------------------
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"Cleaned shape: {df.shape}")
    print(f"Saved to: {OUTPUT_FILE}")

    print("\nCleaning completed successfully!")
    print("\nPreview:")
    print(df.head())


if __name__ == "__main__":
    clean_marketplace_data()