#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Name: Hiral Athwani
#UIN: 664050185

import preprocess
import os
from collections import defaultdict
from math import log, sqrt
import sys
import requests

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#data_directory = '/cranfield/cranfieldDocs'
query_file = '/queries.txt'
#relevance_file = '/relevance.txt'

#data_path = sys.argv[1]
query_path = 'queries.txt'  #sys.argv[2]
#relevance_path = sys.argv[3]

def dd():
    return defaultdict(int)

def index(links,stopwords):
    inverted_index = defaultdict(dd)
    error = 0
    num_docs = 0
    for link in links:
        num_docs += 1
        #file_path = os.path.join(data_path + data_directory, file)
        print("Requesting ", num_docs)
        try:
            raw_HTML_content = requests.get(link, verify = False).content
        except:
            error += 1
            print("Total errors: ", error)
            continue
        print("Received", num_docs)
        #doc_id, doc = preprocess.parseSGML(file_path)
        doc_id, doc = preprocess.parseHTML(raw_HTML_content, link)
        doc = preprocess.tokenize(doc)  #half-angle -> halfangle
        doc = preprocess.remove_stopwords(doc,stopwords)
        doc = preprocess.stemmer(doc)
        doc = preprocess.remove_stopwords(doc,stopwords)  #to remove stopwords created after stemming
        #col.append(doc)
        for token in doc:
            inverted_index[token][doc_id] += 1
        print("Done: ", num_docs)
        
    document_lengths = defaultdict(int)
    
    for token in inverted_index:
        for doc in inverted_index[token]:
            tf = inverted_index[token][doc]
            df = len(inverted_index[token])
            idf = log((num_docs/df), 10)
            document_lengths[doc] += (tf*idf)**2
    
    return (inverted_index, document_lengths, num_docs)

  
## Query Processing ##
def preprocess_query(stopwords):
    queries = []
    processed_queries = []
    with open(query_path,'r') as f:
        queries = f.readlines()
    
    for query in queries:
        processed_query = preprocess.tokenize(query)
        processed_query = preprocess.remove_stopwords(processed_query,stopwords)
        processed_query = preprocess.stemmer(processed_query)
        processed_query = preprocess.remove_stopwords(processed_query,stopwords)
        processed_queries.append(processed_query)
    return processed_queries

def preprocess_query_(stopwords, q):
    queries = q
    processed_queries = []
    # with open(query_path,'r') as f:
    #     queries = f.readlines()
    
    for query in queries:
        processed_query = preprocess.tokenize(query)
        processed_query = preprocess.remove_stopwords(processed_query,stopwords)
        processed_query = preprocess.stemmer(processed_query)
        processed_query = preprocess.remove_stopwords(processed_query,stopwords)
        processed_queries.append(processed_query)
    return processed_queries

def calc_tf_query(tok, quer):   #calculates tf of a query
    tf = 0
    for q in quer:
        if tok == q:
            tf += 1
    return tf

#calculates unnormalized similarity table for a query with all docs
def calc_similarity_table(query, inverted_index, document_lengths, num_docs):
    similarity_table = defaultdict(int)
    for token in query:
        if token in inverted_index:
            for doc in inverted_index[token]:
                tf = inverted_index[token][doc]
                df = len(inverted_index[token])
                idf = log((num_docs/df + 1), 10)
                weight_word_doc = tf*idf
                tf_q = calc_tf_query(token, query)
                print(tf_q,df)
                #return
                weight_word_query = tf_q * idf
                similarity_table[doc] += weight_word_doc * weight_word_query
    for doc in similarity_table:
        similarity_table[doc] /= sqrt(document_lengths[doc])
    return similarity_table

'''
def retrieve_relevance():
    with open(relevance_path, 'r') as f:
        raw_relevance = f.readlines()
    query_rel = []
    for r in raw_relevance:
        query_rel.append(r.split())
    rel_dict = {}
    for q in query_rel:
        rel_dict[q[0]] = []
    for q in query_rel:
        rel_dict[q[0]].append(q[1])
    return rel_dict

processed_queries = preprocess_query()
rel_dict = retrieve_relevance()

def check_precision_recall(k, q, rel_q_d):
    similarity_table = calc_similarity_table(processed_queries[q])
    st = sorted(similarity_table.items(), key=lambda kv: kv[1], reverse=True)
    num_relevant_retrieved = 0
    st_onlyDocs = [i[0] for i in st[0:k]]
    for rel in rel_q_d[str(q+1)]:
        if rel in st_onlyDocs:
            num_relevant_retrieved += 1
    precision = num_relevant_retrieved / k
    recall = num_relevant_retrieved / len(rel_q_d[str(q+1)])
    return (precision, recall)

def out_query_doc(queries,k):
    query_doc_pairs = []
    for q in range(len(queries)):
        similarity_table = calc_similarity_table(queries[q])
        st = sorted(similarity_table.items(), key=lambda kv: kv[1], reverse=True)
        st_onlyDocs = [i[0] for i in st[0:k]]
        
        for doc in st_onlyDocs:
            query_doc_pairs.append((q+1,doc))
    return query_doc_pairs
        
query_doc_pairs = out_query_doc(processed_queries, 50)

ks = [10, 50, 100, 500]
prec_recall_qs = {}     #precision recall for all queries
for query in range(len(rel_dict)):
    prec_recall_ks = []     #precision recall for different ks
    for k in ks:
        precision, recall = check_precision_recall(k, query, rel_dict)
        prec_recall_ks.append((precision, recall))
    prec_recall_qs[query+1] = prec_recall_ks
    
def avg_precision_recall(p_r_dict,ks):      #over all queries
    #precision
    avgPrecs = []
    avgRecalls = []
    num_queries = len(p_r_dict)
    for k in range(len(ks)):
        avg_prec = 0
        avg_recall = 0
        for p_r in p_r_dict:
            avg_prec += p_r_dict[p_r][k][0]
            avg_recall += p_r_dict[p_r][k][1]
        avg_prec /= num_queries
        avg_recall /= num_queries
        avgPrecs.append(avg_prec)
        avgRecalls.append(avg_recall)
    return (avgPrecs, avgRecalls)

avgPrecs, avgRecalls = avg_precision_recall(prec_recall_qs, ks)

print("Query Document Pairs in Descending order of relevancy")
print(query_doc_pairs)
print("\nAverage Precision and Recall over queries for different k values")
for k in range(len(ks)):
    print('K = ', ks[k], "Precision: ", avgPrecs[k], "Recall: ", avgRecalls[k])
    
print("\nPrecision and Accuracy Pairs for Each Query")
print(prec_recall_qs)
'''