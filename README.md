# Search_Engine

Following Libraries should be installed before running the code.

Flask
BeautifulSoup
NLTK
requests

To run the code, 
Open terminal in Current working directory.
Run export FLASK_APP=search.py  
flask run

This will return a link to the search engine web page.

Please make sure that the directory structure is maintained and all txt files such as stopwords.txt are in the same directory of search.py

List of files and what they do:<br>
crawler.py crawls webpages in the uic.edu domain and stores an inverted index in the CWD.
indexer.py consists of the implementation of the TF-IDF indexer and is imported by crawler.py
preprocess.py implements the preprocessing of documents and queries.
inverted_index.txt consists of the inverted_index
document_lengths.txt = consists of length of all documents
num_docs.txt = consists of total number of documents

templates directory contains the HTML source code.
