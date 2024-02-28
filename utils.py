from SearchPack.components import *

# The range of unicode of kanji
def char_is_kanji(c) -> bool:
    return u'\u4E00' <= c <= u'\u9FFF'
def char_is_hira(c) -> bool:
    return u'\u3040' <= c <= u'\u309F'
def char_is_kata(c) -> bool:
    return u'\u30A0' <= c <= u'\u30FF'
def char_is_kata_or_hira(c) -> bool:
    return char_is_hira(c) or char_is_kata(c)


