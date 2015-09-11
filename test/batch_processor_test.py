'''
Here we have three processing approaches

- First is the normal method
- Second is the multi-threading method, it is useless in python because of the GIL(global interpreter lock), but it might be useful if our task is heavy IO
- Third is the multi-processing method, it is useful if our task is CPU(calculation) heavy

One should test all three methods on server, setting the proper params according to the available memory capacity and CPU process number, then decide which method to use.
'''

from lib.xml_stream_parser import XMLStreamParser
from Queue     import Queue as TQueue
from threading import Thread
from time import time
import os
import re

from functools import partial
from multiprocessing import Pool
from multiprocessing import Queue as PQueue
from multiprocessing import Process

# Create target dir for parsed files
def create_folder(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)

def parse(input_dir, output_dir, file):
  parser = XMLStreamParser(input_dir + file, "crf_files/final_model", "NOTE_TEXT")
  parser.parse_and_write_to(output_dir + re.sub(".xml", "", file) + "_parsed.xml" )

class XmlParserWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            output_dir, input_dir, file = self.queue.get()
            parse(input_dir, output_dir, file)
            self.queue.task_done()

if __name__ == '__main__':

    ###
    ##
    # Compare multi-processing, multi-threading with normal process time
    ##
    ###

    # set the folder of origial data
    original_folder = "test/data/threading_test/"

    # create folder for parsed files
    parsed_file_dir = "test/data/parsed/"
    create_folder(parsed_file_dir)


    '''
    Part 1 Normal Procedure
    '''
    ts = time()
    for file in os.listdir(original_folder):
        parse(original_folder, parsed_file_dir, file)
    print('Took {}'.format(time() - ts))


    '''
    Part 2 Multi Threading
    Use this procedure if script is IO heavy
    This procedure is probably not useful in this line break task.
    '''
    ts = time()
    # Create a queue to communicate with the worker threads
    queue = TQueue()

    # Create worker threads
    for x in range(8):
        worker = XmlParserWorker(queue)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()

    # Put the tasks into the queue as a tuple
    for file in os.listdir(original_folder):
        if file.endswith(".xml"):
            queue.put((parsed_file_dir, original_folder, file))

    # Causes the main thread to wait for the queue to finish processing all the tasks
    queue.join()
    print('Took {}'.format(time() - ts))

    '''
    Part 3 Multi Processing
    Create 8 threads for each xml file ( Because the CPU has 8 process)
    The basic rule of process number setting is:
    1. If process needed is less than CPU number, set to process number
    2. If process needed is more than CPU number, choose batch number that is in [CPU_num, CPU_num*2)
       e.g: if we have 12 process and 8 CPU, set number to 12 because 8 < 12 < 8*2
            if we have 18 process and 8 CPU, set number to 18/2=9 because  8 < 9  < 8*2
    Use this procedure if script is CPU heavy
    '''
    ts = time()
    files = [f for f in os.listdir(original_folder) if f.endswith('.xml')]
    parse_process = partial(parse, original_folder, parsed_file_dir)
    Pool(8).map(parse_process, files)
    print('Took {}s'.format(time() - ts))
