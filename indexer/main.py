from selenium import webdriver
import os
import html2text
from nltk.tokenize import word_tokenize
import string
import db
from collections import defaultdict
from stopwords import stop_words_slovene
import time
from tabulate import tabulate

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
    return all_tokens


def build_word_indexes(word_list):
    index = defaultdict(list)
    for i in range(len(word_list)):
        word = word_list[i]
        normalized = normalize_word(word)
        if normalized not in stop_words_slovene and normalized not in string.punctuation:
            index[normalized].append(i)
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


def index_files(display_progress=False):
    to_index = get_document_paths()
    processed = 0
    all = len(to_index)
    for file_name in to_index:
        processed += 1
        if display_progress:
            print('In progress: {0} -> ({1} of {2})'.format(file_name, processed, all))
        relative_p = '{0}/{1}'.format(DOCUMENT_ROOT,file_name)
        words = get_page_words(relative_p)
        indexes = build_word_indexes(words)
        store_indexes(file_name, indexes)


def build_one_snippet(words, around_index, words_around=3):
    from_index = max(around_index-words_around, 0)
    to_index = min(around_index+words_around+1, len(words))
    return " ".join(words[from_index:to_index])


def build_search_snippet(document_name, word_indexes):
    # @TODO This part here is pretty slow. Should optimise this if needed.
    words = get_page_words('{0}/{1}'.format(DOCUMENT_ROOT, document_name))
    return ' ... '.join([build_one_snippet(words, int(index)) for index in word_indexes])


def search(expression):
    # Start measuring time
    start = time.time()

    parts = [normalize_word(x) for x in expression.split(' ')]
    documents = db.search_words_in_index(parts)
    results = []
    for doc in documents:
        document = doc[1]
        freq = doc[2]
        text = build_search_snippet(document, doc[3].split(','))
        results.append([freq, document, text])

    print('Result for query {0}: \n'.format(expression))
    print('Result found in {0}ms'.format(round(time.time() - start, 2)))
    print(tabulate(results, headers=['Frequencies', 'Document', 'Snippet']))


if __name__ == '__main__':
    # Uncomment this line to build indexes
    # index_files(display_progress=True)
    # Search example
    search("Inšpekcijskemu")
