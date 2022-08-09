"""
=============================================================================
Package :   rematch2
Module  :   ArchScienceRuler.py
Version :   20220803
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   ARIADNEplus
Summary :   spaCy custom pipeline component (specialized EntityRuler)
Imports :   os, sys, spacy, Language, PatternRuler
Example :   nlp.add_pipe("archscience_ruler", last=True)           
License :   https://creativecommons.org/licenses/by/4.0/ [CC-BY]
History :   03/08/2022 CFB Initially created script
=============================================================================
""" 
import os
import sys
import spacy            # NLP library

from spacy.language import Language
from spacy.lang.en import English
#from spacy.lang.fr import French

from patterns import patterns_en_ARCHSCIENCE
from PatternRuler import PatternRuler

module_path = os.path.abspath(os.path.join('..', 'src'))
if module_path not in sys.path:
    sys.path.append(module_path)

@Language.factory("archscience_ruler")
def create_archscience_ruler(nlp, name="archscience_ruler", patterns=[]):
    return PatternRuler(nlp, name, patterns)    

@English.factory("archscience_ruler")
def create_archscience_ruler_en(nlp, name="archscience_ruler_en"):
    return create_archscience_ruler(nlp, name, patterns_en_ARCHSCIENCE)   


# test the ArchScienceRuler class
if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm", disable = ['ner']) 
    nlp.add_pipe("archscience_ruler", last=True)
    print(nlp.pipe_names)  
    text = "Undertook some alpha spectrometry followed by a stable isotope analysis, on the site."
    doc = nlp(text)
    for ent in doc.ents:
        print (ent.ent_id_, ent.text, ent.label_)

    