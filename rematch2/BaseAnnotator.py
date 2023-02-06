"""
=============================================================================
Project   : ARIADNEplus
Package   : rematch2
Module    : BaseAnnotator.py
Classes   : Annotator
Version   : 1.0.0
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : Annotation Tool base class
Imports   : os, pandas, spacy, rematch2
Example   : 
License   : https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History
31/09/2022 CFB Initially created script
02/02/2023 CFB use of supplementary patterns passed in during init
=============================================================================
"""
import os
from os.path import exists
import pandas as pd                     # for DataFrame output
import spacy
from spacy.tokens import Doc
from spacy import displacy              # for HTML formatting results
import argparse                         # for argument parsing
from rematch2 import components         # spaCy pipeline components


# base class for VocabularyAnnotator and TemporalAnnotator
class BaseAnnotator():
    def __init__(self, language="en", patterns=[]) -> None:
        # start with predefined language-specific spaCy pipeline
        pipeline_name = ""
        if (language == "de"):
            pipeline_name = "de_core_news_sm"   # German
        elif (language == "es"):
            pipeline_name = "es_core_news_sm"   # Spanish
        elif (language == "fr"):
            pipeline_name = "fr_core_news_sm"   # French
        elif (language == "it"):
            pipeline_name = "it_core_news_sm"   # Italian
        elif (language == "nl"):
            pipeline_name = "nl_core_news_sm"   # Dutch
        elif (language == "no"):
            pipeline_name = "nb_core_news_sm"   # Norwegian Bokmal
        elif (language == "sv"):
            pipeline_name = "sv_core_news_sm"   # Swedish
        else:
            pipeline_name = "en_core_web_sm"    # English (default)
        # create the pipeline
        self._pipeline = spacy.load(pipeline_name, disable=['ner'])

        # append any additional patterns passed in (for local customisation)
        if(len(patterns or []) > 0):
            self._pipeline.add_pipe(
                "pattern_ruler", last=True, config={"patterns": patterns})

    # process text using the modified pipeline

    def __annotate(self, input_text="") -> Doc:
        doc = self._pipeline(input_text)
        return doc

    @property
    def pipe_names(self):
        return self._pipeline.pipe_names

    # process text and output results to specified format
    def annotateText(self, input_text="", format="csv"):
        output = ""
        # normalise white spaces before annotation
        # (extra spaces frustrate pattern matching)
        clean_input = " ".join(input_text.split())

        # perform the annotation
        doc = self.__annotate(clean_input)

        # convert the rersults to the required format
        if (format == "html"):
            output = self._to_html(doc)
        elif (format == "ttl"):
            output = self.__to_ttl(doc)
        elif (format == "json"):
            output = self.__to_json(doc)
        elif (format == "dataframe"):
            output = self.__to_dataframe(doc)
        elif (format == "csv"):
            output = self.__to_csv(doc)
        else:
            output = doc  # spaCy doc for further processing

        return output

    # process single text file

    def annotateFile(inputFileNameWithPath="", format="csv", encoding="utf-8-sig"):
        txt = ""

        # open and read text file
        with open(inputFileNameWithPath, 'r', encoding=encoding) as f:
            txt = f.read()

        # process text file contents
        output = self.annotateText(txt, format)
        return output

    # convert results to pandas.DataFrame object

    @staticmethod
    def __to_dataframe(doc) -> pd.DataFrame:
        data = [[ent.ent_id_, ent.text, ent.label_] for ent in doc.ents]
        df = pd.DataFrame(data, columns=["id", "text", "type"])
        return df

    # convert results to CSV formatted string,
    # or write to specified CSV file if name supplied

    @staticmethod
    def __to_csv(doc, fileName=None):
        df = BaseAnnotator.__to_dataframe(doc)
        return df.to_csv(fileName, index=False)

    # convert results to JSON formatted string,
    # or write to specified JSON file if name supplied

    @staticmethod
    def __to_json(doc, fileName=None):
        df = BaseAnnotator.__to_dataframe(doc)
        return df.to_json(fileName, orient="records")

    # convert results to TTL (Turtle RDF) formatted string
    @staticmethod
    def __to_ttl(doc, id=None):
        ttl = ""
        if (id is None):
            id = "http://tempuri/mydata"
        # TODO....
        return ttl

    # convert results to python dictionary

    @staticmethod
    def __to_dict(doc):
        df = BaseAnnotator.__to_dataframe(doc)
        return df.to_dict(orient="records")

    # convert results to HTML formatted string

    @staticmethod
    def _to_html(doc, options={}):
        # options passed in specify colours for HTML output
        # generate and return HTML marked up text
        output = displacy.render(doc, style="ent", options=options)
        return output
