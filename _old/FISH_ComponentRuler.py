"""
=============================================================================
Package :   rematch2.components
Module  :   FISH_ComponentRuler.py
Version :   20221027
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   ARIADNEplus
Summary :   spaCy custom pipeline component (specialized EntityRuler)
            to identify Terms from the HE Components Thesaurus in free text. 
            Entity type added will be "COMPONENT"
Imports :   os, sys, spacy, Language, EntityRuler
Example :   nlp.add_pipe("fish_component_ruler", last=True)           
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
History :   03/08/2022 CFB Initially created script
=============================================================================
"""
import os
import sys
import spacy            # NLP library

from spacy.language import Language

from ..spacypatterns import patterns_en_FISH_COMPONENT
from spacy.pipeline import EntityRuler


@Language.factory("fish_component_ruler")
def create_fish_component_ruler(nlp, name="fish_component_ruler", patterns=patterns_en_FISH_COMPONENT):
    return EntityRuler(
        nlp=nlp,
        name=name,
        phrase_matcher_attr="LOWER",
        validate=True,
        overwrite_ents=True,
        ent_id_sep="||",
        patterns=patterns
    )


# test the FISH_ComponentRuler class
if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm", disable=['ner'])
    nlp.add_pipe("fish_component_ruler", last=True)
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
