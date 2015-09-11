'''
This module generates word based features in our training data
It is a necessary part of data preprocessing
'''

from string import punctuation as punct
from pandas import DataFrame, Series
import pandas as pd
import re

def word_features(text, gold_standard=True):
    '''
    Generate word features strictly in order of WORD_FEAT_LIST below for each word in original training data
    '''

    WORD_FEAT_LIST  = ["word", "isalpha", "allcaps", 'lowercase', 'titlecase', 'endsWithPunctuation', "startsWithPunctuation", "hasNumbers", "allNum", "new_line_value"]

    feature_list_of_features = list()
    if gold_standard:
        feat_index = Series(WORD_FEAT_LIST)
    else:
        feat_index = Series(WORD_FEAT_LIST[:-1])

    paragraphs = text.split("\n")
    for p in paragraphs:
        words = p.split()
        linelen = len(words)
        if linelen == 0:
            feature_list = ["<BLANKLINE>", False, True, True, False, False, False, False, False, True]
        pointer = 1
        for w in words:
            feature_list = list()
            #Add word itself
            feature_list.append(w)

            #If the word isalpha()
            if w.isalpha():
                feature_list.append(True)
            else:
                feature_list.append(False)

            #if word is all caps
            if w.isupper():
                feature_list.append(True)
            else:
                feature_list.append(False)

            #if word is lowercase
            if w.islower():
                feature_list.append(True)
            else:
                feature_list.append(False)

            #is word titlecase?
            if w[0].isupper() and w[1:].islower():
                feature_list.append(True)
            else:
                feature_list.append(False)

            #Ends in punctuation
            if w[-1] in punct:
                feature_list.append(True)
            else:
                feature_list.append(False)

            if w[0] in punct:
                feature_list.append(True)
            else:
                feature_list.append(False)

            #Has digits
            nodigit = True
            for idx in range(len(w)):
                if w[idx].isdigit():
                    feature_list.append(True)
                    nodigit = False
                    break
            if nodigit:
                feature_list.append(False)

            #Is only digits:
            if w.isdigit():
                feature_list.append(True)
            else:
                feature_list.append(False)
            if gold_standard:
                if pointer == linelen:
                    feature_list.append("NL")
                else:
                    feature_list.append("NNL")
                    pointer += 1
            features = Series(feature_list)
            feature_list_of_features.append(features)

    df = pd.concat(feature_list_of_features, axis=1)
    df.index = feat_index
    return df.T

def char_features(char_list, gold_standard=True):
    CHAR_FEAT_LIST  = ["isAlpha", "isNumeric", "isPunct", "isUpper", "isLower", "is<sp>", "char", "new_line_value"]

    assert isinstance(char_list, list)

    #If the data contains an oracle label, include that label in the features table
    if gold_standard:
        feat_index = Series(CHAR_FEAT_LIST)
    else:
        feat_index = Series(CHAR_FEAT_LIST[:-1])

    feature_list_of_series = list()
    for i in range(len(char_list)):
        featurelist = list()

        #is character alpha?
        if char_list[i].isalpha():
            featurelist.append(True)
        else:
            featurelist.append(False)

        #is character a digit?
        if char_list[i].isdigit():
            featurelist.append(True)
        else:
            featurelist.append(False)

        #is character punctuation?
        if char_list[i] in punct and not ((char_list[i] is '*') or (char_list[i] is '[') or (char_list[i] is ']')):
            featurelist.append(True)
        else:
            featurelist.append(False)

        #is character in uppercase?
        if char_list[i].isupper():
            featurelist.append(True)
        else:
            featurelist.append(False)

        #is character in lowercase?
        if char_list[i].islower():
            featurelist.append(True)
        else:
            featurelist.append(False)

        #is character blank?
        if (char_list[i] == " "):
            featurelist.append(True)
            char_list[i] = "<sp>"
            store = "NNL"

        #is character new_line?
        elif char_list[i] =="\n":
            if gold_standard:
                char_list[i] = "<sp>"
                featurelist.append(True)
                char_list[i] = "<sp>"
                store = "NL"
            else:
                featurelist.append(False)
        else:
            featurelist.append(False)
            store = "NNL"

        #Add character (at the end 'cause we changed it)
        featurelist.append(str("'"+char_list[i]+"'"))

        #Add oracle label
        if gold_standard:
            featurelist.append(store)

        features = Series(featurelist)
        feature_list_of_series.append(features)

    df = pd.concat(feature_list_of_series, axis=1)
    df.index = feat_index
    return df.T
