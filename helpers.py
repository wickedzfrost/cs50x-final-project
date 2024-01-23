from flask import redirect, render_template, session
from functools import wraps
import xml.etree.ElementTree as ET
import random
import urllib.parse
import json

tree = ET.parse("JMdict_e.xml")
root = tree.getroot()


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def generate():

    ls = []
    while True:
        rand = random.randrange(0, len(root))
        condition = root[rand].findall("sense")[0].findall("pos")[0].text
        if "noun" in condition or "nouns" in condition or "adjective" in condition or "na-adjective" in condition or "adverb" in condition or "expressions" in condition:
            text = (root[rand].findall("r_ele")[0][0].text)
            if text[-1] != "ん" and text[-1] != "ン":
                definition = root[rand].findall("sense")[0].findall("gloss")[0].text
                dictionary = {text:definition}
                ls.append(dictionary)
        if len(ls) == 1:
            break
    return ls


def check(encoded):

    decoded_string = urllib.parse.unquote(encoded)
    text = decoded_string[5:len(decoded_string)]
    for elem in root.iter():
        if elem.text == text:
            return decoded_string
    return "False"


def genword(encoded):
    decoded_string = urllib.parse.unquote(encoded)
    last_mora = decoded_string[5:len(decoded_string)]
    ls = []
    for i in range(0, len(root)):
        condition = root[i].findall("sense")[0].findall("pos")[0].text
        if "noun" in condition or "nouns" in condition or "adjective" in condition or "na-adjective" in condition or "adverb" in condition or "expressions" in condition:
            word = root[i].findall("r_ele")[0][0].text
            definition = root[i].findall("sense")[0].findall("gloss")[0].text
            if word[0] == last_mora and (word[-1] != "ん" and word[-1] != "ン" and word[-1] != "っ" and word[-1] != "ッ"):
                dictionary = {word:definition}
                ls.append(dictionary)

    index = random.randrange(0, len(ls))
    text = ls[index]
    text = json.dumps(text)
    return text


def genword_special(encoded):
    decoded_string = urllib.parse.unquote(encoded)
    last_mora = decoded_string[5:len(decoded_string)]
    ls = []
    for i in range(0, len(root)):
        condition = root[i].findall("sense")[0].findall("pos")[0].text
        if "noun" in condition or "nouns" in condition or "adjective" in condition or "na-adjective" in condition or "adverb" in condition or "expressions" in condition:
            word = root[i].findall("r_ele")[0][0].text
            definition = root[i].findall("sense")[0].findall("gloss")[0].text
            if word[0] == last_mora[0] and (word[-1] != "ん" and word[-1] != "ン" and word[-1] != "っ" and word[-1] != "ッ"):
                try:
                    if word[1] == last_mora[1]:
                        dictionary = {word:definition}
                        ls.append(dictionary)
                except IndexError:
                    pass

    index = random.randrange(0, len(ls))
    text = ls[index]
    text = json.dumps(text)
    return text


def decode(input):
    decoded = urllib.parse.unquote(input)
    return decoded[6:len(decoded)]
