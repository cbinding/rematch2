"""
=============================================================================
Package   : rematch2
Module    : FishVocabularyAnnotator.py
Classes   : FishVocabularyAnnotator
Version   : 1.0.0
Project   : 
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : Vocabulary Annotation Tool (VAT) for archaeological texts
Imports   : os, pandas, spacy, rematch2
Example   : va = FishVocabularyAnnotator()
            output = va.annotateText(input_text="abcde", format="csv")
License   : https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History
31/09/2022 CFB Initially created script
07/11/2022 CFB Extended supported entity types
02/02/2023 CFB Support for supplementary patterns passed to base initialisation
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
from rematch2 import BaseAnnotator

# TODO: formats and entity types as internal enums??


class FishVocabularyAnnotator(BaseAnnotator):
    def __init__(self,
                 language="en",
                 entity_types=["NAMEDPERIOD", "MATERIAL", "MARITIME", "EVIDENCE",
                               "EVENTTYPE", "ARCHSCIENCE", "OBJECT", "COMPONENT", "MONUMENT"],
                 periodo_authority_id="p0kh9ds",
                 patterns=[]) -> None:

        super().__init__(language=language, patterns=patterns)
        # TODO: get cleaned unique entity types list

        # using predefined (English language) spaCy pipeline
        # self.__pipeline = spacy.load("en_core_web_sm", disable=['ner'])

        # conditionally add rematch2 component(s) to the end of the pipeline
        # in order specified in init (allows user-specified order)
        for entity_type in list(map(lambda s: (s or "").strip().upper(), entity_types)):
            if (entity_type == "NAMEDPERIOD"):
                self._pipeline.add_pipe("namedperiod_ruler", last=True, config={
                    "periodo_authority_id": periodo_authority_id})
            elif (entity_type == "ARCHSCIENCE"):
                self._pipeline.add_pipe("fish_archscience_ruler", last=True)
            elif (entity_type == "EVIDENCE"):
                self._pipeline.add_pipe("fish_evidence_ruler", last=True)
            elif (entity_type == "EVENTTYPE"):
                self._pipeline.add_pipe("fish_eventtype_ruler", last=True)
            elif (entity_type == "MATERIAL"):
                self._pipeline.add_pipe("fish_material_ruler", last=True)
            elif (entity_type == "MARITIME"):
                self._pipeline.add_pipe("fish_maritime_ruler", last=True)
            elif (entity_type == "OBJECT"):
                self._pipeline.add_pipe("fish_archobject_ruler", last=True)
            elif (entity_type == "COMPONENT"):
                self._pipeline.add_pipe("fish_component_ruler", last=True)
            elif (entity_type == "MONUMENT"):
                self._pipeline.add_pipe("fish_monument_ruler", last=True)
            else:
                warnings.warn(
                    f"unknown entity type '{entity_type}' in initialisation")

    @staticmethod
    def _to_html(doc):
        # convert results to HTML formatted string (override and call base method)

        # specify colours for HTML output
        options = {
            "ents": [
                "NAMEDPERIOD",
                "EVIDENCE",
                "MATERIAL",
                "MARITIME",
                "ARCHSCIENCE",
                "EVENTTYPE",
                "OBJECT",
                "COMPONENT",
                "MONUMENT"
            ],
            "colors": {
                "NAMEDPERIOD": "lightpink",
                "EVIDENCE": "beige",
                "MATERIAL": "lightgreen",
                "MARITIME": "steelblue",
                "ARCHSCIENCE": "lightblue",
                "EVENTTYPE": "cyan",
                "OBJECT": "yellow",
                "COMPONENT": "yellow",
                "MONUMENT": "salmon"
            }
        }
        output = super(FishVocabularyAnnotator, FishVocabularyAnnotator)._to_html(
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
    anno = FishVocabularyAnnotator()
    print(anno.pipe_names)

    output = anno.annotateText(input_text=txt1, format="dataframe")
    print(output)
