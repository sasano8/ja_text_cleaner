blank = {
    # https://ja.wikipedia.org/wiki/%E3%82%B9%E3%83%9A%E3%83%BC%E3%82%B9
    # https://blog.fenrir-inc.com/jp/2011/06/post_51.html
    # https://pata2.jp/127/stylesheets/css_others/whitespace_character.html
    " ",  # same: \s
    "　",  # same: \u3000
    "\xa0",  # &nbsp 改行しないスペース
    "\u2002",  # &ensp
    "\u2003",  # &emsp
    "\u2004",  # &emsp13
    "\u2005",  # &emsp14
    "\u2006",  # &#x2006
    "\u2007",  # &numsp
    "\u2008",  # &puncsp
    "\u2009",  # &thinsp
    "\u200A",  # &hairsp
    "\u200B",  # &NegativeMediumSpace
    "\u3000",  # &#x3000(全角スペース)
    "\ufeff",  # &#xFEFF
}

tab = {"\t", "\u0009"}  # same: \t

newline = {"\r", "\n"}


ハイフン = {"\u00AD"}  # &shy


# hiragana = [chr(i) for i in range(ord("ぁ"), ord("ん") + 2)]
hiragana = [chr(i) for i in range(ord("ぁ"), 12439)]
katakana = [chr(i) for i in range(12449, 12449 + 86)]
kana_han = [chr(i) for i in range(65393, 65393 + 86)]

# "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
han_to_zen = {chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)}
zen_to_han = {v: k for k, v in han_to_zen.items()}

chr(12449)

kana_to_hira = [hiragana]


# 日本語名を正規化したい

# 理想
# NFKCに正規化されているが、なるべく記号等はそのまま
# 日本語は合成文字になっている
# 英数字は半角　日本語は全角
# 制御文字は空白になっている
#
