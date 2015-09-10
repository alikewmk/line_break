from xml_stream_parser import XMLStreamParser
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
    original_folder = "data/threading_test/"

    # create folder for parsed files
    parsed_file_dir = "data/parsed/"
    create_folder(parsed_file_dir)

    ########################################################
    ### Part 1 Normal
    ts = time()
    for file in os.listdir(original_folder):
        parse(original_folder, parsed_file_dir, file)
    print('Took {}'.format(time() - ts))



    ########################################################
    ### Part 2 Multi Threading
    ### Use this procedure if script is IO heavy

    ts = time()
    # Create a queue to communicate with the worker threads
    queue = TQueue()

    # Create 8 worker threads
    # Create 8 threads for each xml file ( Because the CPU has 8 process?? )
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



    ########################################################
    ### Part 3 Multi Processing
    ### Use this procedure if script is CPU heavy
    ts = time()
    files = [f for f in os.listdir(original_folder) if f.endswith('.xml')]
    parse_process = partial(parse, original_folder, parsed_file_dir)
    Pool(8).map(parse_process, files)
    print('Took {}s'.format(time() - ts))
