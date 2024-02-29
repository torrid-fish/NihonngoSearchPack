"""
The basic definition of classes in this pack. A "Sentence" is composed of many "Char"s.

About the syntax in Hackmd, we use the following syntax to mark the furigana:

        痛める -> {痛|い<b>た</b>}{め|<i>*&emsp;*</i>}る (This sentence is composed of three Chars)

We use {|} to represent the use of ruby 
This syntax is supported by markdown-it, and can be applyed on hackmd

As for accent, we use the css setting written by @OrangeSagoCream based on @Koios's idea
The syntax sugar is supported like this:

        <b>:  apply the line
        <i>:  higher line to match the kanji, type one more character than the marked content to get proper length
    
        italic(**): apply top accent (right border) 

To use this css style and syntax, type `{%hackmd @OrangeSagoCream/Accent %}` at the first line of your hackmd.
"""

from .utils import *
from .yahooAPI.furigana import getFurigana
from .suzukiKunAPI.accent import getAccent
import re

CharType = ["kanji", "hira", "kata", "number", "symbol"]

class Char:
    """
    The basic component of a sentence. It will contains three infomation:
    - word: It can be either kanji, hiragana, or katakana.
    - furigana: The reading of the word.
    - accent: The accent of the word. It will be an number.
    """
    def __init__(self, word: str, furigana : str = "", accent : int = -1):
        self.word = word
        self.accent = accent # If accent = -1, then this word don't need to draw accent
        
        # Determine the type
        if is_kanji(word):
            self.type = CharType[0]
        elif is_hira(word):
            self.type = CharType[1]
        elif is_kata(word):
            self.type = CharType[2]
        elif is_number(word):
            self.type = CharType[3]
        else:
            self.type = CharType[4]
        
        # Determine furigana
        if self.type == "hira":
            self.furigana = word
        elif self.type == "kata":
            self.furigana = kata_to_hira(word)
        else:
            self.furigana = furigana

        self.furiganas = get_furiganas(self.furigana)

    def print(self):
        """
        Print the data of the word.
        """
        print("{%s|%s;%d}" % (self.word, ' '.join(self.furiganas), self.accent))

    def getHackmdSyntax(self, addAccent: bool = True, addFuriOnHira: bool = False, addFuriOnKata: bool = False, addFuriOnKanji: bool = True) -> str:
        """
        Get the syntax of hackmd.
        """
        # Whether to add furigana
        addFuri = (addFuriOnHira and self.type == "hira") or (addFuriOnKata and self.type == "kata") or (addFuriOnKanji and self.type == "kanji")
            
        if addAccent and self.accent == 0:
            # At most the last two characters will be drawn
            threshold = max(1, len(self.furiganas)-2)

            if addFuri:
                upperData = "".join(self.furiganas[:threshold]) + "<b>" + "".join(self.furiganas[threshold:]) + "</b>"
            else:
                upperData = "<i>" + "&emsp;" + "</i>"

        elif addAccent and self.accent > 0 and self.accent <= len(self.furiganas) - 1:
            threshold = self.accent - 1

            if addFuri:
                upperData = "".join(self.furiganas[:threshold]) + "<b>*" + self.furiganas[threshold] + "*</b>" + "".join(self.furiganas[threshold+1:])
            else:
                upperData = "<i>*" + "&emsp;" + "*</i>"
        elif addFuri:
            upperData = self.furigana
        else: 
            upperData = ""

        # Special case for accent on hira or kata
        if not addFuri and addAccent and self.accent > 0 and self.accent < len(self.furiganas):
            if self.type == "hira":
                headWord, tailWord = ''.join(self.furiganas[:self.accent]), ''.join(self.furiganas[self.accent:])
            elif self.type == "kata":
                headWord, tailWord = hira_to_kata(''.join(self.furiganas[:self.accent])), hira_to_kata(''.join(self.furiganas[self.accent:]))
            else:
                headWord, tailWord = self.word, ""
            # Return the seperated parts
            return "{%s|%s}%s" % (headWord, upperData, tailWord)
        elif upperData:
            return "{%s|%s}" % (self.word, upperData)
        else:
            return self.word

class Sentence:
    """
    The unit that holds Chars.
    """
    def __init__(self, sentence: list[Char]):
        self.sentence = sentence

    def __init__(self, sentence: str, accent: bool = True):
        self.sentence = []

        # Previous length of sentence
        threshold = 0 
        # The input might be too long, we use "\n" to seperate the sentence
        for s in sentence.split("\n"):

            # Use regex to choose predefined furiganas with syntax {a|b}, extract a and b
            predefined = re.findall(r'{([^|]+)\|([^}]+)}', s)
            s = re.sub(r'{([^|]+)\|([^}]+)}', r'※\1', s)

            # Get the furigana
            furigana = getFurigana(s)
            cnt, replace = 0, False
            for t in furigana: 
                if t[0] == "※":
                    replace = True
                elif replace:
                    self.sentence.append(Char(predefined[cnt][0], predefined[cnt][1]))
                    replace = False
                    cnt += 1
                else:
                    self.sentence.append(Char(t[0], t[1]))
                    
            yahooGeneratedFuri = self.getFurigana(threshold)

            # Add accent from suzukikun
            if accent:
                # Get the accent
                temp = getAccent(s)
                accentData = []
                suzukiGeneratedFuri = ""
                for c, _ in temp:
                    if char_is_hira(c):
                        accentData.append((c, _))
                        suzukiGeneratedFuri += c

                # Generate accent map
                listOfFuri = list(map(lambda c: c.furiganas, self.sentence[threshold:]))
                accentMap = genearte_accent_map(yahooGeneratedFuri, suzukiGeneratedFuri, accentData, listOfFuri)

                # Fill accent
                for i in range(threshold, len(self.sentence)):
                    self.sentence[i].accent = accentMap[i-threshold]

            # Fill the "\n" back
            self.sentence.append(Char("\n"))
            threshold = len(self.sentence)


    def getWord(self, begin: int = 0, end: int = -1) -> str:
        """
        Get the word (base Part).
        """
        result = ""
        for word in self.sentence[begin:end]:
            result += word.getWord()
        return result
    
    def getFurigana(self, begin: int = 0, end: int = -1) -> str:
        """
        Get the furigana.
        """
        result = ""
        for word in self.sentence[begin:end]:
            result += word.furigana
        return result

    def getSentence(self, begin: int = 0, end: int = -1) -> list[Char]:
        """
        Get the sentence.
        """
        return self.sentence[begin:end]
    
    def getAccent(self, begin: int = 0, end: int = -1) -> list[int]:
        """
        Get the accent.
        """
        result = []
        for word in self.sentence[begin:end]:
            result.append(word.accent)
        return result
    
    def getType(self, begin: int = 0, end: int = -1) -> list[str]:
        """
        Get the type of the word.
        """
        result = []
        for word in self.sentence[begin:end]:
            result.append(word.type)
        return result

    def print(self, begin: int = 0, end: int = -1) -> str:
        """
        Print the sentence.
        """
        for word in self.sentence[begin:end]:
            word.print()

    def getHackmdSyntax(self, begin: int = 0, end: int = -1, addAccent: bool = True, addFuriOnHira: bool = False, addFuriOnKata: bool = False, addFuriOnKanji: bool = True) -> str:
        """
        Get the syntax of hackmd.
        """
        result = ""
        for word in self.sentence[begin:end]:
            result += word.getHackmdSyntax(addAccent, addFuriOnHira, addFuriOnKata, addFuriOnKanji)
        return result