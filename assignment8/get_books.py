from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import json
for book in books:
    try:
        title = book.find_element(By.CSS_SELECTOR, "TITLE_SELECTOR").text

        authors = book.find_elements(By.CSS_SELECTOR, "AUTHOR_SELECTOR")
        author_names = [a.text for a in authors]
        author = "; ".join(author_names)

        format_year = book.find_element(By.CSS_SELECTOR, "FORMAT_SELECTOR").text

        results.append({
            "Title": title,
            "Author": author,
            "Format-Year": format_year
        })

    except:
        continue
