'''
A module that gathering methods for
  - test feature template precision and recall of CRF++
  - ten fold cross validation of feature template
'''

from __future__ import division
from word_templaterizer import TemplateGenerator
from model_generator import generate_model
from data_preprocessor import split_corpus
from StringIO import StringIO
import random
import pandas as pd
import prettytable
import CRFPP
import csv
import os
import re

def create_folder(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)

def check_file(file):
    try:
        f = open(file)
    except:
        print file, "file do not exists."

def check_folder(folder):
    try:
        os.listdir(folder)
    except:
        print folder, 'folder do not exists.'

def ten_fold_data_preparation(source_data_folder, data_folder):
    '''
    Preparing ten fold training and testing data from a data source file
    '''
    # check if data files exists
    check_folder(source_data_folder)

    # check if data folder exists, if not, create one
    create_folder(data_folder)

    for i in range(10):
        random.seed(i)
        train_data_file = data_folder + "training_data_fold_" + str(i+1)
        test_data_file  = data_folder + "testing_data_fold_" + str(i+1)
        split_corpus(source_data_folder, train_data_file, test_data_file)

def generate_templates(templates_folder):

    # check if template folder exists, if not, create one
    create_folder(templates_folder)

    generator = TemplateGenerator()
    generator.batch_generate_template(folder=templates_folder)

def ten_fold_test(template_file, data_folder):

    # check if data folder exists
    check_folder(data_folder)

    for i in range(10):
        idx = str(i+1)
        train_data_file = data_folder + "training_data_fold_" + idx
        model_file      = re.sub(".template", "", template_file)
        model_file      = re.sub("(.*/)+", "", model_file)

        # generate training model file
        generate_model(template_file, train_data_file, model_file)
        check_file(model_file)
        test_data_file  = data_folder + "testing_data_fold_" + idx

        # generate result
        for result in get_test_result(model_file, test_data_file):
            yield result

        os.remove(model_file)

def get_test_result(model_file, test_data_file):
    '''
    Get precision and recall statistic data from model and test file
    '''

    check_file(model_file)
    check_file(test_data_file)

    tagger = CRFPP.Tagger("-m " + model_file + " -v 3 -n2")
    gold_standard = []
    with open(test_data_file) as input_file:
        lines = iter(input_file)
        for line in lines:
            line = re.sub("\n+", "", line)
            line = re.sub("[\s]+", " ", line)
            gold_standard.append(line.split(" ")[-1])
            tagger.add(line)
        tagger.parse()

        tp,fp,tn,fn = [0]*4
        feature_num = tagger.size()

        # get confusion matrix and calculate important statistic numbers
        for idx in range(0, feature_num):
            y = gold_standard[idx]
            y_hat = tagger.y2(idx)

            # here NL means new line, NNL means not new line
            if y == "NL"  and y_hat == "NL":
                tp += 1
            if y == "NL"  and y_hat == "NNL":
                fn += 1
            if y == "NNL" and y_hat == "NNL":
                tn += 1
            if y == "NNL" and y_hat == "NL":
                fp += 1

        ppv = tp/(tp + fp)
        tpr = tp/(tp + fn)
        f_score = 2*(ppv*tpr)/(ppv+tpr)

        yield [model_file, tp, fp, fn, tn, ppv, tpr, f_score]

def batch_get_test_result(result_file, templates_folder, data_folder):

    check_folder(data_folder)
    check_folder(templates_folder)

    header = ["Template Name", "TP", "FP", "FN", "TN", "PPV", "TPR", "F-Score"]

    with open(result_file, 'wb', 0) as csvfile:
        result_writer = csv.writer(csvfile, delimiter=',')
        result_writer.writerow(header)

        for file in os.listdir(templates_folder):
            if file.endswith(".template"):
                template_file = templates_folder + file
                for row in ten_fold_test(template_file, data_folder):
                    result_writer.writerow(row)

def top_ten(r_type, result_file):
    '''
    Print top ten test result as a table in console with specified stat data
    '''
    result = pd.read_csv(result_file, sep=",")
    print "\nTop ten in descending order " + r_type
    output = StringIO()
    result.groupby(["Template Name"]).mean().sort([r_type], ascending=False)[:10].to_csv(output, encoding='utf-8', sep=",")
    output.seek(0)
    pt = prettytable.from_csv(output)
    print pt
