"""
=============================================================================
Package :   rematch2
Module  :   CenturyRuler.py
Version :   20220803
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   ARIADNEplus
Summary :   spaCy custom pipeline component (specialized EntityRuler)
            Language-sensitive component to identify and tag ordinal centuries
            in free text. Entity type added will be "CENTURY"
Imports :   os, sys, spacy, Language, EntityRuler, Doc
Example :   nlp.add_pipe("century_ruler", last=True)           
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

from spacy.lang.de import German
from spacy.lang.en import English
from spacy.lang.es import Spanish
from spacy.lang.fr import French
from spacy.lang.it import Italian
from spacy.lang.nl import Dutch
from spacy.lang.nb import Norwegian
from spacy.lang.sv import Swedish

from patterns import * 

from OrdinalRuler import *
from DatePrefixRuler import *
from DateSuffixRuler import *
from DateSeparatorRuler import *
from MonthNameRuler import *
from SeasonNameRuler import *

module_path = os.path.abspath(os.path.join('..', 'src'))
if module_path not in sys.path:
    sys.path.append(module_path)

@Language.factory("century_ruler")
def create_century_ruler(nlp, name="century_ruler", patterns=[]):
    return CenturyRuler(nlp, name, patterns)    

@German.factory("century_ruler")
def create_century_ruler_de(nlp, name="century_ruler_de"):
    return create_century_ruler(nlp, name, patterns_de_CENTURY)    

@English.factory("century_ruler")
def create_century_ruler_en(nlp, name="century_ruler_en"):
    return create_century_ruler(nlp, name, patterns_en_CENTURY)    

@Spanish.factory("century_ruler")
def create_century_ruler_es(nlp, name="century_ruler_es"):
    return create_century_ruler(nlp, name, patterns_es_CENTURY)   

@French.factory("century_ruler")
def create_century_ruler_fr(nlp, name="century_ruler_fr"):
    return create_century_ruler(nlp, name, patterns_fr_CENTURY)    

@Italian.factory("century_ruler")
def create_century_ruler_it(nlp, name="century_ruler_it"):
    return create_century_ruler(nlp, name, patterns_it_CENTURY)    

@Dutch.factory("century_ruler")
def create_century_ruler_nl(nlp, name="century_ruler_nl"):
    return create_century_ruler(nlp, name, patterns_nl_CENTURY)
    
@Norwegian.factory("century_ruler")
def create_century_ruler_no(nlp, name="century_ruler_no"):
    return create_century_ruler(nlp, name, patterns_no_CENTURY)    

@Swedish.factory("century_ruler")
def create_century_ruler_sv(nlp, name="century_ruler_sv"):
    return create_century_ruler(nlp, name, patterns_sv_CENTURY)    


# CenturyRuler is a specialized EntityRuler
class CenturyRuler(EntityRuler):        
   
    def __init__(self, nlp: Language, name: str, patterns=[]) -> None:
        EntityRuler.__init__(
            self, 
            nlp=nlp, 
            name=name,
            phrase_matcher_attr="LOWER",
            validate=True,
            overwrite_ents=True,
            ent_id_sep="||"
        )
        atomic_pipe_names = [
            "ordinal_ruler",
            "monthname_ruler", 
            "seasonname_ruler",             
            "dateprefix_ruler", 
            "datesuffix_ruler", 
            "dateseparator_ruler"            
        ] 
        for name in atomic_pipe_names:
            if not name in nlp.pipe_names:       
                nlp.add_pipe(name, last=True)       

         # add century patterns to this pipeline component
        self.add_patterns(patterns)           


    def __call__(self, doc: Doc) -> Doc:
        EntityRuler.__call__(self, doc)
        filtered = [ent for ent in doc.ents if ent.label_ not in ["ORDINAL", "DATEPREFIX", "DATESUFFIX", "DATESEPARATOR", "MONTHNAME", "SEASONNAME"]]
        doc.ents = filtered
        return doc


# test the pipeline component
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

        nlp.add_pipe("century_ruler", last=True) 
        print(nlp.pipe_names) 
        doc = nlp(test["text"])
        #if(test["language"]=="no"):
            #for token in doc:
                #print(f"{token.pos_}\t{token.text}\t{token.lemma_}\n")
            
        for ent in doc.ents:
            print (ent.ent_id_, ent.text, ent.label_)