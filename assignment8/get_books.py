# Assignment 8 - Tasks 1-4
# Before running, review https://durhamcountylibrary.org/robots.txt
# and confirm the public search-results page is allowed.

import json
import time
from pathlib import Path
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

SEARCH_URL = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"
HERE = Path(__file__).resolve().parent

def build_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options
    )

def first_elements(parent, selectors):
    for selector in selectors:
        found = parent.find_elements(By.CSS_SELECTOR, selector)
        if found:
            return found
    return []

def first_element(parent, selectors):
    found = first_elements(parent, selectors)
    return found[0] if found else None

def extract_book(item):
    title_el = first_element(item, [
        'a[data-key="bib-title"]',
        'a[data-testid*="title"]',
        'h2 a',
        'h3 a',
        'a[class*="title"]'
    ])
    title = title_el.text.strip() if title_el else ""

    author_els = first_elements(item, [
        'a[data-key="bib-author"]',
        'a[data-testid*="author"]',
        'a[class*="author"]'
    ])
    authors = [el.text.strip() for el in author_els if el.text.strip()]
    author = "; ".join(dict.fromkeys(authors))

    format_container = first_element(item, [
        'div[data-testid*="format"]',
        'div[class*="format"]',
        'div[class*="metadata"]',
        'div[class*="bib-details"]'
    ])
    format_year = ""
    if format_container:
        spans = format_container.find_elements(By.CSS_SELECTOR, "span")
        parts = [s.text.strip() for s in spans if s.text.strip()]
        format_year = " ".join(parts) if parts else format_container.text.strip()

    return {"Title": title, "Author": author, "Format-Year": format_year}

def main():
    driver = build_driver()
    results = []
    try:
        driver.get(SEARCH_URL)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
        )
        time.sleep(2)

        items = first_elements(driver, [
            'li[data-testid*="search-result"]',
            'li[class*="search-result"]',
            'li[class*="SearchResult"]',
            'li[class*="cp-search-result"]'
        ])

        if not items:
            items = driver.find_elements(By.XPATH, "//li[.//h2//a or .//h3//a]")

        print("Search results found:", len(items))

        for item in items:
            book = extract_book(item)
            if book["Title"]:
                results.append(book)

        df = pd.DataFrame(results)
        print(df)

        df.to_csv(HERE / "get_books.csv", index=False)
        with open(HERE / "get_books.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
