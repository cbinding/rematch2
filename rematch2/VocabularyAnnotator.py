"""
=============================================================================
Project   : ARIADNEplus
Package   : rematch2
Module    : VocabularyAnnotator.py
Classes   : VocabularyAnnotator
Version   : 1.0.0
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : Vocabulary Annotation Tool for archaeological texts
Imports   : os, pandas, spacy, rematch2
Example   : va = VocabularyAnnotator()
            output = va.annotateText(input_text="abcde", format="csv")
License   : https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History
05/10/2023 CFB New component AAT annotator based on FISH annotator
23/10/2023 CFB Changed to generic vocabulary annotator, pass in vocab
=============================================================================
"""
import os
from os.path import exists
import json
import pandas as pd                     # for DataFrame output
import spacy
from spacy.tokens import Doc
from spacy import displacy              # for HTML formatting results
import argparse                         # for argument parsing
# from rematch2 import components         # spaCy pipeline components
# from rematch2 import BaseAnnotator
#from components import BaseAnnotator

#from .BaseAnnotator import BaseAnnotator
if __package__ is None or __package__ == '':
    # uses current directory visibility
    from BaseAnnotator import BaseAnnotator
    from VocabularyRuler import create_vocabulary_ruler
else:
    # uses current package visibility
    from .BaseAnnotator import BaseAnnotator
    from .VocabularyRuler import create_vocabulary_ruler

# TODO: formats and entity types as internal enums??


class VocabularyAnnotator(BaseAnnotator):
    def __init__(self,
                 language="en",
                 min_lemmatize_length=4,
                 min_term_length=3,
                 lemmatize=True,
                 pos=[],
                 default_label="OBJECT",
                 default_language="en",
                 vocabulary=[],
                 patterns=[]) -> None:

        super().__init__(language=language, patterns=patterns)

        # using predefined (English language) spaCy pipeline
        # self.__pipeline = spacy.load("en_core_web_sm", disable=['ner'])
        self._pipeline.add_pipe("vocabulary_ruler", last=True, config={
            "min_lemmatize_length": min_lemmatize_length,
            "min_term_length": min_term_length,
            "lemmatize": lemmatize,
            "pos": pos,
            "default_label": default_label,
            "default_language": default_language,
            "vocabulary": vocabulary})

    @staticmethod
    def _load_vocab_from_json_file(file_path):
        pass

    @staticmethod
    def _load_vocab_from_json_url(url):
        pass

    @staticmethod
    def _to_html(doc):
        # convert results to HTML formatted string (override and call base method)

        # specify colours for HTML output
        options = {
            "ents": [
                "ACTIVITY",
                "AGENT",
                "MATERIAL",
                "OBJECT",
                "STYLEPERIOD",
                "NAMEDPERIOD",
                "EVIDENCE",
                "MARITIME",
                "ARCHSCIENCE",
                "EVENTTYPE",
                "COMPONENT",
                "MONUMENT"
            ],
            "colors": {
                "ACTIVITY": "lightpink",
                "AGENT": "beige",
                "MATERIAL": "lightgreen",
                "OBJECT": "yellow",
                "STYLEPERIOD": "salmon",
                "NAMEDPERIOD": "lightgray",
                "EVIDENCE": "beige",
                "MARITIME": "steelblue",
                "ARCHSCIENCE": "lightblue",
                "EVENTTYPE": "cyan",
                "COMPONENT": "yellow",
                "MONUMENT": "salmon"
            }
        }
        output = super(VocabularyAnnotator, VocabularyAnnotator)._to_html(
            doc, options=options)
        # output = BaseAnnotator()._to_html(doc, options=options)
        # generate and return HTML marked up text
        # output = displacy.render(doc, style="ent", options=options)
        return output


if __name__ == "__main__":
    DEFAULT_FORMAT = "csv"
    # initiate the input arguments parser
    parser = argparse.ArgumentParser(
        prog=__file__, description="Find entities in text")

    # add long and short argument descriptions
    parser.add_argument("--inputfilename", "-n", required=False,
                        help="Input file name")

    parser.add_argument("--inputtext", "-t", required=False,
                        help="Input text")

    parser.add_argument("--format", "-f", required=False,
                        default=DEFAULT_FORMAT, help="Required output format")

    # parse command line arguments
    args = parser.parse_args()

    # get clean required arguments
    inputFileName = ""
    inputText = ""
    format = DEFAULT_FORMAT

    if args.inputfilename:
        inputFileName = args.inputfilename.strip()

    if args.inputtext:
        inputText = args.inputtext.strip()

    if args.format:
        format = args.format.strip().lower()

    # temp for testing - example input text from https://doi.org/10.5284/1100095
    txt1 = """
    This collection comprises site data (images and CAD) from an archaeological evaluation which was undertaken by Cotswold Archaeology in October 2015 at Knotwood Fields Farm, Northamptonshire. The evaluation was undertaken to inform a planning application to South Northamptonshire Council (SNC; the local planning authority) for the development of a solar farm. The fieldwork comprised the excavation of fourteen trenches. A previous geophysical survey identified a number of anomalies representing potential archaeological features; these comprised sub-circular anomalies, linear anomalies and back-filled pits, indicative of former settlement activity of probable late prehistoric to Roman date. The evaluation recorded a number of curvilinear ditches, which most likely represent small enclosures and a roundhouse. Pottery dating from the Iron Age was recovered from the silted fills of these ditches. Broadly contemporaneous boundary ditches, containing pottery dating to the Iron Age, were also identified. These features probably relate to settlement activity and land division, focused at the north-eastern end of the site. Medieval plough furrows were indicated across the entire site by the geophysical survey; variations in their alignment indicates that the site covers parts two or more former open fields. A number of undated, but probably post-medieval/modern, ditches corresponding to a north-west/south-east oriented field system were identified within the south-eastern part of the site. There was a good correlation between the evaluation and the geophysical survey results, although there were a small number of archaeological features which had not been detected by the survey, as well as limited geophysical anomalies which were not found to correspond to below-ground archaeological remains.
    """
    txt2 = """
    Aside from three residual flints, none closely datable, the earliest remains comprised a small assemblage of Roman pottery and ceramic building material, also residual and most likely derived from a Roman farmstead found immediately to the north within the Phase II excavation area. A single sherd of Anglo-Saxon grass-tempered pottery was also residual.
    The earliest features, which accounted for the majority of the remains on site, relate to medieval agricultural activity focused within a large enclosure. There was little to suggest domestic occupation within the site: the pottery assemblage was modest and well abraded, whilst charred plant remains were sparse, and, as with some metallurgical residues, point to waste disposal rather than the locations of processing or consumption. A focus of occupation within the Rodley Manor site, on higher ground 160m to the north-west, seems likely, with the currently site having lain beyond this and providing agricultural facilities, most likely corrals and pens for livestock. Animal bone was absent, but the damp, low-lying ground would have been best suited to cattle. An assemblage of medieval coins recovered from the subsoil during a metal detector survey may represent a dispersed hoard.
    """

    vocabulary = []
    vocab_dir = os.path.join(os.path.abspath(""), "rematch2/vocabularies")
    file_path = os.path.join(vocab_dir, "vocab_en_AAT_ACTIVITIES_20231018.json")
    with open(file_path, "r") as f:
        vocabulary = json.load(f)

    annotator = VocabularyAnnotator(min_lemmatize_length=4,
                                    min_term_length=3,
                                    lemmatize=True,
                                    pos=["NOUN"],
                                    default_label="OBJECT",
                                    default_language="en",
                                    vocabulary=vocabulary)

    # print(annotator.pipe_names)
    output = annotator.annotateText(input_text=txt1, format="dataframe")
    print(output)