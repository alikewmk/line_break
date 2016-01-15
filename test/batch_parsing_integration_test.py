'''
This is the integration test script for multi threading parsing several BIG xml files
'''

from lib.data_preprocessor import prepare_crf_data
from lib.model_generator import generate_model
from lib.batch_processor import multi_processing

if __name__ == '__main__':

    '''
    Integration test for batch parsing
    You need:
    1. A tempate file
    2. Training data folder path
    3. xml files folder path
    4. parsed xml files folder path
    5. number of process
    '''
    print("Integration test for batch parsing")
    # Data Preprocessing from original data folder
    prepare_crf_data("test/data/train_test_data/", "crf_files/train_features")

    # Generate target model
    generate_model("crf_files/final_template", "crf_files/train_features", "crf_files/final_model")

    # set the folder of origial data
    original_folder = "/home/groups/pearl/notes_revised/"

    # set the folder for parsed files
    parsed_file_dir = "/home/groups/pearl/notes_revised_parsed/"

    # Multi process xml files
    multi_processing(11, original_folder, parsed_file_dir)
