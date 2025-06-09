"""Example script to scrape Korean case law.

This script demonstrates how one might collect case texts from a website and
save them to ``data/legal_cases.jsonl`` for model training.
It uses the ``requests`` and ``BeautifulSoup`` packages.

Note: This is a simplified example and does not handle website terms of service
or robust error checking. Always review and respect the target site's policies
before scraping.
"""

import json
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://example.com/cases"  # Placeholder URL


def fetch_case_list():
    """Fetch a list of case URLs from the site."""
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    links = [a["href"] for a in soup.select("a.case-link")]
    return links


def fetch_case_text(url: str) -> dict:
    """Fetch case text and citation from a case detail page."""
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.select_one("div.case-text").get_text(strip=True)
    citation = soup.select_one("span.citation").get_text(strip=True)
    return {"text": text, "citation": citation}


def main():
    cases = []
    for url in fetch_case_list():
        case = fetch_case_text(url)
        cases.append(case)

    with open("data/legal_cases.jsonl", "w", encoding="utf-8") as f:
        for idx, case in enumerate(cases, 1):
            entry = {"id": idx, **case}
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
