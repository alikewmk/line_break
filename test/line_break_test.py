'''
This is the unit test of line break parsing
The model file is not provided due to safety reasons, if need to run the test on your own machine, please add your own model
under /line_break/crf_files/ and change this test script accordingly

Note: Please run this script from root folder
'''

from lib.xml_stream_parser import XMLStreamParser
import os

def parse_txt_files():
    '''
    This is a hacking way of parsing txt files
    You might find it useful sometimes. :)
    '''
    parser          = XMLStreamParser("", "crf_files/final_model", "")
    note_dir        = "test/data/note_texts"
    parsed_note_dir = "test/data/note_texts_parsed"
    if not os.path.exists(parsed_note_dir):
        os.mkdir(parsed_note_dir)
    for file in os.listdir(note_dir):
        new_string = None
        with open(note_dir + "/" + file) as f:
            if file.endswith(".txt"):
                string = f.read()
                new_string = parser.add_line_break(string)
                with open(parsed_note_dir + "/" + file, "w+") as wf:
                    wf.write(new_string)

def parse_big_xml(model="crf_files/final_model"):
    parser = XMLStreamParser("test/data/fake_hno_notes.xml", model, "NOTE_TEXT")
    parser.parse_and_write_to("test/data/fake_hno_notes_parsed.xml")

if __name__ == '__main__':

    print("Testing txt parsing")
    parse_txt_files()

    print("Testing xml parsing")
    parse_big_xml()

    print("Success!")
