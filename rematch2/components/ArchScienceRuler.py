"""
=============================================================================
Package :   rematch2
Module  :   ArchScienceRuler.py
Version :   20220803
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   ARIADNEplus
Summary :   spaCy custom pipeline component (specialized EntityRuler)
            to identify Terms from the FISH Archaeological Sciences Thesaurus 
            in free text. Entity type added will be "ARCHSCIENCE"
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
from ..patterns import patterns_en_ARCHSCIENCE

from .PatternRuler import PatternRuler

#module_path = os.path.abspath(os.path.join('..', 'src'))
#if module_path not in sys.path:
    #sys.path.append(module_path)

# defaults to English patterns if no language-specific factory exists
@Language.factory("archscience_ruler")
def create_archscience_ruler(nlp, name="archscience_ruler", patterns=patterns_en_ARCHSCIENCE):
    return PatternRuler(nlp, name, patterns)    

# test the ArchScienceRuler class
if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm", disable = ['ner']) 
    nlp.add_pipe("archscience_ruler", last=True)
    print(nlp.pipe_names)  
    text = "Undertook some alpha spectrometry followed by a stable isotope analysis, on the site."
    doc = nlp(text)
    for ent in doc.ents:
        print (ent.ent_id_, ent.text, ent.label_)

    