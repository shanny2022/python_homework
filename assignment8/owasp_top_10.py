# Assignment 8 - Task 6

import csv
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://owasp.org/www-project-top-ten/"
OUT = Path(__file__).resolve().parent / "owasp_top_10.csv"

def build_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options
    )

def main():
    driver = build_driver()
    results = []
    try:
        driver.get(URL)
        links = driver.find_elements(
            By.XPATH,
            "//a[starts-with(normalize-space(.),'A01') or "
            "starts-with(normalize-space(.),'A02') or "
            "starts-with(normalize-space(.),'A03') or "
            "starts-with(normalize-space(.),'A04') or "
            "starts-with(normalize-space(.),'A05') or "
            "starts-with(normalize-space(.),'A06') or "
            "starts-with(normalize-space(.),'A07') or "
            "starts-with(normalize-space(.),'A08') or "
            "starts-with(normalize-space(.),'A09') or "
            "starts-with(normalize-space(.),'A10')]"
        )

        seen = set()
        for link in links:
            title = link.text.strip()
            href = link.get_attribute("href")
            if not title or not href:
                continue
            key = title[:3]
            if key in seen:
                continue
            seen.add(key)
            results.append({"Title": title, "Link": href})

        results.sort(key=lambda x: x["Title"][:3])
        results = results[:10]
        print(results)

        with open(OUT, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["Title", "Link"])
            writer.writeheader()
            writer.writerows(results)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
