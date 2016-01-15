'''
This is the integration test of all important methods in this package

Note: Please run this script from root folder
'''

from lib.data_preprocessor import prepare_crf_data
from lib.model_generator import generate_model
from lib.xml_stream_parser import XMLStreamParser
from lib.word_templaterizer import TemplateGenerator
from lib.cross_validation import *


if __name__ == '__main__':
    '''
    Integration test for ten fold cross validation
    The final statistic result is stored in result_file
    '''
    print("Integration for ten fold cross validation")
    # Files you need to prepare
    source_data_folder = "test/data/train_test_data/"

    # Files auto generated
    target_data_folder = "test/data/train_data_files/"
    templates_folder   = "test/data/templates/"
    result_file        = "test/data/results.csv"

    ten_fold_data_preparation(source_data_folder, target_data_folder)
    generate_templates(templates_folder)
    batch_get_test_result(result_file, templates_folder, target_data_folder)

    ### These tests is better used in console instead of script
    # top_ten("PPV", result_file)
    # top_ten("TPR", result_file)
    # top_ten("F-Score", result_file)
