from subprocess import call

def generate_model(template_file, data_file, model_file):
    '''
    Generate crf model from command line
    '''
    call(["crf_learn", template_file, data_file, model_file])

