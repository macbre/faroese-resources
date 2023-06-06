#!/usr/bin/env python3
import dataclasses
import json
import re
from dataclasses import dataclass
from os import path
from typing import Optional

import requests
import logging


class HttpSession:
    USER_AGENT = 'faroese-resources/frodskaparrit scrapper'
    _session = None

    @classmethod
    def session(cls) -> requests.Session:
        if cls._session is None:
            logging.info(f'Starting the HTTP session with the user-agent {cls.USER_AGENT} ...')
            cls._session = requests.session()
            cls._session.headers['user-agent'] = cls.USER_AGENT

        return cls._session

    @staticmethod
    def get(url, **kwargs) -> requests.Response:
        resp = HttpSession.session().get(url, **kwargs)
        resp.raise_for_status()

        return resp


def get_links(pattern: str, content: str):
    for match in re.finditer(pattern, string=content):
        yield (
            str(match.group(1)),
            str(match.group(2)).strip()
        )


def get_match(pattern: str, content: str) -> Optional[str]:
    match = re.search(pattern, content)

    if match is None:
        return None

    return match.group(1).strip()


def issues(url: str):
    """
    Yields a collection of URLs to the issues
    e.g. https://ojs.setur.fo/index.php/frit/issue/view/35
    """
    logger = logging.getLogger(name='issues')
    page = 1

    while True:
        logger.info(f'Scraping page #{page}')
        resp = HttpSession.get(f'{url}/{page}')

        # No more results
        if '<a class="cover"' not in resp.text:
            return

        # <a class="cover" href="https://ojs.setur.fo/index.php/frit/issue/view/73">Book 43</a>
        for issue, label in get_links(r'<a class="title" href="([^"]+issue/view/\d+)">([^<]+)</a>', content=resp.text):
            logger.info(f'Found "{label}" <{issue}>')
            yield issue

        page += 1


@dataclass
class Article:
    title: str
    url: str
    pdf: str
    author: str
    abstract: str
    published: str


def articles(issue_url: str):
    """
    Yields a collection of Article dataclass from a given issue
    e.g. https://ojs.setur.fo/index.php/frit/issue/view/47
    """
    # 		<h3 class="media-heading">
    # 			<a href="https://ojs.setur.fo/index.php/frit/article/view/416">
    # 				Die Präteritopräsentien im Färoischen
    # 			</a>
    # 		</h3>
    logger = logging.getLogger(name='articles')
    resp = HttpSession.get(issue_url)

    for article_url, article_title in get_links(r'<a href="([^"]+/article/view/\d+)">([^<]+)</a>', content=resp.text):
        logger.info(f'Found "{article_url}" <{article_title}>')

        # parse the article page, e.g. https://ojs.setur.fo/index.php/frit/article/view/561
        article = HttpSession.get(article_url)

        # <meta name="citation_pdf_url" content="https://ojs.setur.fo/index.php/frit/article/download/561/625"/>
        pdf = get_match(r'<meta name="citation_pdf_url" content="([^"]+)"/>', article.text)

        # <meta name="DC.Creator.PersonalName" content="Garth N. Foster"/>
        # <meta name="DC.Date.created" scheme="ISO8601" content="2004-12-31"/>
        author = get_match(r'<meta name="DC.Creator.PersonalName" content="([^"]+)"/>', article.text)
        published = get_match(r'<meta name="DC.Date.created" scheme="ISO8601" content="([^"]+)"/>', article.text)

        # <meta name="DC.Description" xml:lang="en" content="..."/>
        abstract = get_match(r'<meta name="DC.Description" xml:lang="en" content="([^"]+)"/>', article.text)

        yield Article(
            title=article_title,
            url=article_url,
            pdf=pdf,
            author=author,
            abstract=abstract,
            published=published
        )


def scrape():
    logger = logging.getLogger(name='scrape')
    logger.info('Starting')

    items: list[Article] = []

    for issue in issues(url='https://ojs.setur.fo/index.php/frit/issue/archive'):
        for article in articles(issue):
            logger.info(f'Article: {article.title} by {article.author} published on {article.published}')
            items.append(article)

        # return items

    logger.info(f'Done, {len(items)} articles found')
    return items


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    articles = scrape()

    # were to store the articles
    filepath = path.join(
        path.abspath(path.dirname(__file__)),
        'articles.json'
    )

    # save it
    with open(filepath, mode='wt') as fp:
        logging.info(f'Saving articles to {filepath} ...')
        json.dump([dataclasses.asdict(article) for article in articles], fp, indent=2)

    logging.info(f'Done')
