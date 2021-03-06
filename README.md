### line_break

This repository is an adaptation of [line_break](https://github.com/allisons/line_break) written by [Allison Sliter](https://github.com/allisons)

#### Purpose

The purpose of this package is to applying CRF learning to right formatted files with proper line breaks, and then predict the best place for those new lines to go in the target file.

#### Basic procedures

The script will then begin by taking that set of text-only files and extracting the word features from it and outputting those features in the format required by [CRF++](http://taku910.github.io/crfpp/)

The next step it will do is take those training features, the template you passed to it, and call CRF++'s train command and create you a model.  It'll show you its progress as it goes along.

After that model has been created, the script will use crf_test and the model to predict new labels.  It outputs the same table-format that it requires as input with the additional column for the predicted label.

The next step will be to take those predicted labels and use them to recreate the text-based files that will hopefully look like the training file.

#### Data

- For training purpose, please use `txt` format files with text you want to train on in it gathered in a directory, xml is not fully supported in this package
- For test and predict purpose, please use `xml` format files with text you want to test/predict on gathered in a directory, txt is not fully supported in this package

#### Usage

All usages have examples under `test` directory

*Under intergration test*

- Parsing one BIG xml file (Add line break)

- Ten Fold Cross Validation of CRF templates

- Batch parsing BIG xml file

*Under unit test*

- Batch Process xml files

- Line break test

#### Bug Reports

If encountered problems during usage, please fire an issue.
