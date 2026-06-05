# Selenium Scraping Final Project

## Project Summary

This project uses Selenium to scrape quote data from a JavaScript-rendered practice website, cleans the data with Pandas, and displays the results in an interactive Streamlit dashboard.

Website used: `https://quotes.toscrape.com/js/`

The project demonstrates:

- Selenium web scraping
- Handling pagination
- Handling missing tags safely
- Avoiding duplicate records
- Saving raw data as CSV and JSON
- Cleaning and transforming data with Pandas
- Creating extracted features
- Building an interactive Streamlit dashboard
- Creating 3+ Plotly visualizations

## Files

- `scraper.py` — Scrapes quote data using Selenium
- `clean_data.py` — Cleans and transforms raw scraped data
- `app.py` — Streamlit dashboard with interactive filters and charts
- `requirements.txt` — Python dependencies
- `data/raw/quotes_raw.csv` — Raw scraped CSV output
- `data/raw/quotes_raw.json` — Raw scraped JSON output
- `data/cleaned/quotes_clean.csv` — Cleaned dataset used by the dashboard

## Setup Instructions

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the scraper:

```bash
python scraper.py
```

3. Clean the data:

```bash
python clean_data.py
```

4. Run the dashboard:

```bash
streamlit run app.py
```

## Dashboard Features

The dashboard allows users to:

- Filter by author
- Filter by quote length group
- Filter by word count range
- View summary metrics
- View cleaned data
- Explore charts interactively

## Visualizations Included

1. Top authors by quote count
2. Quote word count distribution
3. Average word count by quote length group
4. Quotes collected by page

## Data Cleaning and Transformation

The cleaning process includes:

- Filling missing author values
- Cleaning extra whitespace
- Converting numeric fields to proper types
- Removing empty quote rows
- Removing duplicate quote-author pairs
- Creating extracted features:
  - `quote_length`
  - `word_count`
  - `has_multiple_tags`
  - `quote_length_group`

## Screenshot

Add a screenshot of your Streamlit dashboard here before submitting.

Example:

```markdown
![Dashboard Screenshot](images/dashboard_screenshot.png)
```

## Project Reflection

This project helped me practice the full data workflow: collecting web data, saving raw output, cleaning and transforming data, and building an interactive dashboard. I also practiced using Selenium for JavaScript-rendered pages and Streamlit for user-friendly data exploration.
