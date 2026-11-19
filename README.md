# Web Scraping with Selenium

A Python script that automates Chrome with Selenium to extract paginated table data from a [CCIL India](https://www.ccilindia.com/OMMWSG.aspx) web page and saves it as JSON.

## Features

- Navigates multiple result pages automatically
- Explicit waits instead of fixed `sleep` calls, so it is faster and more reliable
- Command-line options for page count, output file and headless mode
- Selenium Manager handles the ChromeDriver, so no manual driver download is needed
- Clean shutdown of the browser, even when errors occur

## Requirements

- Python 3.9+
- Google Chrome installed

## Setup

```bash
git clone https://github.com/rajas20052001/Webscrap-with-Selenium.git
cd Webscrap-with-Selenium
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
python webscraping_selenium.py --pages 3 --output output.json --headless
```

| Option | Default | Description |
|---|---|---|
| `--pages` | `3` | Number of pages to scrape |
| `--output` | `output.json` | Output file path |
| `--headless` | off | Run Chrome without a visible window |

### Example output

```json
{
  "page_1": "...text of the data block...",
  "page_2": "..."
}
```

## Project structure

```
.
├── webscraping_selenium.py   # Scraper
├── requirements.txt
├── .gitignore
└── README.md
```

## Notes

- The script relies on XPath locators for the page layout. If the site changes, update `PAGER_XPATH` and `DATA_ROW_INDEX` at the top of the script.
- Check the website's terms of use before scraping, and keep request rates low.

## Possible improvements

- Parse the text into structured rows and export to CSV or a database
- Add retry logic and unit tests
- Schedule runs with cron or Task Scheduler

## Author

Rajasekar · [LinkedIn](https://www.linkedin.com/in/rajasekarss/)
