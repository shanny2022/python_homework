"""Assignment 11 Task 6: explore the cleaned quotes stored in SQLite."""
from contextlib import closing
from pathlib import Path
import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st

DATABASE = Path(__file__).resolve().parent / "db/capstone_data.db"


def load_data():
    with closing(sqlite3.connect(f"{DATABASE.as_uri()}?mode=ro", uri=True)) as conn:
        return pd.read_sql_query("SELECT * FROM quotes_clean", conn)


def main():
    st.set_page_config(page_title="Quote Explorer", page_icon="📖", layout="wide")
    st.title("Quote Explorer")
    st.write("Explore authors, tags, and quote lengths. Use the sidebar filters to update every chart and the quote table.")
    try:
        df = load_data()
    except (sqlite3.Error, pd.errors.DatabaseError) as error:
        st.error(f"The quote database could not be loaded: {error}")
        st.stop()
    if df.empty:
        st.info("There are no quotes in this dataset yet.")
        st.stop()
    st.caption(f"Source: {len(df)} supplied quote records from the capstone archive. This is a saved snapshot, not a live feed.")
    authors = sorted(df.author.dropna().unique())
    selected = st.sidebar.multiselect("Authors", authors, default=authors)
    tags = sorted({tag.strip() for value in df.tags.fillna("") for tag in value.split(",") if tag.strip()})
    tag = st.sidebar.selectbox("Tag", ["All tags"] + tags)
    low, high = int(df.word_count.min()), int(df.word_count.max())
    bounds = st.sidebar.slider("Word count", low, high, (low, high)) if low < high else (low, high)
    filtered = df[df.author.isin(selected) & df.word_count.between(*bounds)].copy()
    if tag != "All tags":
        mask = filtered.tags.fillna("").apply(lambda value: tag in [part.strip() for part in value.split(",")]).astype(bool)
        filtered = filtered.loc[mask]
    a, b, c = st.columns(3)
    a.metric("Quotes", len(filtered))
    b.metric("Authors", filtered.author.nunique())
    c.metric("Average words", f"{filtered.word_count.mean():.1f}" if len(filtered) else "—")
    if filtered.empty:
        st.info("No quotes match these filters. Select an author or widen your filters.")
        return

    left, right = st.columns(2)
    author_counts = filtered.groupby("author").size().reset_index(name="quote_count")
    author_counts = author_counts.sort_values("quote_count", ascending=False)
    with left:
        st.plotly_chart(px.bar(author_counts, x="author", y="quote_count",
            title="Quotes by author", labels={"author":"Author", "quote_count":"Quotes"}), width="stretch")
    with right:
        st.plotly_chart(px.histogram(filtered, x="word_count", nbins=10,
            title="Distribution of quote lengths", labels={"word_count":"Words per quote"}), width="stretch")
    lengths = filtered.groupby("quote_length_group", as_index=False).word_count.mean()
    st.plotly_chart(px.bar(lengths, x="quote_length_group", y="word_count",
        title="Average words by length group", category_orders={"quote_length_group":["Short","Medium","Long"]},
        labels={"quote_length_group":"Length group", "word_count":"Average words"}), width="stretch")

    st.subheader("What the selection shows")
    top = author_counts.iloc[0]
    st.write(f"{top['author']} is one of the most represented authors in this selection, with {int(top['quote_count'])} quote(s). Quote lengths range from {int(filtered.word_count.min())} to {int(filtered.word_count.max())} words.")
    st.caption("These patterns describe this small supplied collection, not an author's popularity or complete body of work. Page numbers and attributions have not been independently verified.")
    st.subheader("Explore the quotes")
    st.dataframe(filtered[["quote","author","tags","word_count","quote_length_group"]], hide_index=True, width="stretch")
    st.download_button("Download filtered quotes", filtered.to_csv(index=False), "filtered_quotes.csv", "text/csv")


if __name__ == "__main__":
    main()
