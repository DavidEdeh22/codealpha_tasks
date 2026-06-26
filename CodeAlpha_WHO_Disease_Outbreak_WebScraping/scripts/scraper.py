"""
=========================================================
WHO Disease Outbreak News Web Scraper
=========================================================

Author: David Edeh
Project: CodeAlpha Data Analytics Internship
Repository:
    CodeAlpha_WHO_Disease_Outbreak_WebScraping

Description
-----------
This script scrapes Disease Outbreak News reports from the
World Health Organization (WHO) website.

The scraper:

• Uses Selenium to render JavaScript content
• Parses rendered HTML using BeautifulSoup
• Automatically navigates through all pages
• Collects reports between 2020 and 2025
• Cleans and validates the data
• Exports results to CSV
• Generates logs
• Handles exceptions gracefully

Author:
David Edeh

Created:
2026

=========================================================
"""

# ============================================
# Standard Python Libraries
# ============================================

import logging
import time
import sys
from pathlib import Path
from datetime import datetime

# ============================================
# Third-party Libraries
# ============================================

import pandas as pd

from bs4 import BeautifulSoup

from tqdm import tqdm

from selenium import webdriver

from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
    NoSuchElementException
)

# ============================================
# PROJECT CONFIGURATION
# ============================================

BASE_URL = "https://www.who.int/emergencies/disease-outbreak-news"

START_YEAR = 2020

END_YEAR = 2025

OUTPUT_DIRECTORY = Path("data")

OUTPUT_FILE = OUTPUT_DIRECTORY / "who_outbreak_reports.csv"

LOG_DIRECTORY = Path("outputs")

LOG_FILE = LOG_DIRECTORY / "scraping.log"

WAIT_TIME = 20

PAGE_LOAD_DELAY = 3

HEADLESS_MODE = False

REPORT_SELECTOR = "a.sf-list-vertical__item"

OUTPUT_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)

LOG_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_FILE,
            encoding="utf-8"
        ),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def print_banner():
    """
    Prints project banner.
    """

    print("\n")

    print("=" * 65)

    print("WHO DISEASE OUTBREAK NEWS SCRAPER")

    print("=" * 65)

    print(f"Start Year : {START_YEAR}")

    print(f"End Year   : {END_YEAR}")

    print("=" * 65)


def initialize_driver():
    """
    Creates and returns a configured Chrome driver.
    """

    logger.info("Initializing Chrome Driver...")

    options = webdriver.ChromeOptions()

    if HEADLESS_MODE:
        options.add_argument("--headless=new")

    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")

    driver = webdriver.Chrome(
        service=Service(
            ChromeDriverManager().install()
        ),
        options=options
    )

    return driver

def wait_for_page(driver):
    """
    Wait until the page
    finishes loading.
    """

    WebDriverWait(
        driver,
        WAIT_TIME
    ).until(
        EC.presence_of_element_located(
            (By.TAG_NAME, "body")
        )
    )

    time.sleep(PAGE_LOAD_DELAY)

def close_driver(driver):
    """
    Closes Selenium safely.
    """

    try:

        driver.quit()

        logger.info("Browser closed.")

    except Exception:

        logger.warning("Unable to close browser.")    

if __name__ == "__main__":

    print_banner()

    logger.info("WHO Scraper Started")


    def open_who_website(driver):
        """
        Opens the WHO Disease Outbreak News page.

        Parameters
        ----------
        driver : webdriver.Chrome

        Returns
        -------
        None
        """

        logger.info("Opening WHO website...")

        driver.get(BASE_URL)

        wait_for_page(driver)

def get_rendered_html(driver):
    """
    Returns the rendered HTML after
    JavaScript execution.

    Parameters
    ----------
    driver : webdriver.Chrome

    Returns
    -------
    str
    """

    logger.info("Capturing rendered HTML...")

    return driver.page_source

def parse_html(html):
    """
    Converts HTML into a BeautifulSoup object.

    Parameters
    ----------
    html : str

    Returns
    -------
    BeautifulSoup
    """

    logger.info("Parsing HTML...")

    return BeautifulSoup(
        html,
        "html.parser"
    )

def get_report_cards(soup):
    """
    Finds all outbreak report cards.

    Parameters
    ----------
    soup : BeautifulSoup

    Returns
    -------
    list
    """

    logger.info("Searching for outbreak reports...")

    reports = soup.select(REPORT_SELECTOR)

    logger.info(f"{len(reports)} reports found.")

    return reports

def safe_extract_text(element):
    """
    Safely extracts text from an HTML element.

    Parameters
    ----------
    element

    Returns
    -------
    str
    """

    if element is None:
        return ""

    return element.get_text(strip=True)

def safe_extract_attribute(
    element,
    attribute
):
    """
    Safely extracts HTML attributes.

    Parameters
    ----------
    element

    attribute : str

    Returns
    -------
    str
    """

    if element is None:
        return ""

    return element.get(attribute, "")

def extract_report(report):
    """
    Extracts information from a single
    outbreak report.

    Parameters
    ----------
    report

    Returns
    -------
    dict
    """
    
    title_container = report.select_one("h4.sf-list-vertical__title")

    title_element = title_container.select_one("span.trimmed")

    report_title = (
        title_element.get_text(strip=True)
        if title_element
        else "Unknown Title"
    )

    spans = title_container.find_all("span")

    publication_date = ""
    
    if len(spans) >= 2:
        publication_date = (
            spans[1]
            .get_text(strip=True)
            .replace("|", "")
            .strip()
        )

    report_url = report.get("href")

    from urllib.parse import urljoin

    report_url = urljoin(BASE_URL, report.get("href"))

    record = {
        "report_title": report_title,
        "publication_date": publication_date,
        "report_url": report_url
    }
    return record

def convert_date(date_text):
    """
    Converts WHO date into datetime.

    Returns
    -------
    datetime
    """

    try:

        return datetime.strptime(
            date_text,
            "%d %B %Y"
        )

    except ValueError:

        logger.warning(
            f"Unable to parse date: {date_text}"
        )

        return None


def enrich_record(record):
    """
    Adds Year and Month columns.
    """

    parsed_date = convert_date(
        record["publication_date"]
    )

    if parsed_date:
        record["year"] = parsed_date.year
        record["month"] = parsed_date.strftime("%B")
    else:
        record["year"] = None
        record["month"] = None

    return record

def is_valid_record(record):
    """
    Checks whether the extracted record
    contains the minimum required fields.
    """

    required_fields = [

        "report_title",

        "publication_date",

        "report_url"

    ]

    for field in required_fields:

        if not record.get(field):

            return False

    return True

def process_page(soup):
    """
    Processes every report on a page.

    Returns
    -------
    list
    """

    reports = get_report_cards(soup)

    page_records = []

    for report in reports:

        record = extract_report(report)

        record = enrich_record(record)

        record["disease"] = extract_disease(record["report_title"])
        record["country"] = extract_country(record["report_title"])

        if is_valid_record(record):

            page_records.append(record)

    logger.info(
        f"{len(page_records)} valid reports extracted."
    )

    return page_records

def get_next_button(driver):
    """
    Returns the pagination Next button.

    Parameters
    ----------
    driver : webdriver.Chrome

    Returns
    -------
    WebElement | None
    """

    try:

        next_button = driver.find_element(
            By.CSS_SELECTOR,
            "a[aria-label='Go to the next page']"
        )

        return next_button

    except NoSuchElementException:

        logger.warning(
            "Next button not found."
        )

        return None
    
def go_to_next_page(driver):
    """
    Navigates to the next page.

    Returns
    -------
    bool
    """

    next_button = get_next_button(driver)

    if next_button is None:

        return False

    try:

        driver.execute_script(
            "arguments[0].click();",
            next_button
        )

        wait_for_page(driver)

        logger.info(
            "Moved to next page."
        )

        return True

    except Exception as error:

        logger.error(error)

        return False   
    
def should_continue(page_records):
    """
    Determines whether scraping
    should continue.

    Returns
    -------
    bool
    """

    if len(page_records) == 0:

        return False

    oldest_year = min(

        record["year"]

        for record in page_records

        if record["year"] is not None

    )

    if oldest_year < START_YEAR:

        logger.info(

            "Reached records older than "
            f"{START_YEAR}."

        )

        return False

    return True

progress = tqdm(

    desc="Scraping Pages",

    unit="page"

)

def scrape_reports(driver):
    """
    Main scraping function.

    Returns
    -------
    list
    """

    all_records = []

    page_number = 1

    progress = tqdm(

        desc="Scraping Pages",

        unit="page"

    )

    while True:

        logger.info(f"Processing page {page_number}...")

        html = get_rendered_html(driver)

        soup = parse_html(html)

        page_records = process_page(soup)

        all_records.extend(page_records)

        progress.update(1)

        if not should_continue(page_records):

            break
        
        success = go_to_next_page(driver)

        if not success:

            break

        page_number += 1

        time.sleep(2)

    progress.close()

    return all_records

MAX_RETRIES = 3

def run_scraper(driver):
    """
    Executes scraper with retries.
    """

    for attempt in range(

        1,

        MAX_RETRIES + 1

    ):

        try:

            logger.info(

                f"Attempt {attempt}"

            )

            return scrape_reports(driver)

        except TimeoutException:

            logger.warning(

                "Timeout occurred."

            )

        except WebDriverException:

            logger.warning(

                "Browser error."

            )

        except Exception as error:

            logger.error(error)

        logger.info(

            "Retrying..."

        )

        time.sleep(5)

    logger.error(

        "Maximum retries reached."

    )

    return []

def extract_disease(title):
    """
    Extract disease from title.
    """

    if "-" in title:

        return title.split("-")[0].strip()

    return title

def extract_country(title):
    """
    Extract country from title.
    """

    if "-" in title:

        return title.split("-")[-1].strip()

    return ""

def create_dataframe(records):
    """
    Converts extracted records into
    a pandas DataFrame.
    """

    logger.info("Creating DataFrame...")

    dataframe = pd.DataFrame(records)

    logger.info(
        f"{len(dataframe)} records loaded."
    )

    return dataframe

def remove_duplicates(dataframe):
    """
    Removes duplicate reports.
    """

    before = len(dataframe)

    dataframe = dataframe.drop_duplicates(
        subset=["report_url"]
    )

    after = len(dataframe)

    logger.info(
        f"Removed {before - after} duplicate records."
    )

    return dataframe

def filter_years(dataframe):
    """
    Filters reports within
    START_YEAR and END_YEAR.
    """

    dataframe = dataframe[
        (dataframe["year"] >= START_YEAR)
        &
        (dataframe["year"] <= END_YEAR)
    ]

    logger.info(
        f"{len(dataframe)} records remain after filtering."
    )

    return dataframe

def sort_dataframe(dataframe):
    """
    Sorts reports by publication date.
    """

    dataframe["publication_date"] = pd.to_datetime(
        dataframe["publication_date"],
        format="%d %B %Y",
        errors="coerce"
    )

    dataframe = dataframe.sort_values(
        by="publication_date",
        ascending=False
    )

    dataframe.reset_index(
        drop=True,
        inplace=True
    )

    dataframe["publication_date"] = dataframe["publication_date"].dt.strftime("%d %B %Y")

    return dataframe

def export_csv(dataframe):
    """
    Saves the dataset to CSV.
    """

    dataframe.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    logger.info(
        f"Dataset exported to {OUTPUT_FILE}"
    )

def print_summary(dataframe):
    """
    Prints project summary.
    """

    print("\n")
    print("=" * 60)
    print("SCRAPING SUMMARY")
    print("=" * 60)

    print(f"Total Reports : {len(dataframe)}")
    print(f"Years Covered : {START_YEAR} - {END_YEAR}")

    print(
        f"Newest Report : "
        f"{dataframe.iloc[0]['publication_date']}"
    )

    print(
        f"Oldest Report : "
        f"{dataframe.iloc[-1]['publication_date']}"
    )

    print(f"CSV Saved To : {OUTPUT_FILE}")

    print("=" * 60)    

def main():
    """
    Main program entry point.
    """

    print_banner()

    driver = None

    try:

        driver = initialize_driver()

        open_who_website(driver)

        records = run_scraper(driver)

        dataframe = create_dataframe(records)

        dataframe = remove_duplicates(dataframe)

        dataframe = filter_years(dataframe)

        dataframe = sort_dataframe(dataframe)

        export_csv(dataframe)

        print_summary(dataframe)

        logger.info("Scraping completed successfully.")

    except Exception as error:

        logger.exception(
            f"Unexpected error: {error}"
        )

    finally:

        if driver:

            close_driver(driver)

if __name__ == "__main__":

    main()