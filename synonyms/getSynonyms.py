import requests
import json

words = ""
with open("synonyms/terms.txt", "r") as terms_file:
    words = terms_file.read()

synonyms = []

for word in words.split(","):
    word = word.lower()
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = json.loads(requests.request("GET", url).text)
    try:
        meanings = response[0]["meanings"]
    except KeyError:
        continue
    meanings = list(filter(lambda meaning: meaning["partOfSpeech"] == "noun", meanings))
    current_synonyms = []
    for meaning in meanings:
        definitions = meaning["definitions"]
        for definition in definitions:
            current_synonyms.extend(definition["synonyms"])
    for synonym in current_synonyms:
        if len(synonym.split(" ")) == 1:
            synonyms.append(f"\"{word}, {synonym}\",")

with open("synonyms/synonyms.txt", "w") as file:    
    for synonym in synonyms:
        synonym = synonym.replace("(", "")
        synonym = synonym.replace(")", "")
        file.write(synonym + "\n")
