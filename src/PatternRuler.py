"""
=============================================================================
Package :   rematch2
Module  :   PatternRuler.py
Version :   20220803
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   ARIADNEplus
Summary :   spaCy custom pipeline component (specialized EntityRuler)
Imports :   os, sys, spacy, EntityRuler, Doc, Language
Example :   nlp.add_pipe("material_ruler", last=True)     
License :   https://creativecommons.org/licenses/by/4.0/ [CC-BY]
History :   03/08/2022 CFB Initially created script
=============================================================================
""" 
import os
import sys
import spacy            # NLP library

from spacy.language import Language

from spacy.pipeline import EntityRuler
from spacy.tokens import Doc

module_path = os.path.abspath(os.path.join('..', 'src'))
if module_path not in sys.path:
    sys.path.append(module_path)

@Language.factory("pattern_ruler")
def create_custom_ruler(nlp, name, patterns):
    ruler = PatternRuler(nlp, name, patterns)
    return ruler

# PatternRuler is a specialized EntityRuler (at the moment it's not very specialized)
class PatternRuler(EntityRuler): 
    def __init__(self, nlp: Language, name: str="pattern_ruler", patterns=None) -> None:        
        EntityRuler.__init__(
            self, 
            nlp=nlp, 
            name=name,
            phrase_matcher_attr="LOWER",
            validate=True,
            overwrite_ents=True,
            ent_id_sep="||",
            patterns = patterns
        )   

    # in this instance we just call the parent function, but could do more doc processing here
    def __call__(self, doc: Doc) -> Doc:
        EntityRuler.__call__(self, doc)        
        return doc
   
    