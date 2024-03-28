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
                output = DocSummary(doc).doctext(format="html", options=options) #self.__doc_to_html(doc, options)
            #case "ttl":
                #output = self.__doc_to_ttl(doc)
            case "json":
                output = DocSummary(doc).spans(format="json") #self.__doc_to_json(doc)
            case "text":
                output = DocSummary(doc).spans(format="text")
            #case "dataframe":
                #output = DocSummary(doc).entities("html") #self.__doc_to_dataframe(doc)
            case "csv":
                output = DocSummary(doc).spans(format="csv") #self.__doc_to_csv(doc)
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

'''
    # convert results to pandas.DataFrame object
    @staticmethod
    def __doc_to_dataframe(doc: Doc) -> pd.DataFrame:
        data = [{
            "from": ent.start_char,
            "to": ent.end_char - 1,
            "id": ent.ent_id_,
            "text": ent.text,
            "type": ent.label_
        } for ent in doc.ents]

        pd.set_option('display.max_colwidth', None)
        df = pd.DataFrame(data)
        
        return df


    # convert results to CSV formatted string,
    # or write to specified CSV file if name supplied
    @staticmethod
    def __doc_to_csv(doc: Doc, fileName: str = None) -> str:
        df = BaseAnnotator.__doc_to_dataframe(doc)
        return df.to_csv(fileName, index=False)


    # convert results to JSON formatted string,
    # or write to specified JSON file if name supplied
    @staticmethod
    def __doc_to_json(doc: Doc, fileName: str = None) -> str:
        df = BaseAnnotator.__doc_to_dataframe(doc)
        return df.to_json(fileName, orient="records")


    # convert results to TTL (Turtle RDF) formatted string
    @staticmethod
    def __doc_to_ttl(doc: Doc, id: str=None) -> str:
        ttl = ""
        if (id is None):
            id = "http://tempuri/mydata"
        # TODO....
        return ttl


    # convert results to python dictionary
    @staticmethod
    def __doc_to_dict(doc: Doc) -> dict:
        df = BaseAnnotator.__doc_to_dataframe(doc)
        return df.to_dict(orient="records")


    # convert results to HTML formatted string
    @staticmethod
    def __doc_to_html(doc: Doc, options = None) -> str:
        # generate and return HTML marked up text
        # options passed in to specify colours for HTML output
        # default options if none passed in
        if options is None:
            options = {
                "ents": None, # so all are displayed
                "colors": {
                    "CENTURY": "lightgreen",
                    "YEARSPAN": "moccasin",
                    "PERIOD": "yellow",
                    "MONUMENT": "cyan",
                    "OBJECT": "plum",
                    "ARCHSCIENCE": "lightpink",
                    "EVIDENCE": "aliceblue",
                    "MATERIAL": "antiquewhite",
                    "EVENTTYPE": "coral",
                    "NEGATION": "lightgray"
                }
            }
        output = displacy.render(doc, style="ent", options=options)
        return output
'''