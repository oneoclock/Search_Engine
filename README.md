# Search_Engine<br>

Following Libraries should be installed before running the code.<br>
<br>
Flask<br>
BeautifulSoup<br>
NLTK<br>
requests<br>

To run the code,<br> 
Open terminal in Current working directory.<br>
Run export FLASK_APP=search.py<br>
flask run<br>
<br>
This will return a link to the search engine web page.<br>
<br>
Please make sure that the directory structure is maintained and all txt files such as stopwords.txt are in the same directory of search.py<br>
<br>
List of files and what they do:<br>
crawler.py crawls webpages in the uic.edu domain and stores an inverted index in the CWD.<br>
indexer.py consists of the implementation of the TF-IDF indexer and is imported by crawler.py<br>
preprocess.py implements the preprocessing of documents and queries.<br>
inverted_index.txt consists of the inverted_index.<br>
document_lengths.txt consists of length of all documents.<br>
num_docs.txt consists of total number of documents.<br>
links,txt consists of all the links parsed.<br>
<br>
templates directory contains the HTML source code.
