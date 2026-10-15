"""Streamlit dashboard for the Selenium scraping project."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA_PATH = Path("data/cleaned/quotes_clean.csv")

st.set_page_config(page_title="Quote Scraping Dashboard", layout="wide")

st.title("Quote Scraping Dashboard")
st.write(
    "This dashboard displays quote data collected with Selenium from a JavaScript-rendered website. "
    "Use the filters to explore authors, tags, quote length, and page-level patterns."
)

@st.cache_data
def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        st.error("Cleaned data file not found. Run `python scraper.py` then `python clean_data.py` first.")
        st.stop()
    return pd.read_csv(DATA_PATH)


df = load_data()

st.sidebar.header("Filters")
author_options = sorted(df["author"].dropna().unique().tolist())
selected_authors = st.sidebar.multiselect("Choose author(s)", author_options, default=author_options[:5])

length_options = sorted(df["quote_length_group"].dropna().unique().tolist())
selected_lengths = st.sidebar.multiselect("Choose quote length group(s)", length_options, default=length_options)

min_words = int(df["word_count"].min())
max_words = int(df["word_count"].max())
word_range = st.sidebar.slider("Word count range", min_words, max_words, (min_words, max_words))

filtered = df[
    (df["author"].isin(selected_authors))
    & (df["quote_length_group"].isin(selected_lengths))
    & (df["word_count"].between(word_range[0], word_range[1]))
]

st.subheader("Dashboard Summary")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Quotes", len(filtered))
col2.metric("Authors", filtered["author"].nunique())
col3.metric("Avg. Words", round(filtered["word_count"].mean(), 1) if len(filtered) else 0)
col4.metric("Avg. Tags", round(filtered["tag_count"].mean(), 1) if len(filtered) else 0)

st.subheader("Filtered Data Preview")
st.dataframe(filtered, use_container_width=True)

# Visualization 1
st.subheader("Visualization 1: Top Authors by Quote Count")
author_counts = (
    filtered.groupby("author")
    .size()
    .reset_index(name="quote_count")
    .sort_values("quote_count", ascending=False)
    .head(10)
)
fig1 = px.bar(
    author_counts,
    x="author",
    y="quote_count",
    title="Top Authors by Number of Quotes",
    labels={"author": "Author", "quote_count": "Quote Count"},
)
st.plotly_chart(fig1, use_container_width=True)

# Visualization 2
st.subheader("Visualization 2: Quote Length Distribution")
fig2 = px.histogram(
    filtered,
    x="word_count",
    nbins=15,
    title="Distribution of Quote Word Counts",
    labels={"word_count": "Word Count"},
)
st.plotly_chart(fig2, use_container_width=True)

# Visualization 3
st.subheader("Visualization 3: Average Word Count by Length Group")
length_summary = (
    filtered.groupby("quote_length_group", as_index=False)["word_count"]
    .mean()
    .sort_values("word_count")
)
fig3 = px.bar(
    length_summary,
    x="quote_length_group",
    y="word_count",
    title="Average Word Count by Quote Length Group",
    labels={"quote_length_group": "Length Group", "word_count": "Average Word Count"},
)
st.plotly_chart(fig3, use_container_width=True)

# Visualization 4
st.subheader("Visualization 4: Quotes Collected by Page")
page_counts = filtered.groupby("page").size().reset_index(name="quote_count")
fig4 = px.line(
    page_counts,
    x="page",
    y="quote_count",
    markers=True,
    title="Quotes Scraped by Page",
    labels={"page": "Page Number", "quote_count": "Quote Count"},
)
st.plotly_chart(fig4, use_container_width=True)

st.subheader("Key Insights")
st.write(
    "1. Some authors appear more often than others, which affects the distribution of the scraped dataset."
)
st.write(
    "2. Quote length varies across the dataset, so grouping by word count helps make the text easier to compare."
)
st.write(
    "3. Tags and length groups help transform raw scraped text into useful features for analysis."
)
