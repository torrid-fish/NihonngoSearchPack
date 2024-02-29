def char_is_kanji(c) -> bool:
    return u'\u4E00' <= c <= u'\u9FFF'

def is_kanji(s: str) -> bool:
    return all([char_is_kanji(c) for c in s])

def char_is_hira(c) -> bool:
    return u'\u3040' <= c <= u'\u309F'

def is_hira(s: str) -> bool:
    return all([char_is_hira(c) for c in s])

def char_is_kata(c) -> bool:
    return u'\u30A0' <= c <= u'\u30FF'

def is_kata(s: str) -> bool:
    return all([char_is_kata(c) for c in s])

def char_is_number(c) -> bool:
    # 0~9
    A = c in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    # ０~９
    B = c in ["０", "１", "２", "３", "４", "５", "６", "７", "８", "９"]
    # 一~九
    C = c in ["〇", "一", "二", "三", "四", "五", "六", "七", "八", "九"]
    # 零~玖
    D = c in ["零", "壱", "弐", "参", "肆", "伍", "陸", "漆", "捌", "玖"]
    return A or B or C or D

def is_number(s: str) -> bool:
    return all([char_is_number(c) for c in s])

def char_is_small_part(c: str) -> bool:
    return c == "ゃ" or c == "ゅ" or c == "ょ" or c == "ぁ" or c == "ぃ" or c == "ぅ" or c == "ぇ" or c == "ぉ"

def kata_to_hira(s: str) -> str:
    return "".join([chr(ord(c) - 96) if u'\u30A1' <= c <= u'\u30F6' else c for c in s])

def get_furiganas(furigana: str = "") -> list[str]:
    """
    Get the furiganas from the furigana string.

    * All the given characters should only be furigana.
    """
    if furigana == "":
        return []
    else:
        result = []
        
        for c in furigana:
            if char_is_small_part(c) and len(result) > 0:
                result[-1] += c
            else:
                result.append(c)

        return result

def minimum_edit_distance(s1: str, s2: str) -> int:
    """
    Calculate the minimum edit distance between two strings.
    The only acceptable operation is insertion. (Will insert a full-width space character)
    This algorithm is an O(n^2) dynamic programming algorithm.
    """
    m, n = len(s1), len(s2)
    # Create a table to store results of subproblems 
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    # Create a table to back tracking
    bt = [[0] * (n + 1) for _ in range(m + 1)]
    # Initialization
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Table filling
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
                bt[i][j] = 1 # From i - 1, j - 1
            else:
                dp[i][j] = min(dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1]) + 1
                if dp[i][j] == dp[i - 1][j - 1] + 1:
                    bt[i][j] = 2
                elif dp[i][j] == dp[i - 1][j] + 1:
                    bt[i][j] = 3
                else:
                    bt[i][j] = 4

    # Back Tracking
    # Use space to fill the place of the inserted character
    newS1, newS2 = "", ""
    i, j = m, n
    while i > 0 and j > 0:
        if bt[i][j] == 1:
            newS1 = s1[i - 1] + newS1
            newS2 = s2[j - 1] + newS2
            i -= 1
            j -= 1
        elif bt[i][j] == 2:
            newS1 = s1[i - 1] + newS1
            newS2 = "　" + newS2
            i -= 1
            j -= 1
        elif bt[i][j] == 3:
            newS1 = s1[i - 1] + newS1
            newS2 = "　" + newS2
            i -= 1
        else:
            newS1 = "　" + newS1
            newS2 = s2[j - 1] + newS2
            j -= 1
    
    assert(len(newS1) == len(newS2))

    return dp[m][n], newS1, newS2

def genearte_accent_map(furiStr: str, accentStr: str, accentData: list[tuple]) -> list[int]:
    """
    Since the content of furi and accent might be different (from different APIs), we will first use minimum edit distance algorithm to align these two strings,
    then generate the accent map for the chars in s1.
    """
    _, alignedFuri, alignedAccent = minimum_edit_distance(furiStr, accentStr)
    alignedFuri, alignedAccent = get_furiganas(alignedFuri), get_furiganas(alignedAccent) # Merge small symbols

    # Fill accent back
    result = []
    for i in range(len(alignedFuri)):
        if char_is_hira(alignedFuri[i]):
            result.append(accentData.pop(0)[1])
        else:
            result.append(-1)
    return result