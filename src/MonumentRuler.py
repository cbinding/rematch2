"""
=============================================================================
Package :   rematch2
Module  :   MonumentRuler.py
Version :   20220803
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   ARIADNEplus
Summary :   spaCy custom pipeline component (specialized EntityRuler)
Imports :   os, sys, spacy, EntityRuler, Doc, Language
Example :   nlp.add_pipe("monument_ruler", last=True);
            draws on https://github.com/ICLRandD/Blackstone/blob/master/blackstone/pipeline/concepts.py            
License :   https://creativecommons.org/licenses/by/4.0/ [CC-BY]
History :   03/08/2022 CFB Initially created script
=============================================================================
""" 
import os
import sys
import spacy            # NLP library

from spacy.language import Language
#from spacy.lang.de import German
from spacy.lang.en import English
from spacy.lang.fr import French

from spacy.pipeline import EntityRuler
from spacy.tokens import Doc

#from collections import Counter
#from patterns import patterns_de_MONUMENT
from patterns import patterns_en_MONUMENT
#from patterns import patterns_fr_MONUMENT
from PatternRuler import PatternRuler

module_path = os.path.abspath(os.path.join('..', 'src'))
if module_path not in sys.path:
    sys.path.append(module_path)

@Language.factory("monument_ruler")
def create_monument_ruler(nlp, name="minument_ruler", patterns=[]):   
    return PatternRuler(nlp, name, patterns) 

@English.factory("monument_ruler")
def create_monument_ruler_en(nlp, name="monument_ruler_en"):
    return create_monument_ruler(nlp, name, patterns_en_MONUMENT)
   
@French.factory("monument_ruler")
def create_monument_ruler_fr(nlp, name="monument_ruler_fr"):
    return create_monument_ruler(nlp, name, patterns_en_MONUMENT) # TODO - use INRAP/PACTOLS patterns here instead...    
 
# test the monument_ruler pipeline component
if __name__ == "__main__":
    import json
    test_file_name = "test-examples.json"
    tests = [] 
    with open(test_file_name, "r") as f:  # what if file doesn't exist?            
        tests = json.load(f)

    for test in tests:
        print(f"-------------\nlanguage = {test['language']}")
        
        nlp = spacy.load(test["pipe"], disable = ['ner']) 
        #nlp.max_length = 2000000

        nlp.add_pipe("monument_ruler", last=True) 
        print(nlp.pipe_names) 
        doc = nlp(test["text"])
        
        for ent in doc.ents:
            print (ent.ent_id_, ent.text, ent.label_)
    


    