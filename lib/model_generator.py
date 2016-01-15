'''
This module has one simple purpose, which is Generate crf model from command line
Notice that template_file and data_file are necessary and need to be prepared by you
while model file is the one to be generated
'''

from subprocess import call

def generate_model(template_file, data_file, model_file):
    '''
    Generate crf model from command line
    '''
    call(["crf_learn", template_file, data_file, model_file])
