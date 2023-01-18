#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 13:15:14 2019

@author: tjb129
"""

#remove stop words, look at 2-gram and 1-gram

#download packages
# import os
# os.system('pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org pandas')
# os.system('pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org nltk')
# os.system('pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org xlrd')
# os.system('pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org openpyxl')
import nltk
nltk.download('punkt')
nltk.download('stopwords')
import numpy as np

import pandas as pd
import os
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk import ngrams, FreqDist
from nltk.corpus import stopwords
import csv


def create_list_of_word_used_in_csv(csv_file_path, column_name, csv_write_dir, sheet_name, number_of_words_to_write=1000):
    
    direct = 'H:\Data\Python Projects Local\Radlex'
    save_file = 'Pneumothorax_reports.csv'

      # read in full data
    if csv_file_path[-3:] == 'csv':
        df = pd.read_csv(csv_file_path)
    elif csv_file_path[-4:] == 'xlsx':
        df = pd.read_excel(csv_file_path, sheet_name = sheet_name)
    
    ## NGRAM ANALYSIS ##
    #get all words into a single list

    #ignore stop words
    stopwords_list = stopwords.words('english')
    # words_not_excluded = ["won't", "wouldn't", 'or', 'both', 'no', 'not', 'same']  # is, has, or?
    # stopwords_list = list(set(stopwords).difference(set(words_not_excluded)))  # remove words from stopwords list


    full_data = []
    tokenizer = RegexpTokenizer(r'\w+')
    for text_i in df[column_name]:
        if text_i == text_i:  #a way to exclude NaNs
            # text_tok = word_tokenize(text_i)
            text_tok = tokenizer.tokenize(text_i)
            for word in text_tok:
                if word not in stopwords_list:
                    full_data.append(word.lower())
    
    #now do ngram analysis, leaving out ones with periods, save to excel
    number_of_words_to_write = 1000
    all_counts = dict()
    df_ngram = pd.DataFrame()
    for size in 2, 3:  #ngram sizes to analyze
        all_counts[size] = FreqDist(ngrams(full_data, size))
        n_written = 0
        i = 0
        ngrams_i = all_counts[size].most_common(number_of_words_to_write)
        ngrams_list = []
        while n_written < number_of_words_to_write and i < number_of_words_to_write:
            text = ngrams_i[i][0]
            i = i+1
            text_untok = "".join([" "+i if not i.startswith("'") else i for i in text]).strip()  #untokenize
            # text_untok = text_untok[1:]   #remove leading _
            if text_untok.find('.') == -1:   #don't want ones with periods
                ngrams_list.append(text_untok)              
                n_written = n_written + 1        
         
        if len(ngrams_list) < number_of_words_to_write:
            for i in range(len(ngrams_list), number_of_words_to_write):
                ngrams_list.append('nan')
        df_ngram[str(size)] = ngrams_list
    
    ngram_save = 'ngram_analysis.xlsx'
    ngram_sheet = 'ngrams'    
    df_ngram.to_excel(os.path.join(csv_write_dir, ngram_save), sheet_name=ngram_sheet)
    
    
    #save 1-grams
    
    ## Save all of the words used based on frequency ###   
    # all_counts[n].most_common(j) gives j most commone n-length grams
    all_counts[1] = FreqDist(ngrams(full_data, 1))
    words_used = all_counts[1].most_common(5000)

    words_used_list = [['words', 'frequency']]
    for d in words_used:
        freq = d[1]
        w = ''.join(d[0])
        words_used_list.append([w,freq])
    np.savetxt(os.path.join(csv_write_dir, 'words_used.txt'), words_used_list, delimiter=",", fmt='%s')
    with open(os.path.join(csv_write_dir, 'all_words_used.csv'), 'w',newline='') as f:
        writer = csv.writer(f)
        for row in words_used_list:
            writer.writerow(row)
