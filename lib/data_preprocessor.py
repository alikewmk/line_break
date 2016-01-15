'''
This module is mainly used for preprocessing training data for CRF model from original data in txt or xml format
Note: `txt` is the recommend format for training data
'''

from __future__ import division
from crf_formatter import word_features
from pandas import DataFrame, Series
import pandas as pd
from random import shuffle
import codecs
import time
import re
import os

def prepare_crf_data(dir, output_file, file_names=[]):
    '''
    Parse data in .xml and .txt file to data that can be recognized by crf++ tool
    Export all newly adapted data to output_file
    '''

    # Store transferred data, which is used for crf training
    total_features = DataFrame()

    # Store the begin train time
    begin_train = time.time()

    print("Data preparation begin:\n")

    if len(file_names) > 0:
        files = file_names
    else:
        files = os.listdir(dir)

    for file in files:
        with codecs.open(dir + file, "r", "ISO-8859-1") as f:
            string = f.read()
            if file.endswith(".xml"):
                text = xml_strip(string)
                assert len(text) < len(string)
            elif file.endswith(".txt"):
                text = string
            else: continue

            total_features = pd.concat([total_features, word_features(text)], axis=0)

    # print total training time
    end_train = time.time() - begin_train
    print("Done prepping training data in ", end_train, "seconds")

    # export training data
    total_features.to_csv(output_file, encoding='utf-8', sep="\t", header=False, index=False)
    print "Training features saved"

def split_corpus(files_dir, train_data_file, test_data_file):
    """
    From a original data file directory
    generate 90 percent of training data, 10 percent of testing data
    Then output preprocessed  data to targeted data files
    """
    files = []
    for file in os.listdir(files_dir):
        if file.endswith(".xml") or file.endswith(".txt"):
            files.append(file)

    shuffle(files)
    file_num    = len(files)
    separator   = int(0.9*file_num)
    train_files = files[:separator]
    test_files  = files[separator:]

    prepare_crf_data(files_dir, train_data_file, train_files)
    prepare_crf_data(files_dir, test_data_file, test_files)

def xml_strip(text, tag="report_text"):
    '''
    Used for generate text data from xml file
    This is previously used in preprocessing Trec Med data (and can only be applied to previous training data currently)
    Since I store all new note training data in txt file, it is useless for them
    If one want to use this method please dig into it and make some adaptations
    '''
    old        = text
    report_tag = re.compile("<"+tag+">")
    end_tag    = re.compile("</"+tag+">")
    begin      = report_tag.search(text)
    end        = end_tag.search(text)
    s          = begin.start()+13
    e          = end.start()
    fixed      = text[s:e]
    assert not old == fixed
    return fixed
