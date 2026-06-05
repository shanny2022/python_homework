"""
Selenium Scraping Project
Scrapes quote data from https://quotes.toscrape.com/js/

This site is designed for scraping practice and includes JavaScript-rendered pages,
which makes it a good Selenium project.
"""

from __future__ import annotations

import csv
import json
import time
from pathlib import Path
from typing import Dict, List, Set

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://quotes.toscrape.com/js/"
RAW_DIR = Path("data/raw")
RAW_JSON = RAW_DIR / "quotes_raw.json"
RAW_CSV = RAW_DIR / "quotes_raw.csv"


def build_driver(headless: bool = True) -> webdriver.Chrome:
    """Create and return a Selenium Chrome driver."""
    chrome_options = Options()

    if headless:
        chrome_options.add_argument("--headless=new")

    # User-agent header to reduce scraping blocks and identify a normal browser request.
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36"
    )
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1400,1000")

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)


def safe_text(parent, selector: str, default: str = "") -> str:
    """Safely extract text from an element. Handles missing tags."""
    try:
        return parent.find_element(By.CSS_SELECTOR, selector).text.strip()
    except NoSuchElementException:
        return default


def scrape_quotes(max_pages: int | None = None, delay: float = 1.0) -> List[Dict[str, str]]:
    """Scrape quotes across paginated JavaScript pages."""
    driver = build_driver(headless=True)
    wait = WebDriverWait(driver, 10)
    results: List[Dict[str, str]] = []
    seen: Set[str] = set()

    try:
        driver.get(BASE_URL)
        page_number = 1

        while True:
            try:
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".quote")))
            except TimeoutException:
                print("No quotes found or page timed out.")
                break

            quote_cards = driver.find_elements(By.CSS_SELECTOR, ".quote")

            for card in quote_cards:
                text = safe_text(card, ".text")
                author = safe_text(card, ".author", "Unknown")
                tag_elements = card.find_elements(By.CSS_SELECTOR, ".tags .tag")
                tags = [tag.text.strip() for tag in tag_elements if tag.text.strip()]

                # Unique key prevents duplicates if a page reloads or repeats.
                unique_key = f"{text}|{author}"
                if unique_key in seen:
                    continue
                seen.add(unique_key)

                results.append(
                    {
                        "quote": text,
                        "author": author,
                        "tags": ", ".join(tags),
                        "tag_count": str(len(tags)),
                        "page": str(page_number),
                    }
                )

            print(f"Scraped page {page_number}: {len(results)} total quotes")

            if max_pages is not None and page_number >= max_pages:
                break

            # Pagination handling: click Next if it exists; stop if it does not.
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "li.next a")
                next_button.click()
                page_number += 1
                time.sleep(delay)  # polite delay to avoid redundant rapid requests
            except NoSuchElementException:
                break

    finally:
        driver.quit()

    return results


def save_outputs(records: List[Dict[str, str]]) -> None:
    """Save raw scraped data to JSON and CSV."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    with RAW_JSON.open("w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    with RAW_CSV.open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["quote", "author", "tags", "tag_count", "page"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"Saved {len(records)} records to {RAW_JSON} and {RAW_CSV}")


if __name__ == "__main__":
    data = scrape_quotes(max_pages=None, delay=1.0)
    save_outputs(data)
