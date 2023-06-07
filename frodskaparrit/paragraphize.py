#!/usr/bin/env python3
# This script takes the text input on stdin and emits the paragraphed text.
#
# Example:
# Three out of four police
# officers at the station
# were hospitalized, but no
# one was seriously hurt.
#
# will become:
# Three out of four police officers at the station were hospitalized, but no  one was seriously hurt.
#
# Usage:
#  $ cat /tmp/text | ./paragraphize.py > /tmp/out.txt
#  $ cat /tmp/text | ./paragraphize.py --html > /tmp/out.html
#
import logging

from sys import stdin, stdout, argv
from typing import Iterable


def paragraphize(text_input: Iterable[str]):
    current_paragraph = ''

    for line in text_input:
        line = line.strip()
        current_paragraph += line + ' '

        # end the current paragraph and yield it
        if line.endswith('.'):
            yield current_paragraph.strip()
            current_paragraph = ''

    # anything left?
    if current_paragraph != '':
        yield current_paragraph.strip()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(name='paragraphize')

    logger.debug('Got CLI arguments: ' + repr(argv))
    use_html = '--html' in argv

    for output in paragraphize(text_input=stdin):
        if use_html is True:
            stdout.write(f'<p>{output}</p>\n')
        else:
            stdout.write(output + '\n')
