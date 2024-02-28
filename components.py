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
        self.accent = accent

    def 

    def print(self):
        print("{%s|%s;%d}" % (self.word, self.furigana, self.accent))

class Sentence:
    """
    The unit that holds a word.
    """
    def __init__(self, sentence: list[Word]):
        self.sentence = sentence

