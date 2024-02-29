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

def hira_to_kata(s: str) -> str:
    return "".join([chr(ord(c) + 96) if u'\u3041' <= c <= u'\u3096' else c for c in s])

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

def minimum_edit_distance(s1: list[str], s2: list[str]):
    """
    Calculate the minimum edit distance between two given list.
    The only acceptable operation is insertion. (Will insert a None into the list)
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
    newS1, newS2 = [], []
    i, j = m, n
    while i > 0 or j > 0:
        if bt[i][j] == 1:
            newS1 = [s1[i - 1]] + newS1
            newS2 = [s2[j - 1]] + newS2
            i -= 1
            j -= 1
        elif bt[i][j] == 2:
            newS1 = [s1[i - 1]] + newS1
            newS2 = [None] + newS2
            i -= 1
            j -= 1
        elif bt[i][j] == 3:
            newS1 = [s1[i - 1]] + newS1
            newS2 = [None] + newS2
            i -= 1
        else:
            newS1 = [None] + newS1
            newS2 = [s2[j - 1]] + newS2
            j -= 1
    
    assert(len(newS1) == len(newS2))

    return dp[m][n], newS1, newS2

def genearte_accent_map(furiStr: str, accentStr: str, accentData: list[tuple], listOfFuri: list[list]) -> list[int]:
    """
    Since the content of `furiStr` and `accentStr` might be different, we will first use minimum edit distance algorithm to align them.
    As long as we align them, we will use the data from `accentData` to transform the accent data from the data type of suzukikun to our definition of accent in Char.
    Finally, we will return a list of accent with the same length of the length of `listOfFuri`.

    * The first two parameters are only composed of furigana.
    """
    _, alignedFuri, alignedAccent = minimum_edit_distance(get_furiganas(furiStr), get_furiganas(accentStr))

    result = []
    alignedFuriCnt, accentDataCnt = 0, 0
    for l in listOfFuri:
        # Default accent
        accent = -1
        for i, c in enumerate(l):
            # Go to the next accent position
            while alignedFuri[alignedFuriCnt] == None: alignedFuriCnt += 1

            assert c == alignedFuri[alignedFuriCnt]

            # If the part doesn't have accent mark, we will skip it
            if alignedAccent[alignedFuriCnt] == None: 
                alignedFuriCnt += 1 
                continue

            # Check if the accent
            if accentData[accentDataCnt][1] == 0:
                accent = 0
            elif accentData[accentDataCnt][1] == 1:
                accent = i + 1

            # Update counter
            alignedFuriCnt += 1
            accentDataCnt += 1

        # Update answer
        result.append(accent)

    assert len(result) == len(listOfFuri)

    return result
