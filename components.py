"""
The basic definition of classes in this pack.
"""

class Word:
    """
    The basic component of a sentence. It will contains three infomation:
    - word: It can be either kanji, hiragana, or katakana.
    - furigana: The reading of the word.
    - accent: The accent of the word. It will be an number.
    """
    def __init__(self, word: str, furigana : str = None, accent : int = None):
        self.word = word
        self.furigana = furigana
        self.furiganas = self.getFuriganas(furigana)
        self.accent = accent

    @staticmethod
    def getFuriganas(furigana: str = "") -> list[str]:
        """
        Get the furiganas from the furigana string.

        * All the given characters should only be furigana.
        """
        if furigana == "":
            return []
        else:
            result = []
            
            def char_is_small_part(c: str) -> bool:
                return c == "ゃ" or c == "ゅ" or c == "ょ" or c == "ぁ" or c == "ぃ" or c == "ぅ" or c == "ぇ" or c == "ぉ"
            
            for c in furigana:
                if char_is_small_part(c) and len(result) > 0:
                    result[-1] += c
                else:
                    result.append(c)

            return result

    def print(self):
        print("{%s|%s;%d}" % (self.word, self.furigana, self.accent))

class Sentence:
    """
    The unit that holds a word.
    """
    def __init__(self, sentence: list[Word]):
        self.sentence = sentence

