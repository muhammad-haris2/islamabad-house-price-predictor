"""
zameen_scraper.py
=================
Scrapes fresh Islamabad property listings from Zameen.com.
Collects Houses and Flats for sale and saves to one CSV file.

Requirements:
    pip install selenium webdriver-manager pandas

Usage:
    python zameen_scraper.py
"""

import os
import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

OUTPUT_PATH = os.path.join("data", "raw", "islamabad_fresh.csv")
DELAY_MIN   = 2.5
DELAY_MAX   = 5.0

# Each entry: (property_type_label, zameen_url_template, max_pages)
TARGETS = [
    ("House", "https://www.zameen.com/Houses_Property/Islamabad-3-{page}.html",     40),
    ("Flat",  "https://www.zameen.com/Flats_Property/Islamabad-3-{page}.html",      25),
]

os.makedirs(os.path.join("data", "raw"), exist_ok=True)


def create_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    service = Service(ChromeDriverManager().install())
    driver  = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver


def scrape_page(driver: webdriver.Chrome, url: str, property_type: str) -> list[dict]:
    listings = []
    try:
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li[aria-label='Listing']"))
        )
    except TimeoutException:
        print(f"      [!] Timed out — skipping.")
        return listings

    for card in driver.find_elements(By.CSS_SELECTOR, "li[aria-label='Listing']"):
        try:
            record = {}

            try:
                record["price"] = card.find_element(By.CSS_SELECTOR, "span[aria-label='Price']").text.strip()
            except NoSuchElementException:
                record["price"] = None

            try:
                loc_text = card.find_element(By.CSS_SELECTOR, "div[aria-label='Location']").text.strip().split("\n")
                record["location"]      = loc_text[0] if loc_text else None
                record["location_city"] = loc_text[1] if len(loc_text) > 1 else "Islamabad"
            except NoSuchElementException:
                record["location"]      = None
                record["location_city"] = "Islamabad"

            try:
                record["area"] = card.find_element(By.CSS_SELECTOR, "span[aria-label='Area']").text.strip()
            except NoSuchElementException:
                record["area"] = None

            try:
                record["bedroom"] = card.find_element(By.CSS_SELECTOR, "span[aria-label='Beds']").text.strip()
            except NoSuchElementException:
                record["bedroom"] = "-"

            try:
                record["bath"] = card.find_element(By.CSS_SELECTOR, "span[aria-label='Baths']").text.strip()
            except NoSuchElementException:
                record["bath"] = "-"

            record["type"]    = property_type
            record["purpose"] = "For Sale"
            record["added"]   = "scraped 2025"
            record["url"]     = ""

            if record["price"] and record["area"]:
                listings.append(record)

        except Exception:
            continue

    return listings


def save(data: list, path: str):
    if not data:
        return
    df   = pd.DataFrame(data)
    cols = ["url", "type", "purpose", "area", "bedroom", "bath", "added", "price", "location", "location_city"]
    for col in cols:
        if col not in df.columns:
            df[col] = None
    df[cols].to_csv(path, index=False)


def scrape():
    print("=" * 55)
    print("  Zameen.com — Islamabad Property Scraper")
    print("=" * 55)
    print(f"  Types  : House, Flat")
    print(f"  Output : {OUTPUT_PATH}\n")

    driver   = create_driver()
    all_data = []

    try:
        for property_type, url_template, max_pages in TARGETS:
            print(f"\n  ── Scraping {property_type}s ──────────────────────")
            empty_pages = 0

            for page in range(1, max_pages + 1):
                url = url_template.format(page=page)
                print(f"  Page {page}/{max_pages}...", end=" ", flush=True)

                listings = scrape_page(driver, url, property_type)

                if not listings:
                    empty_pages += 1
                    print("0 listings")
                    if empty_pages >= 3:
                        print(f"  3 consecutive empty pages — done with {property_type}s.")
                        break
                    continue

                empty_pages = 0
                all_data.extend(listings)
                print(f"{len(listings)} collected  (total: {len(all_data)})")

                if page % 5 == 0:
                    save(all_data, OUTPUT_PATH)
                    print(f"  [✓] Progress saved — {len(all_data)} rows")

                time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))

    except KeyboardInterrupt:
        print("\n  Interrupted — saving collected data...")
    finally:
        driver.quit()

    save(all_data, OUTPUT_PATH)

    # Summary by type
    df = pd.DataFrame(all_data)
    print("\n" + "=" * 55)
    print("  DONE")
    print("=" * 55)
    print(f"  Total collected : {len(all_data)} listings")
    if not df.empty and "type" in df.columns:
        print(f"  By type         :")
        for ptype, count in df["type"].value_counts().items():
            print(f"    {ptype:<12} : {count}")
    print(f"  Saved to        : {OUTPUT_PATH}")
    print("=" * 55)


if __name__ == "__main__":
    scrape()