import pytest
from pydantic import BaseModel

from ja_text_cleaner import name, normalizer, tokenizer


class MyType(BaseModel):
    str_normalize: normalizer.Cleanup
    str_normalize_trim: normalizer.Strip
    str_finalize_japanize: name.Zenkaku


def test_normalizer():
    s = " \t\na\xa0b\u3000"
    data = MyType(
        str_normalize=s,
        str_normalize_trim=s,
        str_finalize_japanize=s,
    )

    assert type(data.str_normalize) is normalizer.Cleanup

    assert data.str_normalize == "   a b "
    assert data.str_normalize_trim == "a\xa0b"
    assert data.str_finalize_japanize == "ａ\u3000ｂ"

    assert normalizer.Cleanup(s) == "   a b "
    assert normalizer.Strip(s) == "a\xa0b"
    assert name.Zenkaku(s) == "ａ\u3000ｂ"
    assert name.Romaji(" 山田\u3000\xa0太郎 ") == "yamada tarou"
    assert name.Hiragana(" 山田\u3000\xa0太郎 ") == "やまだ　たろう"
    assert name.Katakana(" 山田\u3000\xa0太郎 ") == "ヤマダ　タロウ"

    assert (
        normalizer.NormalizeControlCharacter(" \t\na\xa0b\u3000!、,$") == "   a b !、,$"
    )

    # s = normalizer.NormalizeControlCharacter(" \t\na\xa0b\u3000")
    # assert s == 1


def test_normalizer_none():
    s = None
    with pytest.raises(Exception) as e:
        data = MyType(
            str_normalize=s,
            str_normalize_trim=s,
            str_finalize_japanize=s,
        )

    assert len(e.value.errors()) == 3

    assert normalizer.Cleanup(None) == ""
    assert normalizer.Strip(None) == ""
    assert name.Zenkaku(None) == ""


@pytest.mark.parametrize(
    "text, wakachi, zenkaku,  katakana, hiragana, romaji",
    [
        (" \t\n\xa0\u3000-!_", "", "", "", "", ""),
        ("神", "神", "神", "カミ", "かみ", "kami"),  # cjk互換漢字
        (
            "abc123あいうアイウｱｲｳ(日本)!-",
            "abc　123　あ　いう　アイウｱｲｳ　日本",
            "ａｂｃ　１２３　あ　いう　アイウアイウ　日本",
            "エービーシー　イチニサン　ア　イウ　アイウアイウ　ニッポン",
            "えーびーしー　いちにさん　あ　いう　あいうあいう　にっぽん",
            "e-bi-shi- ichinisan a iu aiuaiu nippon",
        ),
        ("日本太郎", "日本　太郎", "日本　太郎", "ニッポン　タロウ", "にっぽん　たろう", "nippon tarou"),
        ("日本 太郎", "日本　太郎", "日本　太郎", "ニッポン　タロウ", "にっぽん　たろう", "nippon tarou"),
        (
            "abc株式会社",
            "abc　株式会社",
            "ａｂｃ　株式会社",
            "エービーシー　カブシキガイシャ",
            "えーびーしー　かぶしきがいしゃ",
            "e-bi-shi- kabushikigaisha",
        ),
        (
            "abc 株式会社",
            "abc　株式会社",
            "ａｂｃ　株式会社",
            "エービーシー　カブシキガイシャ",
            "えーびーしー　かぶしきがいしゃ",
            "e-bi-shi- kabushikigaisha",
        ),
        ("伊藤", "伊藤", "伊藤", "イトウ", "いとう", "itou"),
        (
            "nippon tarou",
            "nippon　tarou",
            "ｎｉｐｐｏｎ　ｔａｒｏｕ",
            "ニッポン　タロウ",
            "にっぽん　たろう",
            "nippon tarou",
        ),
        (
            "e-bi-shi-",
            "e　bi　shi",
            "ｅ　ｂｉ　ｓｈｉ",
            "エ　ビ　シ",
            "え　び　し",
            "e bi shi",
        ),  # ローマ字の表現が乏しいため残念な結果になる
        (
            "エービーシー",
            "エービーシー",
            "エービーシー",
            "エービーシー",
            "えーびーしー",
            "e-bi-shi-",
        ),  # ローマ字の表現が乏しいため残念な結果になる
        (
            "永田町１丁目７−１",
            "永田町　１　丁目　７　１",
            "永田町　１　丁目　７　１",
            "ナガタチョウ　イチ　チョウメ　ナナ　イチ",
            "ながたちょう　いち　ちょうめ　なな　いち",
            "nagatachou ichi choume nana ichi",
        ),
        (
            "永田町一丁目七−一",
            "永田町　一　丁目　七　一",
            "永田町　一　丁目　七　一",
            "ナガタチョウ　イチ　チョウメ　ナナ　イチ",
            "ながたちょう　いち　ちょうめ　なな　いち",
            "nagatachou ichi choume nana ichi",
        ),
    ],
)
def test_reading_form(text, wakachi, zenkaku, katakana, hiragana, romaji):
    assert tokenizer.Katakana(text) == katakana
    assert tokenizer.Hiragana(text) == hiragana
    assert tokenizer.Romaji(text) == romaji
    assert name.Wakachi(text) == wakachi
    assert name.Zenkaku(text) == zenkaku
    assert name.Katakana(text) == katakana
    assert name.Hiragana(text) == hiragana
    assert name.Romaji(text) == romaji

    assert tokenizer.Katakana(katakana) == katakana
    assert tokenizer.Hiragana(katakana) == hiragana
    assert tokenizer.Romaji(katakana) == romaji

    # 再実行は形態素解析によりわかち書きが変わってしまうのでNG
    # assert normalizer.Katakana(hiragana) == katakana
    # assert normalizer.Hiragana(hiragana) == hiragana
    # assert normalizer.Romaji(hiragana) == romaji
