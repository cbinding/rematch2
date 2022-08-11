"""
=============================================================================
Package :   rematch2
Module  :   YearSpanRuler.py
Version :   20220803
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   ARIADNEplus
Summary :   spaCy custom pipeline component (specialized EntityRuler)
            Language-sensitive component to identify and tag ordinal centuries
            in free text. Entity type added will be "YEARSPAN"
Imports :   os, sys, spacy, Language, EntityRuler, Doc
Example :   nlp.add_pipe("yearspan_ruler", last=True)           
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

from ..patterns import * 

from .OrdinalRuler import *
from .DatePrefixRuler import *
from .DateSuffixRuler import *
from .DateSeparatorRuler import *
from .MonthNameRuler import *
from .SeasonNameRuler import *

#module_path = os.path.abspath(os.path.join('..', 'src'))
#if module_path not in sys.path:
    #sys.path.append(module_path)

@Language.factory("yearspan_ruler")
def create_yearspan_ruler(nlp, name="yearspan_ruler", patterns=[]):
    return YearSpanRuler(nlp, name, patterns)    

@German.factory("yearspan_ruler")
def create_yearspan_ruler_de(nlp, name="yearspan_ruler_de"):
    return create_yearspan_ruler(nlp, name, patterns_de_YEARSPAN)    

@English.factory("yearspan_ruler")
def create_yearspan_ruler_en(nlp, name="yearspan_ruler_en"):
    return create_yearspan_ruler(nlp, name, patterns_en_YEARSPAN)    

@Spanish.factory("yearspan_ruler")
def create_yearspan_ruler_es(nlp, name="yearspan_ruler_es"):
    return create_yearspan_ruler(nlp, name, patterns_es_YEARSPAN)   

@French.factory("yearspan_ruler")
def create_yearspan_ruler_fr(nlp, name="yearspan_ruler_fr"):
    return create_yearspan_ruler(nlp, name, patterns_fr_YEARSPAN)    

@Italian.factory("yearspan_ruler")
def create_yearspan_ruler_it(nlp, name="yearspan_ruler_it"):
    return create_yearspan_ruler(nlp, name, patterns_it_YEARSPAN)    

@Dutch.factory("yearspan_ruler")
def create_yearspan_ruler_nl(nlp, name="yearspan_ruler_nl"):
    return create_yearspan_ruler(nlp, name, patterns_nl_YEARSPAN)
    
@Norwegian.factory("yearspan_ruler")
def create_yearspan_ruler_no(nlp, name="yearspan_ruler_no"):
    return create_yearspan_ruler(nlp, name, patterns_no_YEARSPAN)    

@Swedish.factory("yearspan_ruler")
def create_yearspan_ruler_sv(nlp, name="yearspan_ruler_sv"):
    return create_yearspan_ruler(nlp, name, patterns_sv_YEARSPAN)    


# YearSpanRuler is a specialized EntityRuler
class YearSpanRuler(EntityRuler):        
   
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
            "dateprefix_ruler", 
            "datesuffix_ruler", 
            "dateseparator_ruler", 
            "ordinal_ruler", 
            "monthname_ruler", 
            "seasonname_ruler"
        ] 
        for name in atomic_pipe_names:
            if not name in nlp.pipe_names:       
                nlp.add_pipe(name, last=True)       

        # add yearspan patterns to this pipeline component
        self.add_patterns(patterns)           


    def __call__(self, doc: Doc) -> Doc:
        EntityRuler.__call__(self, doc)
        filtered = [ent for ent in doc.ents if ent.label_ not in ["ORDINAL", "DATEPREFIX", "DATESUFFIX", "DATESEPARATOR", "MONTHNAME", "SEASONNAME"]]
        doc.ents = filtered
        return doc


# test the YearSpanRuler class
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

        nlp.add_pipe("yearspan_ruler", last=True) 
        print(nlp.pipe_names) 
        doc = nlp(test["text"])
        
        for ent in doc.ents:
            print (ent.ent_id_, ent.text, ent.label_)
        