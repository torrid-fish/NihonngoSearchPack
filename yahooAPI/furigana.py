from query import callAPI
from SearchPack.yahooAPI.query import callAPI
from SearchPack.components import Word
from SearchPack.utils import *

def getFurigana(query) -> list[Word]:
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
