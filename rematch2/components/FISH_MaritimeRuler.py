"""
=============================================================================
Package :   rematch2.components
Module  :   FISH_MaritimeRuler.py
Version :   20220803
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   ARIADNEplus
Summary :   spaCy custom pipeline component (specialized EntityRuler)
            to identify Terms from the HE Maritime Craft Thesaurus 
            in free text. Entity type added will be "MARITIME"
Imports :   os, sys, spacy, Language, PatternRuler
Example :   nlp.add_pipe("fish_maritime_ruler", last=True)           
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
History :   03/08/2022 CFB Initially created script
=============================================================================
"""
import os
import sys
import spacy            # NLP library

from spacy.language import Language
from ..spacypatterns import patterns_en_FISH_MARITIME

from .PatternRuler import PatternRuler

# defaults to English patterns if no language-specific factory exists


@Language.factory("fish_maritime_ruler")
def create_fish_maritime_ruler(nlp, name="fish_maritime_ruler", patterns=patterns_en_FISH_MARITIME):
    return PatternRuler(nlp, name, patterns)


# test the FISH_MaritimeRuler class
if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm", disable=['ner'])
    nlp.add_pipe("fish_maritime_ruler", last=True)
    print(nlp.pipe_names)
    text = "Undertook some excavation on the site, then some aerial reconnaissance, followed by a laser scanning survey."
    doc = nlp(text)
    for ent in doc.ents:
        print(ent.ent_id_, ent.text, ent.label_)
