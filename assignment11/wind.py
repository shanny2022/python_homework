"""Assignment 11 Task 3: Plotly wind dataset visualization.

This script loads Plotly's built-in wind dataset, prints the first and last
10 rows, cleans the strength column into a numeric value, and saves an
interactive scatter plot as wind.html.

Run from the assignment11 folder:
    python wind.py
"""

from pathlib import Path

import pandas as pd
import plotly.data as pl
import plotly.express as px


OUTPUT_HTML = Path(__file__).resolve().parent / "wind.html"


def clean_strength(value: str) -> float:
    """Convert wind strength ranges like '0-1' or '6+' into numeric values."""
    text = str(value).strip()

    if "+" in text:
        return float(text.replace("+", ""))

    if "-" in text:
        low, high = text.split("-", 1)
        return (float(low) + float(high)) / 2

    return float(text)


def main() -> None:
    wind_df = pl.wind()

    print("First 10 rows of the Plotly wind dataset:")
    print(wind_df.head(10))

    print("\nLast 10 rows of the Plotly wind dataset:")
    print(wind_df.tail(10))

    wind_df = wind_df.copy()
    wind_df["strength_clean"] = wind_df["strength"].apply(clean_strength)

    print("\nCleaned wind strength values:")
    print(wind_df[["strength", "strength_clean"]].drop_duplicates())

    fig = px.scatter(
        wind_df,
        x="strength_clean",
        y="frequency",
        color="direction",
        hover_data=["direction", "strength", "frequency"],
        title="Wind Strength vs. Frequency by Direction",
        labels={
            "strength_clean": "Wind Strength (cleaned numeric value)",
            "frequency": "Frequency",
            "direction": "Wind Direction",
        },
    )

    fig.update_layout(
        xaxis_title="Wind Strength",
        yaxis_title="Frequency",
        legend_title="Direction",
    )

    fig.write_html(OUTPUT_HTML)
    print(f"\nSaved interactive Plotly chart to {OUTPUT_HTML}")


if __name__ == "__main__":
    main()
