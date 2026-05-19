from pathlib import Path
import csv

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


PROJECT_URL = "https://owasp.org/www-project-top-ten/"
OUTPUT_FILE = Path(__file__).parent / "owasp_top_10.csv"


def build_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    return webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options,
    )


def main():
    driver = build_driver()
    vulnerabilities = []

    try:
        # Task 6: Use Selenium to read the OWASP Top Ten project page.
        driver.get(PROJECT_URL)
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Task 6: Use XPath to follow the current released Top Ten page.
        current_release = driver.find_element(
            By.XPATH,
            "//a[contains(., 'OWASP Top Ten') and contains(., '2025')]",
        )
        top_ten_url = current_release.get_attribute("href")
        driver.get(top_ten_url)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Task 6: Find the ordered list after the Top 10 heading and extract the links.
        top_ten_links = driver.find_elements(
            By.XPATH,
            "//h3[contains(., 'Top 10')]/following-sibling::ol[1]//a[starts-with(normalize-space(.), 'A')]",
        )

        for link in top_ten_links:
            title = " ".join(link.text.split())
            href = link.get_attribute("href")
            if title and href:
                vulnerabilities.append({"Title": title, "Link": href})

    except TimeoutException:
        print("Timed out waiting for the OWASP page to load.")
    finally:
        driver.quit()

    print(vulnerabilities)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["Title", "Link"])
        writer.writeheader()
        writer.writerows(vulnerabilities)

    print(f"Saved {len(vulnerabilities)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
