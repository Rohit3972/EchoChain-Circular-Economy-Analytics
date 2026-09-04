import pandas as pd
from pathlib import Path


# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

PRODUCT_FILE = BASE_DIR / "data" / "sample" / "product_master.csv"
MARKETPLACE_FILE = (
    BASE_DIR / "data" / "processed" / "secondary_market_cleaned.csv"
)
OUTPUT_FILE = (
    BASE_DIR / "data" / "processed" / "marketplace_product_matched.csv"
)


def normalize_text(text):
    """Normalize text for matching."""
    return (
        str(text)
        .lower()
        .replace("-", " ")
        .replace("_", " ")
        .strip()
    )


def match_products():

    print("Loading product master...")
    products = pd.read_csv(PRODUCT_FILE)

    print("Loading cleaned marketplace data...")
    listings = pd.read_csv(MARKETPLACE_FILE)

    # Normalize matching fields
    products["model_normalized"] = (
        products["product_model"].apply(normalize_text)
    )

    listings["title_normalized"] = (
        listings["listing_title"].apply(normalize_text)
    )

    matched_rows = []

    for _, listing in listings.iterrows():

        title = listing["title_normalized"]

        # Find product model appearing in marketplace title
        matches = products[
            products["model_normalized"].apply(
                lambda model: model in title
            )
        ]

        if len(matches) > 0:

            product = matches.iloc[0]

            matched_rows.append({
                "listing_id": listing["listing_id"],
                "listing_title": listing["listing_title"],
                "sku_id": product["sku_id"],
                "product_model": product["product_model"],
                "brand": product["brand"],
                "category": product["category"],
                "original_price": product["original_price"],
                "listed_price": listing["listed_price"],
                "condition": listing["condition"],
                "listing_date": listing["listing_date"],
                "marketplace": listing["marketplace"],
                "match_status": "Matched"
            })

        else:

            matched_rows.append({
                "listing_id": listing["listing_id"],
                "listing_title": listing["listing_title"],
                "sku_id": None,
                "product_model": None,
                "brand": None,
                "category": None,
                "original_price": None,
                "listed_price": listing["listed_price"],
                "condition": listing["condition"],
                "listing_date": listing["listing_date"],
                "marketplace": listing["marketplace"],
                "match_status": "Unmatched"
            })

    matched_df = pd.DataFrame(matched_rows)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    matched_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nProduct matching completed!")
    print(f"Total listings: {len(matched_df)}")
    print(
        f"Matched listings: "
        f"{(matched_df['match_status'] == 'Matched').sum()}"
    )
    print(
        f"Unmatched listings: "
        f"{(matched_df['match_status'] == 'Unmatched').sum()}"
    )

    print(f"\nSaved to: {OUTPUT_FILE}")

    print("\nPreview:")
    print(matched_df.head())


if __name__ == "__main__":
    match_products()