#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  3 11:50:21 2021

@author: helios
"""

from urllib.request import urljoin
from bs4 import BeautifulSoup
import requests
from urllib.request import urlparse
import indexer


links_intern = set()
input_url = "https://cs.uic.edu"
domain = "https://uic.edu"

# Set for storing urls with different domain
links_extern = set()
  
  
# Method for crawling a url at next level
def level_crawler(input_url):
    #add condition if url in llinks_intern dont scan
    temp_urls = set()
    current_url_domain = urlparse(domain).netloc
  
    # Creates beautiful soup object to extract html tags
    beautiful_soup_object = BeautifulSoup(
        requests.get(input_url, verify = False).content, "lxml")
  
    # Access all anchor tags from input 
    # url page and divide them into internal
    # and external categories
    for anchor in beautiful_soup_object.findAll("a"):
        href = anchor.attrs.get("href")
        if(href != "" and href != None and ('mailto' not in href) ):
            print(href)
            href = href.strip()
            href = urljoin(input_url, href)
            href_parsed = urlparse(href)
            href = href_parsed.scheme
            href += "://"
            href += href_parsed.netloc
            href += href_parsed.path
            final_parsed_href = urlparse(href)
            is_valid = bool(final_parsed_href.scheme) and bool(
                final_parsed_href.netloc)
            if is_valid:
                if current_url_domain not in href and href not in links_extern:
                    print("Extern - {}".format(href))
                    links_extern.add(href)
                if current_url_domain in href and href not in links_intern:
                    print("Intern - {}".format(href))
                    links_intern.add(href)
                    temp_urls.add(href)
    return temp_urls

queue = []
bfs_traversal = []
bfs_traversal.append(input_url)
queue.append(input_url)
level = 0
while len(bfs_traversal) < 4000 :
    level += 1
    for count in range(len(queue)):
        url = queue.pop(0)
        urls = level_crawler(url)
        for i in urls:
            bfs_traversal.append(i)
            queue.append(i)
        print("----------------------------------------------")
        print("----------------------------------------------")
        print("----------------------------------------------")
        print(level)
        print(len(bfs_traversal))
        print("----------------------------------------------")
        print("----------------------------------------------")
        print("----------------------------------------------")
    
stopwords = []
stopwords_file = 'stopwords.txt'
with open(stopwords_file, 'r') as f:
    stopwords = f.read().split('\n')
    stopwords.pop(-1)   #pop last ''(empty) element
    
    inverted_index, document_lengths, num_docs = indexer.index(bfs_traversal[0:3001], 
                                                               stopwords)

#relevance_file = '/relevance.txt'
    query_path = 'queries.txt'  #sys.argv[2]
    q=['university']
    processed_queries = indexer.preprocess_query(stopwords,q) #pass query as list

    similarity_table = indexer.calc_similarity_table(processed_queries[0], 
                                         inverted_index, document_lengths, 
                                         num_docs)