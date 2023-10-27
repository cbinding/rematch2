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
from collections.abc import MutableSequence
import pandas as pd                     # for DataFrame output
import spacy
from spacy.tokens import Doc
from spacy import displacy              # for HTML formatting results
import argparse                         # for argument parsing


# base class for VocabularyAnnotator and TemporalAnnotator
class BaseAnnotator():
    def __init__(self, language: str = "en", patterns: MutableSequence = []) -> None:
        # start with predefined language-specific spaCy pipeline
        pipe_name = ""
        match language.strip().lower():
            case "de":
                pipe_name = "de_core_news_sm"   # German
            case "es":
                pipe_name = "es_core_news_sm"   # Spanish
            case "fr":
                pipe_name = "fr_core_news_sm"   # French
            case "it":
                pipe_name = "it_core_news_sm"   # Italian
            case "nl":
                pipe_name = "nl_core_news_sm"   # Dutch
            case "no":
                pipe_name = "nb_core_news_sm"   # Norwegian Bokmal
            case "sv":
                pipe_name = "sv_core_news_sm"   # Swedish
            case _:
                pipe_name = "en_core_web_sm"    # English (default)

        # create the pipeline
        self._pipeline = spacy.load(pipe_name, disable=['ner'])

        # append any additional patterns passed in (for local customisation)
        if (len(patterns or []) > 0):
            self._pipeline.add_pipe(
                "entity_ruler", last=True, config={"patterns": patterns})


    # process text using the modified pipeline
    def __annotate(self, input_text: str="") -> Doc:
        doc = self._pipeline(input_text)
        return doc

    @property
    def pipe_names(self):
        return self._pipeline.pipe_names

    # process text and output results to specified format
    def annotateText(self, input_text: str="", output_format: str="csv"):
        output = ""

        # data cleansing stages on input text
        # cleaned = input_text.strip()
        # remove any punctuation before annotation DOESNT WORK for unicode punctuation though, only ASCII
        # cleaned = cleaned.translate(str.maketrans("", "", string.punctuation))
        # this does handle unicode
        # cleaned = regex.sub('[\p{P}\p{Sm}]+', '', cleaned)
        # problem though - if we strip punctuation here we lose full stops before the NER...

        # normalise white space before annotation
        # (extra spaces frustrate pattern matching)
        cleaned = " ".join(input_text.strip().split())

        # perform the annotation
        doc = self.__annotate(cleaned)

        # convert the results to the required format
        match output_format.strip().lower():
            case "html":
                output = self._to_html(doc)
            case "ttl":
                output = self.__to_ttl(doc)
            case "json":
                output = self.__to_json(doc)
            case "dataframe":
                output = self.__to_dataframe(doc)
            case "csv":
                output = self.__to_csv(doc)
            case _:
                output = doc  # spaCy doc for further processing

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

    # convert results to pandas.DataFrame object
    @staticmethod
    def __to_dataframe(doc: Doc) -> pd.DataFrame:
        data = [{
            "from": ent.start_char,
            "to": ent.end_char - 1,
            "id": ent.ent_id_,
            "text": ent.text,
            "type": ent.label_
        } for ent in doc.ents]

        df = pd.DataFrame(data)
        return df

    # convert results to CSV formatted string,
    # or write to specified CSV file if name supplied

    @staticmethod
    def __to_csv(doc: Doc, fileName: str = None) -> str:
        df = BaseAnnotator.__to_dataframe(doc)
        return df.to_csv(fileName, index=False)

    # convert results to JSON formatted string,
    # or write to specified JSON file if name supplied

    @staticmethod
    def __to_json(doc: Doc, fileName: str = None) -> str:
        df = BaseAnnotator.__to_dataframe(doc)
        return df.to_json(fileName, orient="records")

    # convert results to TTL (Turtle RDF) formatted string
    @staticmethod
    def __to_ttl(doc: Doc, id: str=None) -> str:
        ttl = ""
        if (id is None):
            id = "http://tempuri/mydata"
        # TODO....
        return ttl

    # convert results to python dictionary

    @staticmethod
    def __to_dict(doc: Doc) -> dict:
        df = BaseAnnotator.__to_dataframe(doc)
        return df.to_dict(orient="records")

    # convert results to HTML formatted string

    @staticmethod
    def _to_html(doc: Doc, options = {}) -> str:
        # generate and return HTML marked up text
        # options passed in to specify colours for HTML output
        output = displacy.render(doc, style="ent", options=options)
        return output
