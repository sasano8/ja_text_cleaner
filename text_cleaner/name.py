from . import normalizer, tokenizer
from .abc import Finalizer


class Wakachi(Finalizer):

    pipe = [normalizer.Cleanup, tokenizer.Wakachi, normalizer.Strip]


class Zenkaku(Finalizer):
    """制御文字や空白を除去し全角にする"""

    pipe = [normalizer.Cleanup, tokenizer.Wakachi, normalizer.Zenkaku, normalizer.Strip]


class Romaji(Finalizer):
    """制御文字や空白を除去し半角ローマ字を推測して返す"""

    pipe = [normalizer.Cleanup, tokenizer.Romaji, normalizer.Strip]


class Hiragana(Finalizer):
    """制御文字や空白を除去しひらがなを返す"""

    pipe = [normalizer.Cleanup, tokenizer.Hiragana, normalizer.Strip]


class Katakana(Finalizer):
    """制御文字や空白を除去しカタカナを返す"""

    pipe = [normalizer.Cleanup, tokenizer.Katakana, normalizer.Strip]
