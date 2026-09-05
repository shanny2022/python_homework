# Final rubric review

## Assignment 11 Tasks 1–5

Implemented in https://github.com/shanny2022/python-assignment11/pull/1.
SQL joins and employee revenue, Pandas bar/line charts, the cumulative column,
float wind strength, HTML export, reflection, and committed files were checked.
Static PNG outputs were visually inspected. Desktop plot-window display and
wind HTML hover/zoom checks still need a browser/desktop verification pass.

## Quotes scraping capstone

| Criterion | Evidence / remaining work |
| --- | --- |
| Selenium, missing tags, pagination, user-agent | Implemented in scraper.py; pagination waits for previous-page elements to become stale. Live scrape not verified in this update. |
| Structured raw output and deduplication | Supplied CSV/JSON preserved; scraper deduplicates quote-author pairs and rejects empty exports. |
| Pandas cleaning and before/after | clean_data.py and database tests; malformed numeric input works with pinned Pandas 3. |
| Features and transformations | Tag count, word count, quote length, length groups, and multi-tag flag recomputed. |
| SQLite persistence | Included database with 12 raw and 12 cleaned records; integrity and repeat-run checks pass. |
| Three interactive visualizations | Author bar chart, length histogram, and average words by length group. |
| Responsive filters | Streamlit tests cover author, tag, word count, and empty selections. |
| Layout and guidance | Columns, sidebar, titles, descriptions, empty-state guidance, and dataset limitations implemented; deployed rendering confirmed in user-supplied screenshots. |
| Reproducible setup | All direct dependencies pinned in requirements.txt; Python 3.13. |
| README screenshot | Three user-supplied screenshots of the deployed dashboard are embedded in README.md. |
| Public deployment | User supplied https://pythonhomework-xvaggbmkepo3ciy3pjkymj.streamlit.app/; recorded in service_urls.txt. User screenshots confirm deployed rendering. Independent signed-out access and live interaction checks remain pending. |

## Kaggle notebook

The previously supplied diabetes notebook is a separate deliverable. Its original
local attachment path was no longer available during this review, and no diabetes
CSV has been supplied. The earlier code inspection showed multiple features,
aggregations, and charts, but these do not by themselves verify the rubric.
Before submission, rerun with the actual CSV and address:

- Replace first-file selection (`csv_files[0]`) with explicit dataset selection
  and required-column validation.
- Validate missing/malformed values before features; missing BMI must not be
  classified as obesity.
- Use the cleaned analysis data consistently; Week 7's `plot_df = diabetes.copy()`
  returns to the raw data.
- Do not silently treat missing cardiovascular indicators as absence of risk.
- Replace generic or conditional conclusions with at least three specific
  findings supported by the actual output values and charts.
- Include reproducible dependency and dataset instructions.

The notebook and actual dataset are needed to implement and verify those changes.
