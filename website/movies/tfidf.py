
# coding: utf-8

# In[201]:


import pandas as pd
import numpy as np

import json
import nltk
import string
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
# Tokenizers

def keyword_tokenize(text):
    tokens = text.split('|')
    tokens = list(filter(None, tokens))
    stemmer = PorterStemmer()
    stems = stem_tokens(tokens, stemmer)
    return stems

def text_tokenize(text):
    stemmer = PorterStemmer()
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

# tf-idf
def tf_idf(movies, col_name, tokenizer = None, to_fill = 'mean'):
    tfidf = TfidfVectorizer(tokenizer, stop_words='english')
    to_tfidf = movies[~pd.isnull(movies[col_name])]
    missing_idx = movies[pd.isnull(movies[col_name])].index
    other_idx = movies[~pd.isnull(movies[col_name])].index
    res = tfidf.fit_transform(to_tfidf[col_name])

    ret = np.zeros((movies.shape[0], res.shape[1]))

    if to_fill == 'mean':
        to_fill_missing = np.mean(res, axis = 0)
        to_fill_missing = np.asarray(to_fill_missing)
    elif to_fill == 'zero':
        to_fill_missing = np.zeros(res.shape[1])

    mat = np.tile(to_fill_missing, (missing_idx.shape[0], 1))

    ret[missing_idx, :] = mat
    ret[other_idx, :] = res.toarray()

    return ret
