from typing import Literal

import jaconv
import romkan

from .abc import Normalizer


class Tokenizer(Normalizer):
    """読みがなを取得する。与えられたテキストは形態素解析され元の情報は失われる。また、再実行を実行すると文脈が更に分解されてしまうので、再実行は推奨しない。"""

    mode: Literal["A", "B", "C"] = "C"
    sudachi = None
    _mode = None

    part_of_speech = [
        "名詞",
        "代名詞",
        "形状詞",
        "連体詞",
        "副詞",
        "接続詞",
        "感動詞",
        "動詞",
        "形容詞",
        "助動詞",
        "助詞",
        "接頭辞",
        "接尾辞",
        "記号",
        "補助記号",
        "空白",
    ]

    def __init_subclass__(cls) -> None:
        if Tokenizer.sudachi is None:
            Tokenizer.init(Tokenizer.mode)

        # TODO: 小クラスの時はモードに応じたインスタンスを生成させる
        parent = cls.__mro__[1]
        cls.init(cls.mode, parent.sudachi)

    @classmethod
    def init(cls, mode: Literal["A", "B", "C"], dic=None):
        from sudachipy import dictionary, tokenizer

        if not mode in {"A", "B", "C"}:
            raise ValueError(mode)
        _mode = getattr(tokenizer.Tokenizer.SplitMode, mode)

        if dic is None:
            dic = dictionary.Dictionary().create()

        cls.mode = mode
        cls.sudachi = dic
        cls._mode = _mode

    @classmethod
    def process(cls, v: str):
        raise NotImplementedError()

    @classmethod
    def surface(cls, text):
        tokens = cls.sudachi.tokenize(text, cls._mode)

        for t in (x for x in tokens if x.part_of_speech()[0] not in {"空白", "補助記号"}):
            yield t.surface()

    @classmethod
    def reading_form(cls, text):
        tokens = cls.sudachi.tokenize(text, cls._mode)

        for t in (x for x in tokens if x.part_of_speech()[0] not in {"空白", "補助記号"}):
            if not (v := t.reading_form()):
                # 読みが存在しない場合はromkanでカタカナへの変換を試みる　例： tarou
                v = romkan.to_katakana(t.surface())
            else:
                # カタカナでなく英数字が返ることがあるので変換する　例： shi
                v = romkan.to_katakana(v)

            # 半角カタカナを全角にしておく
            # 辞書に読みが存在しない場合、半角カタカナが混じり、romkan.to_hepburnが反応しなくなるため
            v = jaconv.h2z(v, ignore="", kana=True, ascii=False, digit=False)
            yield v


class Wakachi(Tokenizer):
    """分かち書きされた文を返す"""

    @classmethod
    def process(cls, v: str):
        return "　".join(cls.surface(v))


class Katakana(Tokenizer):
    """全角カタカナを返す"""

    @classmethod
    def process(cls, v: str):
        return "　".join(cls.reading_form(v))


class Hiragana(Tokenizer):
    """全角ひらがなを返す"""

    @classmethod
    def process(cls, v: str):
        v = "　".join(cls.reading_form(v))
        # v = jaconv.kata2hira(v, ignore="")  # 半角カタカナに反応しないため、事前に半角は処理しておく
        v = romkan.to_hepburn(v)
        v = romkan.to_hiragana(v)  # ローマ字からしか反応しない
        # v = re.sub(" +", "　", v)
        return v


class Romaji(Tokenizer):
    """半角ローマ字を返す"""

    @classmethod
    def process(cls, v: str):
        v = " ".join(cls.reading_form(v))
        # v = romaji_converter.do(v)
        v = romkan.to_hepburn(v)
        # v = re.sub(" +", " ", v)  # 名字をわけた時スペースが重複する時があるので削除
        return v
