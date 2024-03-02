from collections import defaultdict
import pickle
import os
import numpy as np

from string_processing import *


def intersect_query(doc_list1, doc_list2):
    # TODO: you might like to use a function like this 
    # in your run_boolean_query implementation
    # for full marks this should be the O(n + m) intersection algorithm for sorted lists
    # using data structures such as sets or dictionaries in this function will not score full marks
    
    # record the position of element in two doc_lists
    pos1 = 0
    pos2 = 0
    len1 = len(doc_list1)
    len2 = len(doc_list2)
    res = []

    while pos1 < len1 and pos2 < len2:
        # not matched
        if doc_list1[pos1] < doc_list2[pos2]:
            # element in doc_list1 go to the next position
            pos1 += 1
        elif doc_list1[pos1] > doc_list2[pos2]:
            # element in doc_list1 go to the next position
            pos2 += 1
            
        #matched
        else:
            # save element
            res.append(doc_list1[pos1])
            # check subsequent element
            pos1 += 1
            pos2 += 1

    return res

def union_query(doc_list1, doc_list2):
    # TODO: you might like to use a function like this 
    # in your run_boolean_query implementation
    # for full marks this should be the O(n + m) union algorithm for sorted lists
    # using data structures such as sets or dictionaries in this function will not score full marks
    # record the position of element in two doc_lists
    pos1 = 0
    pos2 = 0
    len1 = len(doc_list1)
    len2 = len(doc_list2)
    res = []

    while pos1 < len1 and pos2 < len2:
        # always save element
        # check all element one by one
        if doc_list1[pos1] < doc_list2[pos2]:
            # save element
            res.append(doc_list1[pos1])
            # element in doc_list1 go to the next position
            pos1 += 1
        elif doc_list1[pos1] > doc_list2[pos2]:
            # save element
            res.append(doc_list2[pos2])
            pos2 += 1
        else:
            # save element
            res.append(doc_list1[pos1])
            # check subsequent element
            pos1 += 1
            pos2 += 1
    
    # if one list has more element than others, also need to include them

    while pos1 < len1:
        res.append(doc_list1[pos1])
        pos1 += 1
    while pos2 < len2:
        res.append(doc_list2[pos2])
        pos2 += 1

    return res

def run_boolean_query(query, index):
    """Runs a boolean query using the index.

    Args:
        query (str): boolean query string
        index (dict(str : list(tuple(int, int)))): The index aka dictionary of posting lists

    Returns:
        list(int): a list of doc_ids which are relevant to the query
    """
    
    relevant_docs = []
    
    # tokenize the query to get a list
    tok = tokenize_text(query)
    lentok = len(tok)
    # save first query item doc_id
    relevant_docs = [i[0] for i in index[tok[0]]]
    # initial position
    pos = 2

    while pos < lentok:
        # check next element
        
        doc_id = [i[0] for i in index[tok[pos]]]
        
        #check whether the previous item is AND or OR
        if tok[pos-1] == 'OR':
            relevant_docs = union_query(relevant_docs, doc_id)
        else:
            relevant_docs = intersect_query(relevant_docs, doc_id)
        pos += 2

    return relevant_docs


# load the stored index
(index, doc_freq, doc_ids, num_docs) = pickle.load(open("stored_index.pik", "rb"))

print("Index length:", len(index))
if len(index) != 906290:
    print("Warning: the length of the index looks wrong.")
    print("Make sure you are using `process_tokens_original` when you build the index.")
    raise Exception()

# the list of queries asked for in the assignment text
queries = [
    "Welcoming",
    "Australasia OR logistic",
    "heart AND warm",
    "global AND space AND wildlife",
    "engine OR origin AND record AND wireless",
    "placement AND sensor OR max AND speed"
]

# run each of the queries and print the result
ids_to_doc = {v:k for k, v in doc_ids.items()}
for q in queries:
    res = run_boolean_query(q, index)
    res.sort(key=lambda x: ids_to_doc[x])
    print(q)
    for r in res:
        print(ids_to_doc[r])

