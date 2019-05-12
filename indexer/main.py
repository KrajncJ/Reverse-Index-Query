from selenium import webdriver
import os
import html2text
from nltk.tokenize import word_tokenize
import string
import db
from collections import defaultdict
from stopwords import stop_words_slovene

# Tels us in which folder are html files
DOCUMENT_ROOT = '../data'


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


def get_document_paths():
    file_list = []
    for folder in os.listdir(DOCUMENT_ROOT):
        for file in os.listdir('{0}/{1}'.format(DOCUMENT_ROOT,folder)):
            if file.endswith('.html'):
                file_list.append('{0}/{1}'.format(folder,file))
    return file_list


def index_files():
    for file_name in get_document_paths():
        relative_p = '{0}/{1}'.format(DOCUMENT_ROOT,file_name)
        words = get_page_words(relative_p)
        indexes = build_word_indexes(words)
        store_indexes(file_name, indexes)


if __name__ == '__main__':

    index_files()

