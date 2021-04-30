from typing import Literal

from fastapi import FastAPI

app = FastAPI()


@app.get("/get_normalize_unicodedata")
def normalize_unicodedata(text: str = "ばﾊﾞは゛①1㈱￥、神神"):
    """与えられたunicode文字の正規化結果を返します。
    D: Decomposition(分解)
    K: KはCompatibility(互換性)
    C: Composition(合成)

    合成：
    大文字の「が」など同じようにみえるが、
    「か」＋「゛」の　基底文字＋結合文字表現か、「が」一文字の合成文字表現かなど内部表現が変わる。

    テキスト入力時に、基底文字と゛に分けて入力（結合文字表現）することはまずないため、
    NFKCが一般的なケースに合うことが多い。
    """
    import unicodedata

    strategy = ["NFD", "NFC", "NFKD", "NFKC"]

    result = {}
    for s in strategy:
        data = unicodedata.normalize(s, text)
        hex_data = [f'0x{x.encode("utf-8").hex()}' for x in data]
        result[s] = {data, " ".join(hex_data)}
    return result


@app.get("/test_diff_composition")
def test_diff_composition(text1: str = "フ\u309a", text2: str = "プ"):
    """同じ見た目の文字を与えても、内部表現次第で一致しない"""
    return f"{text1} == {text2}: {text1 == text2}"


@app.get("/test_ヷ")
def test_ヷ(text: str = "ヷ"):
    """ヷはひらがな版の合成文字が存在しない。そのような場合、わ＋結合文字で表現できるが、NFKCで正規化されない。"""
    import unicodedata

    # "\u308F\u3099"
    return unicodedata.normalize("NFKC", text)


@app.get("/test_神")
def test_神と神(text: str = "神と神"):
    """神はCJK互換漢字とされ、ユニコード正規化するとCJK統合漢字の神に変換されてしまう"""
    import unicodedata

    # "\u308F\u3099"
    return unicodedata.normalize("NFC", text)
