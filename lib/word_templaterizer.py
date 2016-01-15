"""
This script creates template file for crf++, for the word-based feature structure
"""

# different combination of features
FEATURE_COMBINATIONS = {
    "all_word_features":       ["word", "isalpha", "allcaps", 'lowercase', 'titlecase', 'endsWithPunctuation', "startsWithPunctuation", "hasNumbers", "allNum"],
    "case_features":           ["word", "isalpha", "allcaps", "lowercase", "titlecase", None,                  None,                    None,         None,   ],
    "num_features":            ["word", "isalpha", None,      None,        None,        None,                  None,                    "hasNumbers", "allNum"],
    "punctuation_features":    ["word", "isalpha", None,      None,        None,        "endsWithPunctuation", "startsWithPunctuation", None,         None,   ],
    "case_and_num_features":   ["word", "isalpha", "allcaps", "lowercase", "titlecase", None,                  None,                    "hasNumbers", "allNum"],
    "case_and_punct_features": ["word", "isalpha", "allcaps", "lowercase", "titlecase", "endsWithPunctuation", "startsWithPunctuation", None,         None,   ],
    "num_and_punct_features":  ["word", "isalpha", None,      None,        None,        "endsWithPunctuation", "startsWithPunctuation", "hasNumbers", "allNum"]
}

class TemplateGenerator:

    def temp_feat_str(self, idx, y_axis, x_axis):
        '''
        Generate features of a word with postions relative to the word
        '''
        return 'U{}:%x[{},{}]\n'.format(idx, y_axis, x_axis)

    def generate_template(self, combination, gram_num, folder=""):
        '''
        Generate a template with assigned feature types and gram number
        '''
        # keep track of added feature index
        feature_idx = 0

        # get type of feature sequence from fixed combination hash
        feature_types = FEATURE_COMBINATIONS[combination]

        # generate file name from combination and gram_num
        file_name = combination+"_"+"gram_num_"+str(gram_num)+".template"

        # init content string that should be written to template
        content = "# " + combination + " gram_num = " + str(gram_num) +"\n"

        # iterate through feature type and get features of valid types
        for type_idx, feature_type in enumerate(feature_types):

            # TODO:
            # The feature position is corresponding to the position of training data
            # So keep the position fixed is important!!!
            # it is not the best practice though
            # Should find a better way later

            # if feature in specific position is None, skip feature
            if feature_type == None: continue

            # if not, add feature to template
            content += "# " + feature_type + "\n"
            for num in range(-gram_num, gram_num):
                if feature_idx < 10:
                    current_idx = '0' + str(feature_idx)
                else:
                    current_idx = str(feature_idx)

                content += self.temp_feat_str(current_idx, num, type_idx)
                feature_idx += 1

        with open(folder+file_name, 'wb') as f:
            f.write(content)

    def batch_generate_template(self, combinations=list(FEATURE_COMBINATIONS.keys()), gram_range=list(range(2,7)), folder=""):
        '''
        Batch generate template files for cross validation test
        '''
        for combination in combinations:
            for gram_num in gram_range:
                self.generate_template(combination, gram_num, folder)
