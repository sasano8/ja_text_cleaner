# ja_text_cleaner
`ja_text_cleaner`は、日本語のための日本語変換ライブラリです。

# パイプライン
内部処理で使われているライブラリと、主な処理過程の概要を次に示します。
現在は名前の処理にマッチするように設計されています。

## わかち書き
1. 制御文字・記号等のノイズを除去
2. 形態素解析でわかち書き（sudachi）

## 読みがな取得
1. わかち書きされたトークンの読み（全角カタカナ）を取得（sudachi）
2. 辞書にヒットしない英字の読み（全角カタカナ）を取得（romkan）
3. 辞書にヒットしない半角カタカナを全角カタカナに変換（jaconv）

## その他
1. 必要に応じて半角を全角に変換（mojimoji）
2. 必要に応じてカタカナからひらがな・ヘボン式に変換（romkan）



# システム要件

- Python 3.8+

# インストール
`ja_text_cleaner`のほかに、形態素解析（sudachi）で使用する辞書（sudachidict_core）が必要です。

``` shell
pip install ja_text_cleaner sudachidict_core
```

# 始める


``` Python
from ja_text_cleaner import name

# 制御文字・記号はノイズとして除去されます
name.Wakachi(" \t\n\xa0a\u3000-!_")  # "a"

# 形態素解析結果はsudachiの処理結果に依存します
name.Wakachi("abc123あいうアイウｱｲｳ日本!")  # "abc　123　あ　いう　アイウｱｲｳ　日本"

# CJK互換漢字はCJK統合漢字へ正規化（NFC・NFKC）されません
name.Wakachi("神")  # "神"

name.Wakachi("日本太郎")  # "日本　太郎"
name.Zenkaku("日本太郎")  # "日本　太郎"
name.Katakana("日本太郎")  # "ニッポン　タロウ"
name.Hiragana("日本太郎")  # "にっぽん　たろう"
name.Romaji("日本太郎")  # "nippon tarou"

name.Wakachi("nippon tarou")  # "nippon　tarou"
name.Zenkaku("nippon tarou")  # "ｎｉｐｐｏｎ　ｔａｒｏｕ"
name.Katakana("nippon tarou")  # "ニッポン　タロウ"
name.Hiragana("nippon tarou")  # "にっぽん　たろう"
name.Romaji("nippon tarou")  # "nippon tarou"

name.Wakachi("abc")  # "abc"
name.Zenkaku("abc")  # "ａｂｃ"
name.Katakana("abc")  # "エービーシー"
name.Hiragana("abc")  # "えーびーしー"
name.Romaji("abc")  # "e-bi-shi-"

name.Wakachi("伊藤")  # "伊藤"
name.Zenkaku("伊藤")  # "伊藤"
name.Katakana("伊藤")  # "イトウ"
name.Hiragana("伊藤")  # "いとう"
name.Romaji("伊藤")  # "itou"

```

# 注意
本ライブラリは実験段階です。

