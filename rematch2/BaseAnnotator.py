"""
=============================================================================
Package   : rematch2
Module    : BaseAnnotator.py
Classes   : BaseAnnotator
Version   : 20231027
Project   : 
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : base class used for VocabularyAnnotator and TemporalAnnotator
Imports   : os, pandas, spacy, argparse
Example   : 
License   : https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History
31/09/2022 CFB Initially created script
02/02/2023 CFB use of supplementary patterns passed in during init
27/10/2023 CFB type hints added for function signatures
=============================================================================
"""
import os
from os.path import exists
#from collections.abc import MutableSequence
import pandas as pd                     # for DataFrame output
import spacy
from spacy.tokens import Doc
from spacy import displacy              # for HTML formatting results
import argparse                         # for argument parsing

if __package__ is None or __package__ == '':
    # uses current directory visibility
    from Util import *
    from DocSummary import DocSummary
else:
    from .Util import *
    from .DocSummary import DocSummary

# base class for VocabularyAnnotator and TemporalAnnotator
class BaseAnnotator():
    def __init__(self, language: str="en", patterns: list=[]) -> None:
        # start with predefined language-specific spaCy pipeline        
        self._pipeline = get_pipeline_for_language(language)

        # append any additional patterns passed in (for local customisation)
        if (len(patterns or []) > 0):
            ruler = self._pipeline.add_pipe("span_ruler", last=True)
            ruler.initialize(lambda: [], nlp=self._pipeline, patterns=patterns)


    # process text using the modified pipeline
    def __annotate(self, input_text: str="") -> Doc:
        doc = self._pipeline(input_text)
        return doc

    @property
    def pipe_names(self) -> list:
        return self._pipeline.pipe_names

    # process text and output results to specified format
    def annotateText(self, input_text: str="", output_format: str="csv", options: dict=None) -> str|list:
        output = ""

        # data cleansing stages on input text
        # cleaned = input_text.strip()
        # remove any punctuation before annotation DOESN'T WORK for unicode punctuation though, only ASCII
        # cleaned = cleaned.translate(str.maketrans("", "", string.punctuation))
        # this does handle unicode
        # cleaned = regex.sub('[\p{P}\p{Sm}]+', '', cleaned)
        # problem though - if we strip punctuation here we lose crucial info before the NER e.g. full stops...

        # normalise white space before annotation
        # (extra spaces frustrate pattern matching)
        cleaned = normalize_whitespace(input_text)

        # perform the annotation
        doc = self.__annotate(cleaned)

        # convert the results to the required format
        match output_format.strip().lower():
            case "html":                
                output = DocSummary(doc).doctext(format="html")
            #case "ttl":
                #output = self.__doc_to_ttl(doc)
            case "json":
                output = DocSummary(doc).spans(format="json")
            case "text":
                output = DocSummary(doc).spans(format="text")
            case "dataframe":
                output = DocSummary(doc).spans(format="dataframe")
            case "csv":
                output = DocSummary(doc).spans(format="csv")
            case _:
                output = DocSummary(doc).spans()

        return output


    # process single text file
    def annotateFile(inputFileNameWithPath: str = "", output_format: str = "csv", encoding: str = "utf-8-sig"):
        txt = ""

        # open and read text file
        with open(inputFileNameWithPath, 'r', encoding=encoding) as f:
            txt = f.read()

        # process text file contents
        output = self.annotateText(txt, output_format)
        return output
