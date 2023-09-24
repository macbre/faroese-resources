#!/usr/bin/env python3
# News in English from Kringvarp Føroya (534 subpages)
# https://kvf.fo/forsida/english

import json
import logging
import re
from typing import Iterable, Optional

from shared import get_http_client

BASE_URL = 'https://kvf.fo/'

def get_news_urls() -> Iterable[str]:
    logger = logging.getLogger('get_news_urls')
    page = 0

    while True:
        # curl 'https://kvf.fo/views/ajax' -X POST --data-raw 'page=12&view_name=english_news&view_display_id=block_9'
        resp = get_http_client().post(f'{BASE_URL}/views/ajax', data={
            'page': page,
            'view_name': 'english_news',
            'view_display_id': 'block_9',
        })

        logger.info(f'Page #{page}, got HTTP {resp.status_code}')

        resp.raise_for_status()
        parsed = json.loads(resp.text)

        # now, parse the HTML content looking for links
        # <div class="views-field views-field-title">        <span class="field-content"><a href="/greinar/2023/08/31/nuns-stop-next-summer">
        html = parsed[1]['data']

        for match in re.finditer(r'<div class="views-field views-field-title">\s+<span class="field-content"><a href="([^"]+)">', html, re.IGNORECASE):
            # e.g. /greinar/2023/08/31/nuns-stop-next-summer
            yield f'{BASE_URL}{match.group(1).lstrip("/")}'

        # no more data
        if 'field-content' not in html:
            logger.info('No more pages to iterate over')
            break

        # next page
        page += 1


# https://kvf.fo/greinar/2020/01/20/hackers-came-close-paralysing-faroese-internet
def get_news_content(url: str) -> Optional[str]:
    logger = logging.getLogger('get_news_urls')

    resp = get_http_client().get(url)
    resp.raise_for_status()

    html = resp.text

    # <meta property="og:title" content="Hackers nearly paralysed all Faroese websites" />
    title = re.search(r'<meta property="og:title" content="([^"]+)" />', html)
    # <meta property="og:description" content="All activity on Faroese websites narrowly escaped a complete shutdown in 2018 when domain administrator was hacked" />
    lead = re.search(r'<meta property="og:description" content="([^"]+)" />', html) or ('','')

    # <div class="field-item even" property="content:encoded">
    # ...
    # </div>
    START_MARKER = '<div class="field-item even" property="content:encoded">'
    END_MARKER = '</div>'

    content = html[ html.find(START_MARKER) + len(START_MARKER) : ]
    content = content[ : content.find(END_MARKER) ]

    try:
        logger.info(f'{title[1]} <{url}>')

        return f'<h1>{title[1]}</h1>\n<h2>{lead[1]}</h2>\n<address>{url}</address>\n\n{content}'
    except Exception:
        raise

def main():
    with open('kvf.html', mode='wt') as fp:
        fp.writelines([
            '<title>News in English from Kringvarp Føroya</title>'
            '<body>'
        ])

        for url in get_news_urls():
            fp.write(get_news_content(url) + "\n\n")

        fp.writelines([
            '</body>'
        ])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

    # print(get_news_content('https://kvf.fo/greinar/2020/01/20/hackers-came-close-paralysing-faroese-internet'))
    # print(get_news_content('https://kvf.fo/greinar/2023/08/07/half-all-electricity-comes-renewable-sources'))
