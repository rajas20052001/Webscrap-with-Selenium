"""Scrape paginated table data from a CCIL India web page using Selenium.

Usage:
    python webscraping_selenium.py --pages 3 --output output.json
"""
import argparse
import json
import logging
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

URL = "https://www.ccilindia.com/OMMWSG.aspx"
TIMEOUT = 15  # seconds

# Pagination links sit in row 27 of the results table. Update these locators
# if the site layout changes.
PAGER_XPATH = "/html/body/form/table[5]/tbody/tr[1]/td/table/tbody/tr[27]/td/a[{index}]"
# Index of the <tr> / <td> that holds the data block on each page.
DATA_ROW_INDEX = 5

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)


def build_driver(headless: bool) -> webdriver.Chrome:
    """Create a Chrome driver. Selenium 4.6+ downloads the driver automatically."""
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=options)


def extract_page_data(driver: webdriver.Chrome) -> str:
    """Return the text of the data block on the current page."""
    rows = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "tr"))
    )
    return rows[DATA_ROW_INDEX].find_elements(By.TAG_NAME, "td")[0].text


def go_to_next_page(driver: webdriver.Chrome, pager_index: int) -> bool:
    """Click the pager link at `pager_index`. Return False if it is not found."""
    try:
        link = WebDriverWait(driver, TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, PAGER_XPATH.format(index=pager_index)))
        )
    except (TimeoutException, NoSuchElementException):
        return False
    link.click()
    return True


def scrape(pages: int, headless: bool) -> dict[str, str]:
    data: dict[str, str] = {}
    driver = build_driver(headless)
    try:
        driver.get(URL)
        for page in range(1, pages + 1):
            log.info("Scraping page %d of %d", page, pages)
            data[f"page_{page}"] = extract_page_data(driver)
            if page < pages and not go_to_next_page(driver, pager_index=page):
                log.warning("No next-page link after page %d; stopping.", page)
                break
    finally:
        driver.quit()
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pages", type=int, default=3, help="Number of pages to scrape")
    parser.add_argument("--output", type=Path, default=Path("output.json"))
    parser.add_argument("--headless", action="store_true", help="Run without a browser window")
    args = parser.parse_args()

    results = scrape(args.pages, args.headless)
    args.output.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    log.info("Saved %d page(s) to %s", len(results), args.output)


if __name__ == "__main__":
    main()
