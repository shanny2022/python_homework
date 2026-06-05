from pathlib import Path
import json
import re
from time import sleep

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


SEARCH_URL = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"
OUTPUT_DIR = Path(__file__).parent
CSV_FILE = OUTPUT_DIR / "get_books.csv"
JSON_FILE = OUTPUT_DIR / "get_books.json"


def build_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--user-agent=python-homework-assignment8")
    return webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options,
    )


def first_match(element, selectors):
    for selector in selectors:
        try:
            found = element.find_element(By.CSS_SELECTOR, selector)
            if found.text.strip():
                return found
        except NoSuchElementException:
            continue
    return None


def all_matches(element, selectors):
    matches = []
    for selector in selectors:
        matches = element.find_elements(By.CSS_SELECTOR, selector)
        if matches:
            break
    return matches


def clean_text(text):
    return " ".join(text.split())


def clean_title(text):
    title = clean_text(text)
    title = re.sub(
        r"\s+(eBook|eAudiobook|Book|Picture Book|DVD|Streaming Video|Streaming Music)\b.*$",
        "",
        title,
    )
    title = title.rstrip(" ,")

    for split_at in range(1, len(title) // 2 + 1):
        first_half = title[:split_at].strip()
        second_half = title[split_at:].strip()
        if first_half and first_half == second_half:
            return first_half

    return title


def main():
    driver = build_driver()
    results = []

    try:
        # Task 3: Load the Durham County Library search results page.
        driver.get(SEARCH_URL)

        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))

        # Task 3: Find all li elements in the search result list.
        book_entries = driver.find_elements(
            By.CSS_SELECTOR,
            "li.cp-search-result-item, li[data-test-id*='search-result'], li:has(a[href*='/v2/record/'])",
        )

        if not book_entries:
            book_entries = driver.find_elements(
                By.XPATH,
                "//h3[.//a[contains(@href, '/v2/record/')]]/ancestor::li[1]",
            )

        print(f"Found {len(book_entries)} search results.")

        # Task 3: Loop through each result and extract title, author, and format-year.
        for book in book_entries:
            title_element = first_match(
                book,
                [
                    "a.title-content",
                    "h3 a[href*='/v2/record/']",
                    "a[href*='/v2/record/']",
                ],
            )
            if not title_element:
                continue

            title = clean_title(title_element.text)

            author_elements = all_matches(
                book,
                [
                    "a.author-link",
                    "a[href*='searchType=author']",
                    "a[href*='/v2/search'][href*='author']",
                ],
            )
            author_names = [clean_text(author.text) for author in author_elements if author.text.strip()]
            author = "; ".join(author_names)

            format_year_element = first_match(
                book,
                [
                    ".cp-format-info span",
                    ".cp-format-info",
                    "[data-test-id*='format'] span",
                    "[data-test-id*='format']",
                    "a[href*='/v2/record/'][aria-label*=',']",
                ],
            )
            format_year = clean_text(format_year_element.text) if format_year_element else ""

            if not format_year:
                label = title_element.get_attribute("aria-label") or ""
                parts = [clean_text(part) for part in label.split(",") if part.strip()]
                format_year = ", ".join(parts[-2:]) if len(parts) >= 2 else ""

            results.append(
                {
                    "Title": title,
                    "Author": author,
                    "Format-Year": format_year,
                }
            )

            sleep(0.2)

    except TimeoutException:
        print("Timed out waiting for the library search page to load.")
    finally:
        driver.quit()

    # Task 4: Create a DataFrame, print it, and save CSV and JSON files.
    df = pd.DataFrame(results, columns=["Title", "Author", "Format-Year"])
    print(df)

    df.to_csv(CSV_FILE, index=False)
    with open(JSON_FILE, "w", encoding="utf-8") as json_file:
        json.dump(results, json_file, indent=4)

    print(f"Saved {len(results)} rows to {CSV_FILE}")
    print(f"Saved {len(results)} rows to {JSON_FILE}")


if __name__ == "__main__":
    main()
