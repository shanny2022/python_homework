"""Create an interactive wind-speed chart as wind.html.

Run with:
    python wind.py
"""

from __future__ import annotations

from pathlib import Path


WIND_DATA = [
    {"month": "Jan", "speed_mph": 11.2, "gust_mph": 22.5},
    {"month": "Feb", "speed_mph": 12.8, "gust_mph": 25.1},
    {"month": "Mar", "speed_mph": 14.3, "gust_mph": 29.4},
    {"month": "Apr", "speed_mph": 13.6, "gust_mph": 27.2},
    {"month": "May", "speed_mph": 10.9, "gust_mph": 20.8},
    {"month": "Jun", "speed_mph": 9.7, "gust_mph": 18.4},
    {"month": "Jul", "speed_mph": 8.5, "gust_mph": 16.9},
    {"month": "Aug", "speed_mph": 8.9, "gust_mph": 17.5},
    {"month": "Sep", "speed_mph": 10.4, "gust_mph": 21.0},
    {"month": "Oct", "speed_mph": 11.7, "gust_mph": 23.6},
    {"month": "Nov", "speed_mph": 12.1, "gust_mph": 24.3},
    {"month": "Dec", "speed_mph": 11.5, "gust_mph": 22.9},
]


def build_chart(output_path: Path) -> None:
    """Build the Plotly chart and save it as an HTML file."""
    try:
        import plotly.graph_objects as go
    except ImportError as exc:
        raise SystemExit(
            "Plotly is required for wind.py. Install it with: pip install plotly"
        ) from exc

    months = [row["month"] for row in WIND_DATA]
    speeds = [row["speed_mph"] for row in WIND_DATA]
    gusts = [row["gust_mph"] for row in WIND_DATA]

    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=months,
            y=speeds,
            mode="lines+markers",
            name="Average wind speed",
            line={"color": "#1f77b4", "width": 3},
        )
    )
    figure.add_trace(
        go.Bar(
            x=months,
            y=gusts,
            name="Peak gust",
            marker_color="#ff7f0e",
            opacity=0.55,
        )
    )
    figure.update_layout(
        title="Monthly Wind Speed and Peak Gusts",
        xaxis_title="Month",
        yaxis_title="Miles per hour",
        template="plotly_white",
        hovermode="x unified",
    )
    figure.write_html(output_path, include_plotlyjs="cdn")


def main() -> None:
    output_path = Path(__file__).with_name("wind.html")
    build_chart(output_path)
    print(f"Created {output_path}")


if __name__ == "__main__":
    main()
