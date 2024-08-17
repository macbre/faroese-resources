#!/usr/bin/env python3
"""
This script generates the list URLs to PDF archives of Faroese Dimmalætting (2014-2023)
"""
import json
import logging
from typing import Iterable

from shared import get_http_client

ARCHIVE_INDEX_URL = 'https://www.dimma.fo/api/bladid'
ISSUE_URL_PATTERN = 'https://www.dimma.fo/blad/{slug}'  # e.g. https://www.dimma.fo/blad/2022-044


def get_issues_urls() -> Iterable[str]:
    resp = get_http_client().get(ARCHIVE_INDEX_URL)
    resp.raise_for_status()

    """
    Example item
    {
        "slug": "2023-001",
        "year": 2023,
        "number": 1,
        "thumbnail": "\/assets\/magazines\/8dceee6c-6c8f-4d92-84b1-c5bad3e3ff7c.jpg",
        "free": false
    }
    """
    issues: list[dict] = json.loads(resp.text)

    for issue in issues:
        if issue.get('free') is True:
            logging.info(f"Found issue #{issue['number']}/{issue['year']} ...")
            yield ISSUE_URL_PATTERN.format(**issue)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    for url in get_issues_urls():
        pdf_path = f'./dimma/dimma_{url.split("/")[-1]}.pdf'
        logging.info(f'Fetching {url} to {pdf_path} ...')

        # write to PDF files        
        resp = get_http_client().get(url)
        resp.raise_for_status()

        with open(pdf_path, "wb") as fp:
            fp.write(resp.content)
