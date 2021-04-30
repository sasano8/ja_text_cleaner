from bs4 import BeautifulSoup

from ja_text_cleaner import build_trans, mappings

mapping = build_trans("A", mappings.blank, mappings.tab, mappings.newline)

content = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
  </head>
  <body>{text}</body>
</html>
"""


def get_text(text):
    html = content.format(text=text)
    soup = BeautifulSoup(html, "html.parser")
    text = soup.select_one("body").text
    return text


def translate_html(text):
    text = get_text(text)
    return text.translate(mapping)


def translate_str(text):
    return text.translate(mapping)


def test_spec():
    assert "　" == "\u3000"
    dic = {"　": 0, "\u3000": 1}
    assert len(dic) == 1
    assert dic["　"] == 1
    assert dic["\u3000"] == 1


def test_text():
    assert translate_str("") == ""
    assert translate_str(" ") == "A"
    assert translate_str("　") == "A"
    assert translate_str("\u3000") == "A"
    assert translate_str("&nbsp") == "&nbsp"
    # assert translate_str("&ensp") == "&ensp"
    # assert translate_str("&emsp") == "&emsp"
    # assert translate_str("&emsp13") == "&emsp13"
    assert translate_str("\t") == "A"
    assert translate_str("\n") == "A"
    assert translate_str("\r") == "A"
    assert translate_str("\r\n\n") == "AAA"


def test_html():
    assert translate_html("") == ""
    assert translate_html(" ") == "A"
    assert translate_html("　") == "A"
    assert translate_html("\u3000") == "A"
    assert translate_html("&nbsp") == "A"
    assert translate_html("&ensp") == "A"
    assert translate_html("&emsp") == "A"
    # assert translate_html("&emsp13") == "A"
    # assert translate_html("&emsp14") == "A"
    assert translate_html("&#x2006") == "A"
    # assert translate_html("&numsp") == "A"
    # assert translate_html("&puncsp") == "A"
    assert translate_html("&thinsp") == "A"
    # assert translate_html("&hairsp") == "A"
    # assert translate_html("&NegativeMediumSpace") == "A"
    assert translate_html("&#xFEFF") == "A"

    assert translate_html("\t") == "A"
    assert translate_html("\n") == "A"
    assert translate_html("\r") == "A"
    assert translate_html("\r\n\n") == "A"  # beautiful soupで連続した改行は１つにまとめる模様
