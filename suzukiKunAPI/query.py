import requests
from bs4 import BeautifulSoup

# URL to suzukikun(すずきくん)
url = "https://www.gavo.t.u-tokyo.ac.jp/ojad/phrasing/index"

# Data of the POST method
data = {
    "data[Phrasing][text]": "",
    "data[Phrasing][curve]": "advanced",
    "data[Phrasing][accent]": "advanced",
    "data[Phrasing][accent_mark]": "all",
    "data[Phrasing][estimation]": "crf",
    "data[Phrasing][analyze]": "true",
    "data[Phrasing][phrase_component]": "invisible",
    "data[Phrasing][param]": "invisible",
    "data[Phrasing][subscript]": "visible",
    "data[Phrasing][jeita]": "invisible"
}

def askAccent(query:str = ""):
    if query == "": return [], []

    # Update the query text
    data["data[Phrasing][text]"] = query
    
    # Send a POST and receive the website html code
    website = requests.post(url, data).text
    soup = BeautifulSoup(website, "html.parser")

    # Fetch the required tags, which are phrasing_text and phrasing_subscript 
    phrasingTexts = soup.findAll("div", attrs={"class": "phrasing_text"})
    phrasingSubscripts = soup.findAll("div", attrs={"class": "phrasing_subscript"})

    return phrasingTexts, phrasingSubscripts

    


