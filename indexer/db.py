
import sqlite3

conn = sqlite3.connect('../inverted-index.db')
cursor = conn.cursor()


def insert_word(word, commit=False):
    try:
        res = cursor.execute("SELECT * FROM IndexWord WHERE  word='{0}'".format(word))
        # Do not insert if already exist
        if res.fetchone() is not None:
            return word
        cursor.execute("INSERT INTO IndexWord VALUES ('{0}')".format(word))
        if commit:
            conn.commit()
        return word
    except Exception as e:
        print('Exception (insert_word): ')
        print(e)


def insert_posting(word, document_name, frequency, indexes):
    try:
        insert_word(word)
        cursor.execute("INSERT INTO Posting VALUES ('{0}','{1}',{2},'{3}')".format(word, document_name, frequency, indexes))
        conn.commit()
    except Exception as e:
        print('Exception (insert_posting): ')
        print(e)


def search_words_in_index(word_list):
    # Build condition
    condition = ' OR '.join(["word='{0}'".format(w) for w in word_list])

    res = cursor.execute("SELECT * FROM Posting WHERE  {0} ORDER BY frequency DESC ".format(condition))
    return res.fetchall()

