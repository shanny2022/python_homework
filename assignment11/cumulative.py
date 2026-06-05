"""Calculate cumulative totals for Assignment 11.

Run with:
    python cumulative.py
"""

from __future__ import annotations


def cumulative_totals(values: list[float]) -> list[float]:
    """Return a running total for each value in the provided list."""
    totals = []
    running_total = 0.0

    for value in values:
        running_total += value
        totals.append(round(running_total, 2))

    return totals


def main() -> None:
    weekly_sales = [1250.50, 1410.25, 1325.00, 1588.75, 1664.40, 1722.10]
    totals = cumulative_totals(weekly_sales)

    print("Weekly Sales Cumulative Totals")
    print("------------------------------")
    for week_number, (sales, total) in enumerate(zip(weekly_sales, totals), start=1):
        print(f"Week {week_number}: sales=${sales:,.2f}, cumulative=${total:,.2f}")


if __name__ == "__main__":
    main()
