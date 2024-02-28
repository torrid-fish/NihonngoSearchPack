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


def get_furigana(query) -> list[Word]:
    """
    Make sure the query is a string without "\n"
    """
    result = []
    if query == "": return result
    response = callAPI(query)
    for partial in response["result"]["word"]:
        if partial.get("subword"):
            for subpartial in partial.get("subword"):
                if all(map(lambda c : char_is_kanji(c), subpartial.get("surface"))):
                    result.append([subpartial.get("surface"), subpartial.get("furigana")])
                else:
                    result.append([subpartial.get("surface"), None])
        elif partial.get("furigana"):
            result.append([partial.get("surface"), partial.get("furigana")])
        else:
            result.append([partial.get("surface"), None])
    
    return result

def syllable_num(s: str):
    """
    Return the number of syllable of the given hiragana.
    """