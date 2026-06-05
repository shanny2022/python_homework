"""Clean and transform the raw quote data scraped with Selenium."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

RAW_CSV = Path("data/raw/quotes_raw.csv")
CLEAN_DIR = Path("data/cleaned")
CLEAN_CSV = CLEAN_DIR / "quotes_clean.csv"


def clean_quotes() -> pd.DataFrame:
    """Load raw data, clean it, transform it, and save clean CSV."""
    if not RAW_CSV.exists():
        raise FileNotFoundError(
            "Missing data/raw/quotes_raw.csv. Run `python scraper.py` first."
        )

    raw_df = pd.read_csv(RAW_CSV)
    print("Before cleaning:")
    print(raw_df.info())
    print(raw_df.head())

    df = raw_df.copy()

    # Clean missing and malformed entries.
    df["quote"] = df["quote"].fillna("").astype(str).str.strip()
    df["author"] = df["author"].fillna("Unknown").astype(str).str.strip()
    df["tags"] = df["tags"].fillna("").astype(str).str.strip()
    df["tag_count"] = pd.to_numeric(df["tag_count"], errors="coerce").fillna(0).astype(int)
    df["page"] = pd.to_numeric(df["page"], errors="coerce").fillna(0).astype(int)

    # Remove empty quotes and duplicate records.
    df = df[df["quote"] != ""]
    df = df.drop_duplicates(subset=["quote", "author"])

    # Transformations / extracted features.
    df["quote_length"] = df["quote"].str.len()
    df["word_count"] = df["quote"].str.replace("“", "", regex=False).str.replace("”", "", regex=False).str.split().str.len()
    df["has_multiple_tags"] = df["tag_count"] > 1

    def length_group(word_count: int) -> str:
        if word_count < 10:
            return "Short"
        if word_count <= 20:
            return "Medium"
        return "Long"

    df["quote_length_group"] = df["word_count"].apply(length_group)

    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_CSV, index=False)

    print("\nAfter cleaning:")
    print(df.info())
    print(df.head())
    print(f"Saved cleaned data to {CLEAN_CSV}")

    return df


if __name__ == "__main__":
    clean_quotes()
