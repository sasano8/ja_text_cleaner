import pytest
from bs4 import BeautifulSoup

from ja_text_cleaner.normalizer import normalize_html

content = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>test</title>
  </head>
  <body>{text}</body>
</html>
"""


def get_text(text):
    html = content.format(text=text)
    soup = BeautifulSoup(html, "html.parser")
    text = soup.select_one("body").text
    return text


tests = [
    ("　", "\u3000"),
    ("　", "　"),
    ("&nbsp", "\xa0"),
    ("&nbsp", "\u00a0"),
    ("&ensp", "\u2002"),
]


@pytest.mark.parametrize("text, expected", tests)
def test_text(text, expected):
    assert get_text(text) == expected


@pytest.mark.parametrize("text, expected", tests)
def test_normalize_html(text, expected):
    inner_text = get_text(text)
    assert normalize_html(inner_text) == " "
