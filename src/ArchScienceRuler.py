"""
=============================================================================
Package :   rematch2
Module  :   ArchScienceRuler.py
Version :   20220803
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   ARIADNEplus
Summary :   spaCy custom pipeline component (specialized EntityRuler)
Imports :   os, sys, spacy, EntityRuler, Doc, Language
Example :   nlp.add_pipe("archscience_ruler", last=True)           
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

from spacy.lang.en import English
#from spacy.lang.fr import French

from patterns import patterns_en_ARCHSCIENCE

module_path = os.path.abspath(os.path.join('..', 'src'))
if module_path not in sys.path:
    sys.path.append(module_path)


@Language.factory("archscience_ruler")
def create_archscience_ruler(nlp, name, patterns):
    ruler = ArchScienceRuler(nlp, name, patterns)
    return ruler


@English.factory("archscience_ruler")
def create_dayname_ruler_en(nlp, name):
    ruler = create_archscience_ruler(nlp, name, patterns_en_ARCHSCIENCE)
    return ruler


# ArchScienceRuler is a specialized EntityRuler
class ArchScienceRuler(EntityRuler):        
   
    def __init__(self, nlp: Language, name: str, patterns=[]) -> None:
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


    # in this instance we just call the parent function, 
    # but could do more doc processing here
    def __call__(self, doc: Doc) -> Doc:
        EntityRuler.__call__(self, doc)
        return doc


# test the ArchScienceRuler class
if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm", disable = ['ner']) 
    nlp.add_pipe("archscience_ruler", last=True)
    print(nlp.pipe_names)  
    text = "Undertook some alpha spectrometry followed by a stable isotope analysis, on the site."
    doc = nlp(text)
    for ent in doc.ents:
        print (ent.ent_id_, ent.text, ent.label_)

    