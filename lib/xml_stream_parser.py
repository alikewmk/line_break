import resource
import re
from crf_formatter import word_features
import CRFPP
from cStringIO import StringIO

#### Define irregular char regexp constant
# Abnormal line break
ABNORMAL_LINE_BREAK = re.compile("\n+\s+")
# Remove unused HTML coded char
# According to The HTML Coded Character Set in http://www.w3.org/MarkUp/html-spec/html-spec_13.html
INVALID_HTML_CODED_CHARACTERS = re.compile('&#(0[0-8]|1[1-2]|1[4-9]|2[0-9]|3[0-1]|12[7-9]|1[3-5][0-9]);')

class XMLStreamParser:
    '''
    Parse specified element in a BIG xml file
    '''
    def __init__(self, source_file, model_file, tag):
        self.source_file = source_file
        self.tag = tag
        self.tagger = CRFPP.Tagger("-m " + model_file + " -v 3 -n2")

    def add_line_break(self, text):

        # because write to a pseudo file is much faster
        # here we use StringIO instead of string concatenation
        new_text = StringIO()

        # generate features for each word to predict if there is a line break after the word
        # split text by blank
        features = word_features(text).values
        for row in features:
            feature_string = " ".join([str(i) for i in row])
            self.tagger.add(feature_string)

        # generate prediction
        self.tagger.parse()

        # change text according to prediction
        for idx in range(0, len(features)):
            new_text.write(features[idx][0])
            # If the word has new line after it, add new line
            # else add whitespace after word
            if self.tagger.y2(idx) == "NL":
                new_text.write("\n\n")
            else:
                new_text.write(" ")

        # clear parsed words
        self.tagger.clear()

        # to join string afterwards is more efficient in python
        return new_text.getvalue()

    def parse(self):
        '''
        Parse text in a specific tag
        '''
        with open(self.source_file) as input_file:
            lines = iter(input_file)
            for line in lines:

                # TODO: check memory usage on server
                # print resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

                if re.search('<' + self.tag + '>', line):
                    # avoid line breaks with no purpose
                    text_line = line
                    while not re.search('</' + self.tag + '>', text_line):
                        text_line += (" " + lines.next())

                    text_line = self.remove_irrgular_char(text_line)

                    # get the text that need to be parsed
                    regexp = re.compile('<' + self.tag + '>' + '(.*)' + '</' + self.tag + '>')
                    text = regexp.search(text_line).groups(0)[0]

                    # add line break to target text
                    new_text = self.add_line_break(text)
                    new_line = text_line.replace(text, new_text, 1)
                    yield new_line
                else:
                    yield line

    def remove_irrgular_char(self, text_line):
        text_line = ABNORMAL_LINE_BREAK.sub(" ", text_line)
        text_line = INVALID_HTML_CODED_CHARACTERS.sub("", text_line)
        return text_line

    def parse_and_write_to(self, output_file):
        '''
        Write parsed element to output file
        Write to file without buffer
        '''
        with open(output_file, "w+", 0) as file:
            for line in self.parse():
                file.write(line)
