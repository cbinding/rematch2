"""
=============================================================================
Package :   rematch2
Module  :   NamedPeriodRuler.py
Version :   20220803
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   ARIADNEplus
Summary :   spaCy custom pipeline component (specialized EntityRuler)
            Language-sensitive component to identify and tag named periods
            (from Perio.do) in free text. Entity type added will be "NAMEDPERIOD"
Imports :   os, sys, spacy, Language, EntityRuler, Doc
Example :   nlp.add_pipe("namedperiod_ruler", last=True)           
License :   https://creativecommons.org/licenses/by/4.0/ [CC-BY]
History :   03/08/2022 CFB Initially created script
=============================================================================
""" 
import os
import sys
import spacy            # NLP library

from spacy.pipeline import EntityRuler
from spacy.tokens import Doc
from spacy.language import Language

from PeriodoData import PeriodoData   

module_path = os.path.abspath(os.path.join('..', 'src'))
if module_path not in sys.path:
    sys.path.append(module_path)

@Language.factory("namedperiod_ruler", default_config={"periodo_authority_id": None})
def create_namedperiod_ruler(nlp, name, periodo_authority_id: str):
    ruler = NamedPeriodRuler(nlp, name, periodo_authority_id)
    return ruler

# NamedPeriodRuler is a specialized EntityRuler
class NamedPeriodRuler(EntityRuler):        
   
    def __init__(self, nlp: Language, name: str, periodo_authority_id=None) -> None:
        EntityRuler.__init__(
            self, 
            nlp=nlp, 
            name=name,
            phrase_matcher_attr="LOWER",
            validate=True,
            overwrite_ents=True,
            ent_id_sep="||"
        ) 
        # add terms from selected Perio.do authority as patterns
        pd = PeriodoData() # new instance, don't refresh cached data
        periodo_periods = pd.get_period_list(periodo_authority_id) # periods for authority id
        periodo_patterns = NamedPeriodRuler._periods_to_patterns(periodo_periods) # convert to spaCy pattern format
        self.add_patterns(periodo_patterns)        


    def __call__(self, doc: Doc) -> Doc:
        EntityRuler.__call__(self, doc)
        return doc

    # COnvert Periodo period records to spaCy patterns
    # input: [{id, language, label}, {id, language, label}]
    # output: [{id, language, label, pattern}, {id, language, label, pattern}]
    @staticmethod
    def _periods_to_patterns(data):
        patterns = list(map(lambda item: { 
            "id": item["id"],            
            "language": item["language"],
            "label": "NAMEDPERIOD",             
            "pattern": list(map(lambda word: { "LOWER": word.lower() }, item["label"].split()))           
        }, data or [])) 
        return patterns


# test the NamedPeriodRuler class
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

        nlp.add_pipe("namedperiod_ruler", last=True, config={"periodo_authority_id": test['periodo_authority_id']}) 
        print(nlp.pipe_names) 
        doc = nlp(test["text"])
        
        for ent in doc.ents:
            print (ent.ent_id_, ent.text, ent.label_)
        