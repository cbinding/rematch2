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

from spacy.tokens import Doc
from spacy.pipeline import SpanRuler
from .Util import *
from .DocSummary import DocSummary
from .TextNormalizer import *


# base class for VocabularyAnnotator and TemporalAnnotator
class BaseAnnotator():
    def __init__(self, language: str="en", patterns: list=[]) -> None:
        # start with predefined language-specific spaCy pipeline        
        self._pipeline = get_pipeline_for_language(language)
        self._pipeline.add_pipe("normalize_text", before="tagger")  
        # append any additional patterns passed in (for local customisation)
        if (len(patterns or []) > 0):
            self._pipeline.add_pipe("vocabulary_ruler", before="tagger", config={"patterns": patterns}) 
            #ruler: SpanRuler = self._pipeline.add_pipe("span_ruler", last=True)
            #ruler.add_patterns(patterns)


    # process text using the modified pipeline
    def __annotate(self, input_text: str="") -> Doc:
        doc = self._pipeline(input_text)
        return doc

    @property
    def pipe_names(self) -> list:
        return self._pipeline.pipe_names

    # process text and output results to specified format
    def annotateText(self, input_text: str="", output_format: str="csv", options: dict={}):
        output = ""       
        
        # perform the annotation
        doc = self.__annotate(input_text)
        summary = DocSummary(doc)
        
        # convert the results to the required format
        match output_format.strip().lower():
            case "html":                
                output = summary.doctext_to_html()
            #case "ttl":
                #output = self.__doc_to_ttl(doc)
            case "json":
                output = summary.spans_to_json()
            case "text":
                output = summary.spans_to_text()
            case "dataframe":
                output = summary.spans_to_df()
            case "csv":
                output = summary.spans_to_csv()
            case _:
                output = summary.spans

        return output


    # process single text file
    def annotateFile(self, inputFileNameWithPath: str = "", output_format: str = "csv", encoding: str = "utf-8-sig"):
        txt = ""

        # open and read text file
        with open(inputFileNameWithPath, 'r', encoding=encoding) as f:
            txt = f.read()

        # process text file contents
        output = self.annotateText(txt, output_format)
        return output
