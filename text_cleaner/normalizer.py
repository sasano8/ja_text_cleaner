import re
import unicodedata

# import jaconv
import mojimoji

# import pykakasi
import romkan

from .abc import Normalizer
from .processor import normalize_html

C = "制御文字"
Z = "区切り空白"
P = "句読点・括弧"
M = "濁点などの結合文字　２バイト文字の２バイト目に格納されている。消去すると文字が変わってしまう"

exclude = {"C", "Z", "P"}


# def get_romaji_converter():
#     kakasi = pykakasi.kakasi()
#     kakasi.setMode("H", "a")  # Hiragana to ascii
#     kakasi.setMode("K", "a")  # Katakana to ascii
#     kakasi.setMode("J", "a")  # Japanese to ascii
#     kakasi.setMode("r", "Hepburn")  # use Hepburn Roman table
#     kakasi.setMode("s", True)  # add space
#     kakasi.setMode("C", False)  # no capitalize
#     return kakasi.getConverter()


# romaji_converter = get_romaji_converter()


# https://www.unicode.org/reports/tr44/#GC_Values_Table
class NormalizeControlCharacter(Normalizer):
    """制御文字と区切り文字（様々な空白等）を一般的な空白に変換する"""

    @classmethod
    def process(cls, v: str):
        v = "".join(
            ch if unicodedata.category(ch)[0] not in {"C", "Z"} else " " for ch in v
        )
        return v

        # return "".join(ch for ch in v if unicodedata.category(ch)[0] not in exclude else " ")


class Cleanup(Normalizer):
    """制御文字(control character)・区切り・空白・改行を半角スペースにする。
    htmlを読み込む場合は、事前にbeautfulsoup等で読み込み、デコード後のテキストを渡してください。
    """

    @classmethod
    def process(cls, v: str):
        return normalize_html(v)


class IgnoreCCBlankSymbol(Normalizer):
    @classmethod
    def process(cls, v: str):
        v = "".join(
            ch if unicodedata.category(ch)[0] not in exclude else " " for ch in v
        )
        return v

        # return " ".join(ch for ch in v if unicodedata.category(ch)[0] not in exclude else " ")


class Strip(Normalizer):
    """両端の空白を削除する"""

    @classmethod
    def process(cls, v: str):
        return v.strip()


class NFKC(Normalizer):
    """結合文字表現を合成文字表現に正規化する。
    加えて、日本語は全角になり、英数字記号は半角に正規化される。
    CJK互換漢字はCJK統合漢字にまとめられてしまうため、そのままの文字を保持したい場合は利用できない。
    基本的に利用するのは、検索のためにインデックスを貼るとき。
    NG例：神　⇛　神
    """

    @classmethod
    def process(cls, v: str):
        # https://qiita.com/fury00812/items/b98a7f9428d1395fc230
        # ["NFD", "NFC", "NFKD", "NFKC"]
        return unicodedata.normalize("NFKC", v)


class Zenkaku(Normalizer):
    """文字を全角にする。日本語の名前や住所の正規化に使用する。
    漢字の正規化は行わない。
    """

    @classmethod
    def process(cls, v: str):
        v = mojimoji.han_to_zen(v, kana=True, ascii=True, digit=True)
        v = re.sub(" +", "　", v)
        return v


class Romaji(Normalizer):
    """半角ローマ字（ヘボン式）を返す。
    変換可能文字種
    半角英字（ヘボン式）：　○
    ひらがな：　○
    全角カタカナ：　○
    全角英字：　☓
    半角カタカナ：　☓
    """

    @classmethod
    def process(cls, v: str):
        v = romkan.to_hepburn(v)
        return v


class Hiragana(Normalizer):
    """ひらがなを返す。
    変換可能文字種
    半角英字（ヘボン式）：　○
    ひらがな：　○
    全角カタカナ：　○
    全角英字：　☓
    半角カタカナ：　☓
    """

    @classmethod
    def process(cls, v: str):
        v = romkan.to_hepburn(v)
        v = romkan.to_hiragana(v)
        return v


class Katakana(Normalizer):
    """全角カタカナを返す。
    変換可能文字種
    半角英字（ヘボン式）：　○
    ひらがな：　○
    全角カタカナ：　○
    全角英字：　☓
    半角カタカナ：　☓
    """

    @classmethod
    def process(cls, v: str):
        v = romkan.to_hepburn(v)
        v = romkan.to_katakana(v)
        return v
