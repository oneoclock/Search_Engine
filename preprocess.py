#Name: Hiral Athwani
#UIN: 664050185

#import os
import re
#from collections import Counter

from bs4 import BeautifulSoup

from nltk.stem import PorterStemmer

stopwords_file = 'stopwords.txt'
#data_directory = '/citeseer/citeseer'
collection = []

def parseSGML(file):
    with open(file, 'r') as f:
        soup = BeautifulSoup(f,"lxml")
    text = soup.find('title').text + soup.find('text').text
    doc_id = soup.find('docno').text
    doc_id = re.findall(r'\d+', doc_id)[0] 
    return (doc_id, text)

def parseHTML(page, url):
    soup = BeautifulSoup(page, "lxml")
    for script in soup(["script","style"]):     #does not bother if no js tags
        script.decompose()
    return (url, soup.text)
    

# for filename in os.listdir(os.getcwd() + data_directory):
#    with open(os.path.join(os.getcwd() + data_directory, filename), 'r') as f:
#       collection.append(f.read())
#       #print(filename)
#       #break
      
def tokenize(text):
    modified = re.sub(r'[^\w\s]', '', text) #remove punctuation
    modified = re.sub(r'\d+', '', modified) #removes numbers
    #print(modified)
    tokenized = modified.split()
    return tokenized

'''
tokenized_collection = []

for text in collection:
    temp = tokenize(text)
    tokenized_collection.append(temp)
    
flattened_tok_collection = [j for sub in tokenized_collection for j in sub]
lower_flattened_tok_collection = [w.lower() for w in flattened_tok_collection]
'''

"""
stopwords = []
with open(stopwords_file, 'r') as f:
    stopwords = f.read().split('\n')
    stopwords.pop(-1)   #pop last ''(empty) element
"""
    
def remove_stopwords(flat_tok_col, stopwords):
    set_stopwords = set(stopwords)
    filtered_tok = [w for w in flat_tok_col if not w in set_stopwords]
    return filtered_tok

########
def stemmer(flat_tok_col):      #stem after removing stopwords
    ps = PorterStemmer()
    stemmed_flattened_tok_collection = []

    for i in flat_tok_col:
        stemmed_flattened_tok_collection.append(ps.stem(i))
    return stemmed_flattened_tok_collection
########
