import resource
import re

class XMLStreamParser:

    '''
    Parse specified element in a BIG xml file
    '''

    def __init__(self, source_file, tag):
        self.source_file = source_file
        self.tag = tag

    def parse(self):
        '''
        Parse text in a specific tag
        '''
        with open(self.source_file) as input_file:
            for line in input_file:

                # TODO: check memory usage on server
                # print resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

                if re.search('<' + self.tag + '>', line):

                    # parse code goes to here
                    regexp = re.compile('<' + self.tag + '>' + '(.*)' + '</' + self.tag + '>')
                    text = regexp.search(line).groups(0)[0]
                    # TODO: parse text using CRF parser
                    new_text = "Hello World!"
                    new_line = re.sub(text, new_text, line)
                    yield new_line
                else:
                    yield line

    def parse_and_write_to(self, output_file):
        '''
        Write parsed element to output file
        Write to file without buffer
        '''
        with open(output_file, "w+", 0) as file:
            for line in self.parse():
                file.write(line)

# TEST
if __name__ == '__main__':

    parser = XMLStreamParser("../data/hno_notes.xml", "NOTE_TEXT")
    parser.parse_and_write_to("result.xml")




