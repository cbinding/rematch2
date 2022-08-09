"""
=============================================================================
Package :   rematch2
Module  :   MaterialRuler.py
Version :   20220803
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   ARIADNEplus
Summary :   spaCy custom pipeline component (specialized EntityRuler)
Imports :   os, sys, spacy, PatternRuler
Example :   nlp.add_pipe("material_ruler", last=True)           
License :   https://creativecommons.org/licenses/by/4.0/ [CC-BY]
History :   03/08/2022 CFB Initially created script
=============================================================================
""" 
import os
import sys
import spacy            # NLP library

from spacy.language import Language
from spacy.lang.en import English

from spacy.pipeline import EntityRuler
from spacy.tokens import Doc

from patterns import patterns_en_MATERIAL
from PatternRuler import PatternRuler 

module_path = os.path.abspath(os.path.join('..', 'src'))
if module_path not in sys.path:
    sys.path.append(module_path)


@Language.factory("material_ruler")
def create_material_ruler(nlp, name="material_ruler", patterns=[]):
    return PatternRuler(nlp, name, patterns)
    

@English.factory("material_ruler")
def create_material_ruler_en(nlp, name):
    ruler = create_material_ruler(nlp, name, patterns_en_MATERIAL)
    return ruler


# test the material_ruler pipeline component
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

        nlp.add_pipe("material_ruler", last=True) 
        print(nlp.pipe_names) 
        doc = nlp(test["text"])
        
        for ent in doc.ents:
            print (ent.ent_id_, ent.text, ent.label_)
     
    