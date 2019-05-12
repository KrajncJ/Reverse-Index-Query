from selenium import webdriver
import os
import html2text
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import db
from collections import defaultdict

# TODO removed set(stopwords.words("slovenian")).union + ---> TODO check if stopwords slovenian are available?
# TODO refactor
stop_words_slovene = set(
        ["ter","nov","novo", "nova","zato","ĹĄe", "zaradi", "a", "ali", "april", "avgust", "b", "bi", "bil", "bila", "bile", "bili", "bilo", "biti",
         "blizu", "bo", "bodo", "bojo", "bolj", "bom", "bomo", "boste", "bova", "boĹĄ", "brez", "c", "cel", "cela",
         "celi", "celo", "d", "da", "daleÄ", "dan", "danes", "datum", "december", "deset", "deseta", "deseti", "deseto",
         "devet", "deveta", "deveti", "deveto", "do", "dober", "dobra", "dobri", "dobro", "dokler", "dol", "dolg",
         "dolga", "dolgi", "dovolj", "drug", "druga", "drugi", "drugo", "dva", "dve", "e", "eden", "en", "ena", "ene",
         "eni", "enkrat", "eno", "etc.", "f", "februar", "g", "g.", "ga", "ga.", "gor", "gospa", "gospod", "h", "halo",
         "i", "idr.", "ii", "iii", "in", "iv", "ix", "iz", "j", "januar", "jaz", "je", "ji", "jih", "jim", "jo",
         "julij", "junij", "jutri", "k", "kadarkoli", "kaj", "kajti", "kako", "kakor", "kamor", "kamorkoli", "kar",
         "karkoli", "katerikoli", "kdaj", "kdo", "kdorkoli", "ker", "ki", "kje", "kjer", "kjerkoli", "ko", "koder",
         "koderkoli", "koga", "komu", "kot", "kratek", "kratka", "kratke", "kratki", "l", "lahka", "lahke", "lahki",
         "lahko", "le", "lep", "lepa", "lepe", "lepi", "lepo", "leto", "m", "maj", "majhen", "majhna", "majhni",
         "malce", "malo", "manj", "marec", "me", "med", "medtem", "mene", "mesec", "mi", "midva", "midve", "mnogo",
         "moj", "moja", "moje", "mora", "morajo", "moram", "moramo", "morate", "moraĹĄ", "morem", "mu", "n", "na", "nad",
         "naj", "najina", "najino", "najmanj", "naju", "najveÄ", "nam", "narobe", "nas", "nato", "nazaj", "naĹĄ", "naĹĄa",
         "naĹĄe", "ne", "nedavno", "nedelja", "nek", "neka", "nekaj", "nekatere", "nekateri", "nekatero", "nekdo",
         "neke", "nekega", "neki", "nekje", "neko", "nekoga", "nekoÄ", "ni", "nikamor", "nikdar", "nikjer", "nikoli",
         "niÄ", "nje", "njega", "njegov", "njegova", "njegovo", "njej", "njemu", "njen", "njena", "njeno", "nji",
         "njih", "njihov", "njihova", "njihovo", "njiju", "njim", "njo", "njun", "njuna", "njuno", "no", "nocoj",
         "november", "npr.", "o", "ob", "oba", "obe", "oboje", "od", "odprt", "odprta", "odprti", "okoli", "oktober",
         "on", "onadva", "one", "oni", "onidve", "osem", "osma", "osmi", "osmo", "oz.", "p", "pa", "pet", "peta",
         "petek", "peti", "peto", "po", "pod", "pogosto", "poleg", "poln", "polna", "polni", "polno", "ponavadi",
         "ponedeljek", "ponovno", "potem", "povsod", "pozdravljen", "pozdravljeni", "prav", "prava", "prave", "pravi",
         "pravo", "prazen", "prazna", "prazno", "prbl.", "precej", "pred", "prej", "preko", "pri", "pribl.",
         "pribliĹžno", "primer", "pripravljen", "pripravljena", "pripravljeni", "proti", "prva", "prvi", "prvo", "r",
         "ravno", "redko", "res", "reÄ", "s", "saj", "sam", "sama", "same", "sami", "samo", "se", "sebe", "sebi",
         "sedaj", "sedem", "sedma", "sedmi", "sedmo", "sem", "september", "seveda", "si", "sicer", "skoraj", "skozi",
         "slab", "smo", "so", "sobota", "spet", "sreda", "srednja", "srednji", "sta", "ste", "stran", "stvar", "sva",
         "t", "ta", "tak", "taka", "take", "taki", "tako", "takoj", "tam", "te", "tebe", "tebi", "tega", "teĹžak",
         "teĹžka", "teĹžki", "teĹžko", "ti", "tista", "tiste", "tisti", "tisto", "tj.", "tja", "to", "toda", "torek",
         "tretja", "tretje", "tretji", "tri", "tu", "tudi", "tukaj", "tvoj", "tvoja", "tvoje", "u", "v", "vaju", "vam",
         "vas", "vaĹĄ", "vaĹĄa", "vaĹĄe", "ve", "vedno", "velik", "velika", "veliki", "veliko", "vendar", "ves", "veÄ",
         "vi", "vidva", "vii", "viii", "visok", "visoka", "visoke", "visoki", "vsa", "vsaj", "vsak", "vsaka", "vsakdo",
         "vsake", "vsaki", "vsakomur", "vse", "vsega", "vsi", "vso", "vÄasih", "vÄeraj", "x", "z", "za", "zadaj",
         "zadnji", "zakaj", "zaprta", "zaprti", "zaprto", "zdaj", "zelo", "zunaj", "Ä", "Äe", "Äesto", "Äetrta",
         "Äetrtek", "Äetrti", "Äetrto", "Äez", "Äigav", "ĹĄ", "ĹĄest", "ĹĄesta", "ĹĄesti", "ĹĄesto", "ĹĄtiri", "Ĺž", "Ĺže",
         "svoj", "jesti", "imeti","\u0161e", "iti", "kak", "www", "km", "eur", "paÄ", "del", "kljub", "ĹĄele", "prek",
         "preko", "znova", "morda","kateri","katero","katera", "ampak", "lahek", "lahka", "lahko", "morati", "torej"])


# Not used currently, may use if content will be displayed with JS. Then we have to render page with browser
def open_page(path):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get("file:///" + os.path.abspath(path))
    return driver.page_source


# TODO should we open file with headless browser?
def read_data(filepath):
    file = open(filepath, 'r', encoding='utf-8').read()
    return file


def extract_text_from_html(html):
    h = html2text.HTML2Text()
    h.ignore_links = True
    return h.handle(html)


# Use this function also when searching in db for user input
def normalize_word(word):
    return word.strip(string.punctuation).lower()


def get_page_words(filepath):
    page_data = read_data(filepath)
    html_text = extract_text_from_html(page_data)
    all_tokens = word_tokenize(html_text)
    filtered = []
    for w in all_tokens:
        normalized = normalize_word(w)
        if normalized not in stop_words_slovene and normalized not in string.punctuation:
            filtered.append(normalized)
    return filtered


def build_word_indexes(word_list):
    index = defaultdict(list)
    for i in range(len(word_list)):
        word = word_list[i]
        index[word].append(i)
    return index


def store_indexes(document_name, indexes):
    for key in indexes.keys():
        db.insert_posting(key, document_name, len(indexes[key]), ",".join([str(x) for x in indexes[key]]))


if __name__ == '__main__':
    DOC_NAME = '../data/e-prostor.gov.si/e-prostor.gov.si.1.html'
    words = get_page_words(DOC_NAME)

    indexes = build_word_indexes(words)

    store_indexes(DOC_NAME, indexes)
