"""
zameen_scraper.py
=================
Scrapes fresh Islamabad house listings from Zameen.com.
Saves results to data/raw/islamabad_fresh.csv in the same
column format expected by ml/preprocess.py.
 
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

# ── Config ────────────────────────────────────────────────────────────────────
OUTPUT_PATH  = os.path.join("data", "raw", "islamabad_fresh.csv")
BASE_URL     = "https://www.zameen.com/Houses_Property/Islamabad-3-{page}.html"
MAX_PAGES    = 40          # 40 pages × ~24 listings = ~960 listings
DELAY_MIN    = 2.5         # min seconds between page requests (be polite)
DELAY_MAX    = 5.0         # max seconds between page requests

os.makedirs(os.path.join("data", "raw"), exist_ok=True)


# ── Setup Selenium Chrome driver ──────────────────────────────────────────────
def create_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--headless=new")          # run without opening browser window
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

    # Mask webdriver detection
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    return driver


# ── Extract listings from a single page ──────────────────────────────────────
def scrape_page(driver: webdriver.Chrome, page: int) -> list[dict]:
    url = BASE_URL.format(page=page)
    listings = []

    try:
        driver.get(url)

        # Wait for listing cards to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "li[aria-label='Listing']")
            )
        )
    except TimeoutException:
        print(f"      [!] Page {page} timed out or no listings found — skipping.")
        return listings

    cards = driver.find_elements(By.CSS_SELECTOR, "li[aria-label='Listing']")

    for card in cards:
        try:
            record = {}

            # ── Price ─────────────────────────────────────────
            try:
                price_el = card.find_element(By.CSS_SELECTOR, "span[aria-label='Price']")
                record["price"] = price_el.text.strip()
            except NoSuchElementException:
                record["price"] = None

            # ── Location ──────────────────────────────────────
            try:
                loc_el = card.find_element(By.CSS_SELECTOR, "div[aria-label='Location']")
                loc_text = loc_el.text.strip().split("\n")
                # Format: "Area Name\nIslamabad"
                record["location"]      = loc_text[0] if len(loc_text) > 0 else None
                record["location_city"] = loc_text[1] if len(loc_text) > 1 else "Islamabad"
            except NoSuchElementException:
                record["location"]      = None
                record["location_city"] = "Islamabad"

            # ── Area / Size ───────────────────────────────────
            try:
                area_el = card.find_element(By.CSS_SELECTOR, "span[aria-label='Area']")
                record["area"] = area_el.text.strip()
            except NoSuchElementException:
                record["area"] = None

            # ── Bedrooms ──────────────────────────────────────
            try:
                bed_el = card.find_element(By.CSS_SELECTOR, "span[aria-label='Beds']")
                record["bedroom"] = bed_el.text.strip()
            except NoSuchElementException:
                record["bedroom"] = "-"

            # ── Bathrooms ─────────────────────────────────────
            try:
                bath_el = card.find_element(By.CSS_SELECTOR, "span[aria-label='Baths']")
                record["bath"] = bath_el.text.strip()
            except NoSuchElementException:
                record["bath"] = "-"

            # ── Property type (fixed — we only scrape Houses) ─
            record["type"]    = "House"
            record["purpose"] = "For Sale"
            record["added"]   = "scraped 2025"
            record["url"]     = ""

            # Only keep if price and area are present
            if record["price"] and record["area"]:
                listings.append(record)

        except Exception:
            continue

    return listings


# ── Main scraper ──────────────────────────────────────────────────────────────
def scrape():
    print("=" * 55)
    print("  Zameen.com Islamabad Scraper — 2025")
    print("=" * 55)
    print(f"\n  Target : Houses for sale in Islamabad")
    print(f"  Pages  : 1 – {MAX_PAGES}")
    print(f"  Output : {OUTPUT_PATH}")
    print(f"\n  Starting browser...\n")

    driver     = create_driver()
    all_data   = []
    empty_pages = 0

    try:
        for page in range(1, MAX_PAGES + 1):
            print(f"  Scraping page {page}/{MAX_PAGES}...", end=" ", flush=True)

            listings = scrape_page(driver, page)

            if not listings:
                empty_pages += 1
                print("0 listings")
                if empty_pages >= 3:
                    print("\n  [!] 3 consecutive empty pages — stopping early.")
                    break
                continue

            empty_pages = 0
            all_data.extend(listings)
            print(f"{len(listings)} listings collected  (total: {len(all_data)})")

            # Save progress every 5 pages in case of crash
            if page % 5 == 0:
                _save(all_data, OUTPUT_PATH)
                print(f"      [✓] Progress saved — {len(all_data)} rows so far")

            # Polite delay between requests
            time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))

    except KeyboardInterrupt:
        print("\n\n  [!] Interrupted by user — saving collected data...")

    finally:
        driver.quit()

    # ── Final save ────────────────────────────────────────────
    _save(all_data, OUTPUT_PATH)

    print("\n" + "=" * 55)
    print("  SCRAPING COMPLETE")
    print("=" * 55)
    print(f"  Total listings collected : {len(all_data)}")
    print(f"  Saved to                 : {OUTPUT_PATH}")
    print("\n  Next steps:")
    print("  1. Open ml/preprocess.py")
    print(f'     Change RAW_PATH to: "data/raw/islamabad_fresh.csv"')
    print("  2. Run: python ml/preprocess.py")
    print("  3. Run: python ml/train.py")
    print("  4. Restart the API — predictions now use 2025 prices!")
    print("=" * 55)


def _save(data: list, path: str):
    if not data:
        return
    df = pd.DataFrame(data)
    # Ensure column order matches what preprocess.py expects
    cols = ["url", "type", "purpose", "area", "bedroom", "bath", "added", "price", "location", "location_city"]
    for col in cols:
        if col not in df.columns:
            df[col] = None
    df = df[cols]
    df.to_csv(path, index=False)


if __name__ == "__main__":
    scrape()