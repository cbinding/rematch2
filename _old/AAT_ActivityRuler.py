"""
=============================================================================
Package :   rematch2
Module  :   AAT_ActivityRuler.py
Version :   20231004
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy custom pipeline component (specialized EntityRuler)
            to identify Terms from the Getty AAT Activities Facet in free text. 
            Entity type added will be "AAT_ACTIVITY"
Imports :   os, sys, spacy, Language, PatternRuler
Example :   nlp.add_pipe("aat_activity_ruler", last=True)           
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
History :   04/10/2023 CFB Initially created script
=============================================================================
"""
import os
import sys
import spacy            # NLP library

from spacy.language import Language

# from ..spacypatterns import patterns_en_AAT_ACTIVITIES
from ..spacypatterns import vocab_en_AAT_ACTIVITIES
# from .PatternRuler import PatternRuler
from .BaseRuler import create_base_ruler

# @Language.factory("aat_activity_ruler")
# def create_aat_activity_ruler(nlp, name="aat_activity_ruler", patterns=patterns_en_AAT_ACTIVITIES):
# return PatternRuler(nlp, name, patterns)


@Language.factory("aat_activity_ruler")
def create_aat_activity_ruler(nlp, name="aat_activity_ruler"):
    return create_base-ruler(nlp, name=name, label="AAT_ACTIVITY", language="en", vocab=vocab_en_AAT_ACTIVITIES)


# test the AAT_ActivityRuler class
if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm", disable=['ner'])
    nlp.add_pipe("aat_activity_ruler", last=True)
    text = '''
    Aside from three residual flints, none closely datable, the earliest remains comprised a small assemblage of Roman pottery \
    and ceramic building material, also residual and most likely derived from a Roman farmstead found immediately to the north \
    within the Phase II excavation area. A single sherd of Anglo-Saxon grass-tempered pottery was also residual. The earliest \
    features, which accounted for the majority of the remains on site, relate to medieval agricultural activity focused within \
    a large enclosure. There was little to suggest domestic occupation within the site: the pottery assemblage was modest and \
    well abraded, whilst charred plant remains were sparse, and, as with some metallurgical residues, point to waste disposal \
    rather than the locations of processing or consumption. A focus of occupation within the Rodley Manor site, on higher ground \
    160m to the north-west, seems likely, with the currently site having lain beyond this and providing agricultural facilities, \
    most likely corrals and pens for livestock. Animal bone was absent, but the damp, low-lying ground would have been best suited \
    to cattle. An assemblage of medieval coins recovered from the subsoil during a metal detector survey may represent a dispersed hoard.
    '''
    doc = nlp(text)
    for ent in doc.ents:
        print(ent.ent_id_, ent.text, ent.label_)
