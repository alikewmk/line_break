'''
This is the integration test script for multi threading parsing several BIG xml files
'''

from lib.data_preprocessor import prepare_crf_data
from lib.model_generator import generate_model
from lib.xml_stream_parser import XMLStreamParser
from lib.word_templaterizer import TemplateGenerator
from lib.cross_validation import *
from multiprocessing import Pool
from functools import partial
from time import time

def parse(input_dir, output_dir, file):
    parser = XMLStreamParser(input_dir + file, "crf_files/final_model", "NOTE_TEXT")
    parser.parse_and_write_to(output_dir + re.sub(".xml", "", file) + "_parsed.xml" )

if __name__ == '__main__':

    '''
    Integration test for parsing
    You need:
    1. A tempate file
    2. Training data folder path
    3. Testing data folder path
    '''
    print("Integration test for parsing")
    # Data Preprocessing from original data folder
    prepare_crf_data("test/data/train_test_data/", "crf_files/train_features")

    ## Generate target model
    generate_model("crf_files/final_template", "crf_files/train_features", "crf_files/final_model")

    # set the folder of origial data
    original_folder = "/home/groups/pearl/wu_hno_notes_revised/"

    # set the folder for parsed files
    parsed_file_dir = "/home/groups/pearl/wu_hno_notes_revised_parsed/"

    files = [f for f in os.listdir(original_folder) if f.endswith('.xml')]
    parse_process = partial(parse, original_folder, parsed_file_dir)
    Pool(11).map(parse_process, files)
