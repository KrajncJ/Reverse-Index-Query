# Data Indexing Querying
Simple index and querying implementation against it.

### Before we start
Sqlite3 tools and driver is [required](https://www.sqlite.org/index.html).  
Create SQLite database or import existing (inverted-index.db).  
Also install the following lib:
  
  ``
pip install html2text nltk
``

If you have any troubles with nltk word_tokenize try to run this command

``
import nltk;
nltk.download('punkt')
``