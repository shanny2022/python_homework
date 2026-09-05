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

## Assignment 10 Task 5 — SQLite database

This update uses the 12 quote records supplied in `selenium_scraping_project.zip`.
No fresh scrape was performed and the supplied page numbers and attributions
have not been independently verified. The raw CSV and JSON are preserved.

From this project folder, run:

```bash
python capstone_database.py
python -m unittest -v test_database.py
```

Only Pandas is required for the database pipeline. The database script also works
when invoked by its path from the homework repository root.
It loads the raw CSV with Pandas, prints before/after cleaning information,
regenerates `data/cleaned/quotes_clean.csv`, and imports every CSV under `data/`
into a separate SQLite table named after its filename. Blank quotes and duplicate
quote-author pairs are removed, missing authors become `Unknown`, tag counts are
recomputed from tags, and invalid page numbers remain missing. Quote lengths,
word counts, multiple-tag flags, and length groups are recomputed from the text.
This corrects inaccurate derived values in the supplied cleaned CSV.

The included `db/capstone_data.db` contains:

| Table | Rows | Columns |
| --- | ---: | ---: |
| quotes_raw | 12 | 5 |
| quotes_clean | 12 | 9 |

Numeric counts use SQLite INTEGER, text uses TEXT, missing values use NULL,
and boolean flags use 0/1. Each run builds and verifies a temporary database
before replacing the project database, so reruns do not append duplicate rows
and failed imports preserve the previous database. This output is dedicated to
this pipeline; rebuilding replaces all its tables.

Example SQL:

```sql
SELECT author, COUNT(*) AS quote_count, AVG(word_count) AS average_words
FROM quotes_clean
GROUP BY author
ORDER BY quote_count DESC, author;

SELECT * FROM quotes_clean LIMIT 5;
PRAGMA integrity_check;
```

Validation: three automated tests passed for the supplied data and repeat runs,
missing/malformed/duplicate fixture records, recomputed features, and database
preservation when an import fails. The Streamlit dashboard still reads the
regenerated clean CSV; running or deploying the dashboard is separate from this
database update.
