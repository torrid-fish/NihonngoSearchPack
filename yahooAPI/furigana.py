from .query import askFurigana

def char_is_kanji(c) -> bool:
    return u'\u4E00' <= c <= u'\u9FFF'

def getFurigana(query:str = "") -> list[tuple]:
    """
    Use the given query to generate a list of Char without accent.
    """
    if query == "": return []

    result = []
    if query == "": return result
    response = askFurigana(query)
    for partial in response["result"]["word"]:
        if partial.get("subword"):
            for subpartial in partial.get("subword"):
                if all(map(lambda c : char_is_kanji(c), subpartial.get("surface"))):
                    result.append((subpartial.get("surface"), subpartial.get("furigana")))
                else:
                    result.append((subpartial.get("surface"), ""))
        elif partial.get("furigana"):
            result.append((partial.get("surface"), partial.get("furigana")))
        else:
            result.append((partial.get("surface"), ""))
    
    return result
