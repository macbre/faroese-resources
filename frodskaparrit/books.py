#!/usr/bin/env python3
import dataclasses
import json
import logging

from os import path
from typing import Iterable

from scrape import get_links, HttpSession, get_match, Article


def articles(issue_root_url: str) -> Iterable[Article]:
    """
    Yields a collection of Article dataclass from a given issue
    e.g. https://ojs.setur.fo/index.php/frit/issue/view/47
    """
    # <h2 class="media-heading">
    # 			<a class="title" href="https://ojs.setur.fo/index.php/frodskapur/issue/view/175">
    # 									For the common good
    # 							</a>
    # 							<div class="series lead">
    # 					2023<br>
    # 					2025-08-29
    # 				</div>
    # 					</h2>
    logger = logging.getLogger(name='articles')
    page = 1

    while page <= 4:
        logging.info(f'Scraping page #{page} ...')
        resp = HttpSession.get(f'{issue_root_url}/{page}')

        for issue_url, article_title in get_links(r'<a[^>]+href="([^"]+/issue/view/\d+)">([^<]+)</a>', content=resp.text):
            # parse the article page, e.g. https://ojs.setur.fo/index.php/frit/article/view/561
            issue = HttpSession.get(issue_url)

            # follow the link to the article page
            # <a href="https://ojs.setur.fo/index.php/frodskapur/article/view/874">
            # 				For the Common Good
            # 			</a>
            article_url = get_match(r'<a[^>]+href="([^"]+/article/view/\d+)">', issue.text)
            article = HttpSession.get(article_url)

            # <meta name="citation_pdf_url" content="https://ojs.setur.fo/index.php/frodskapur/article/download/192/868"/>
            pdf = get_match(r'<meta name="citation_pdf_url" content="([^"]+)"/>', article.text)

            # <meta name="DC.Creator.PersonalName" content="Garth N. Foster"/>
            # <meta name="DC.Date.created" scheme="ISO8601" content="2004-12-31"/>
            # <meta name="DC.Title" content="For the Common Good: In Memory of Jóannes Jacobsen"/>
            author = get_match(r'<meta name="DC.Creator.PersonalName" content="([^"]+)"/>', article.text)
            published = get_match(r'<meta name="DC.Date.created" scheme="ISO8601" content="([^"]+)"/>', article.text)
            article_title = get_match(r'<meta name="DC.Title" content="([^"]+)"/>', article.text)

            # <meta name="DC.Description" xml:lang="en" content="..."/>
            abstract = get_match(r'<meta name="DC.Description" xml:lang="en" content="([^"]+)"/>', article.text)

            logger.info(f'Found "{issue_url}" <{article_title}>')

            yield Article(
                title=article_title,
                url=article_url,
                pdf=pdf,
                author=author,
                abstract=abstract,
                published=published
            )

        # next page?
        # <a class="next" href="https://ojs.setur.fo/index.php/frodskapur/issue/archive/3">Next</a>
        # if not 'class="next"' in resp.text:
        #     break
        page += 1


def scrape():
    return articles(issue_root_url='https://ojs.setur.fo/index.php/frodskapur/issue/archive')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    books = list(scrape())

    # print out the Markdown syntax listing all the books with the PDF link
    for book in books:
        if book.pdf is not None:
            print(f'* [{book.title}]({book.pdf}) by {book.author}')

    # were to store the books
    filepath = path.join(
        path.abspath(path.dirname(__file__)),
        'books.json'
    )

    # save it
    with open(filepath, mode='wt') as fp:
        logging.info(f'Saving books to {filepath} ...')
        json.dump([dataclasses.asdict(book) for book in books], fp, indent=2)

    logging.info(f'Done')
