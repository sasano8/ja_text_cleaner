import re
from functools import partial
from typing import Set

from . import mappings

replace_blank = partial(re.sub, "\s+", "　")


def build_mapping(replace: str, *mappings: Set[str]):
    mapping = {}
    for group in mappings:
        for key in group:
            mapping[key] = replace
    return mapping


def build_trans(replace: str, *mappings: Set[str]):
    mapping = build_mapping(replace, *mappings)
    mapping.pop(replace, None)
    return str.maketrans(mapping)


mapping_normalize_blank = build_trans(
    " ", mappings.blank, mappings.tab, mappings.newline
)


def normalize_ja(text: str):
    if text is None:
        return text
    text = normalize_html(text)
    return replace_blank(text)


def normalize_html(text: str):
    if text is None:
        return text
    return text.translate(mapping_normalize_blank)
