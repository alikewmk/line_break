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
    Integration test for parsing
    You need:
    1. A tempate file
    2. Training data folder path
    3. Testing data folder path
    '''
    print("Integration test for parsing")
    # Data Preprocessing from original data folder
    prepare_crf_data("test/data/note_texts/", "crf_files/note_train_features")

    # Generate target model
    generate_model("crf_files/final_template", "crf_files/train_features", "crf_files/final_model")

    parser = XMLStreamParser("test/data/fake_notes.xml", "crf_files/final_model", "NOTE_TEXT")
    parser.parse_and_write_to("test/data/fake_notes_parsed.xml")
