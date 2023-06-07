#!/usr/bin/env python3
import dataclasses
import json
import logging

from os import path

from scrape import articles


def scrape():
    return articles(issue_url='https://ojs.setur.fo/index.php/frodskapur')


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
