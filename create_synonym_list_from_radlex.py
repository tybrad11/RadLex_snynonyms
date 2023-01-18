#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 12:33:04 2019

Read in the findings/indications, and do text clean up (eg, synonym analysis,
changing date formats, etc).

@author: tjb129
"""

import pandas as pd
import os
import re
import string
from nlp_utils import *

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk import ngrams, FreqDist


def isnan(val):
    return val != val

def add_radlex_synonyms():
    #read radlex
    radlex_direct = 'H:\Data\Python Projects Local\Radlex'
    radlex_file  = 'Radlex.xls'
    radlex_sheet = 'RADLEX (4)'
    df_radlex = pd.read_excel(os.path.join(radlex_direct, radlex_file), radlex_sheet)

    words_direct = 'H:\Data\Python Projects Local\Radlex'
    words_file  = 'all_words_used.csv'
    df_words = pd.read_csv(os.path.join(words_direct, words_file))

    #read in list of most common words, find if they are contained in radlex. the grab synonyms
    list_words_and_synonyms = []

    for word in df_words['words']:
            for ind, radlex_word in enumerate(df_radlex['Preferred Label']):
                if word == radlex_word:
                    if not isnan(df_radlex['Synonyms'][ind]):
                        synonym = df_radlex['Synonyms'][ind]
                        if '|' in synonym:
                            synonyms = synonym.split('|')
                            list_words_and_synonyms.append([word, synonyms])
                        else:
                            list_words_and_synonyms.append([word, synonym])
    df_words_and_synonyms = pd.DataFrame(list_words_and_synonyms, columns=['word', 'synonyms'])
    df_words_and_synonyms.to_excel(os.path.join(words_direct, 'words_and_their_synonyms.xlsx'), sheet_name='v1')

    #now n-gram analysis
    ngrams_direct = 'H:\Data\Python Projects Local\Radlex'
    ngrams_file  = 'ngram_analysis.xlsx'
    df_ngrams = pd.read_excel(os.path.join(ngrams_direct, ngrams_file))

    list_ngrams_and_synonyms = []
     for ngram in df_ngrams['2']:
            for ind, radlex_word in enumerate(df_radlex['Preferred Label']):
                if ngram == radlex_word:
                    if not isnan(df_radlex['Synonyms'][ind]):
                        synonym = df_radlex['Synonyms'][ind]
                        if '|' in synonym:
                            synonyms = synonym.split('|')
                            list_ngrams_and_synonyms.append([ngram, synonyms])
                        else:
                            list_ngrams_and_synonyms.append([ngram, synonym])

    df_ngrams_and_synonyms = pd.DataFrame(list_ngrams_and_synonyms, columns=['ngrams', 'synonyms'])
    df_ngrams_and_synonyms.to_excel(os.path.join(ngrams_direct, 'ngrams_and_their_synonyms.xlsx'), sheet_name='v1')
