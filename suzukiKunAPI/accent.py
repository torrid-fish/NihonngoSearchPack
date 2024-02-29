from .query import askAccent

def getAccent(s: str) -> list[tuple]:
    """
    Use the given query to generate a List of pairs of accent data.
    """
    phrasingTexts, phrasingSubscripts = askAccent(s)

    # Since suzukikun will parsed into small sentences, we need to merge them back
    results = []
    for d, s in zip(phrasingTexts, phrasingSubscripts):
        # Fetch subscript text (in the first span tag, final tag is the halt sign)
        phrase = s.find_all("span", recursive= False)
        sentence = ""
        for p in phrase: sentence += p.get_text()

        # Fetch processed data
        temp = d.find_all("span", recursive= False)
        for p in temp:
            # Check accent mark (we don't use unvoiced)
            accent = -1 # No accent
            if p['class'][0] == 'accent_plain': accent = 0 # Plain
            elif p['class'][0] == 'accent_top': accent = 1 # Down
            
            results.append((p.get_text(), accent))

    return results