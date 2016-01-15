'''
Module consists of methods used in multi processing xml files
'''

from xml_stream_parser import XMLStreamParser
from multiprocessing import Pool
from functools import partial
import os
import re

def create_folder(folder):
    '''
    Create target dir for parsed files
    '''
    if not os.path.exists(folder):
        os.mkdir(folder)

def parse(input_dir, output_dir, file):
    '''
    This is a fixed parse procedure
    One should manually change this function if you want a different parse procedure
    '''
    create_folder(output_dir)
    parser = XMLStreamParser(input_dir + file, "crf_files/final_model", "NOTE_TEXT")
    parser.parse_and_write_to(output_dir + re.sub(".xml", "", file) + "_parsed.xml" )

def multi_processing(process_num, input_dir, output_dir):
    '''
    The basic rule of batch number setting is:
    1. If processes needed is less than CPU number, set to process number
    2. If processes needed is more than CPU number, choose a batch number that is in [CPU_num, CPU_num*2)
       e.g: if we have 12 processes and 8 CPU, set number to 12 because 8 <= 12 < 8*2
            if we have 18 processes and 8 CPU, set number to 18/2=9 because  8 <= 9 < 8*2
    '''
    files = [f for f in os.listdir(input_dir) if f.endswith('.xml')]
    parse_process = partial(parse, input_dir, output_dir)
    Pool(process_num).map(parse_process, files)
