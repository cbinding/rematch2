"""
=============================================================================
Package :   rematch2
Module  :   NegationRuler.py
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy custom pipeline component (specialized EntityRuler)
            Language-sensitive component to identify negation phrases
            in free text. Entity type added will be "NEGATION"
Imports :   os, sys, spacy, Language, EntityRuler, Doc
Example :   nlp.add_pipe("negation_ruler", last=True)           
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History :   
28/02/2024 CFB Initially created script
=============================================================================
"""
import os
import sys
from pathlib import Path
import json
import spacy            # NLP library
from spacy.pipeline import EntityRuler
from spacy.language import Language
from spacy.lang.en import English

if __package__ is None or __package__ == '':
    # uses current directory visibility
    from spacypatterns import *
    from Util import *    
else:
    # uses current package visibility
    from .spacypatterns import *
    from .Util import *   


@Language.factory("negation_ruler", default_config={"patterns": []})
def create_negation_ruler(nlp: Language, name: str="negation_ruler", patterns: list=[]) -> EntityRuler:
    normalized_patterns = normalize_patterns(
        nlp=nlp, 
        patterns=patterns,
        default_label="NEGATION",
        lemmatize=False,
        min_term_length=3
    )
    return EntityRuler(
        nlp=nlp, 
        name=name, 
        patterns=normalized_patterns,
        phrase_matcher_attr="LOWER",
        validate=False,
        overwrite_ents=True,
        ent_id_sep="||"
    )
    

@English.factory("negation_ruler")
def create_negation_ruler_en(nlp: Language, name: str = "negation_ruler") -> EntityRuler:
    return create_negation_ruler(nlp, name, patterns_en_NEGATION)

'''
@Spanish.factory("negation_ruler")
def create_negation_ruler_es(nlp: Language, name: str = "negation_ruler") -> EntityRuler:
    return create_negation_ruler(nlp, name, patterns_es_NEGATION)


@French.factory("negation_ruler")
def create_negation_ruler_fr(nlp: Language, name: str = "negation_ruler") -> EntityRuler:
    return create_negation_ruler(nlp, name, patterns_fr_NEGATION)


@Italian.factory("negation_ruler")
def create_negation_ruler_it(nlp: Language, name: str = "negation_ruler") -> EntityRuler:
    return create_negation_ruler(nlp, name, patterns_it_NEGATION)


@Dutch.factory("negation_ruler")
def create_negation_ruler_nl(nlp: Language, name: str = "negation_ruler") -> EntityRuler:
    return create_negation_ruler(nlp, name, patterns_nl_NEGATION)


@Norwegian.factory("negation_ruler")
def create_negation_ruler_no(nlp: Language, name: str = "negation_ruler") -> EntityRuler:
    return create_negation_ruler(nlp, name, patterns_no_NEGATION)


@Swedish.factory("negation_ruler")
def create_negation_ruler_sv(nlp: Language, name: str = "negation_ruler") -> EntityRuler:
    return create_negation_ruler(nlp, name, patterns_sv_NEGATION)

# Polish as temp experimental substitute until Czech is available
@Polish.factory("negation_ruler")
def create_negation_ruler_cs(nlp: Language, name: str = "negation_ruler") -> EntityRuler:
    return create_negation_ruler(nlp, name, patterns_cs_NEGATION)
'''

# test the NegationRuler class
if __name__ == "__main__":
    tests = []
    # load some local test texts from JSON file..    
    test_file_path = (Path(__file__).parent.parent / "test_examples_english.json").resolve()    
    with open(test_file_path, "r") as f:
        tests = json.load(f)
    
    # set up the spaCy pipeline
    nlp = get_pipeline_for_language("en")
    nlp.add_pipe("negation_ruler", last=True)
        
    # run using test texts
    for test in tests:
        text = test.get("text", "")
        
        print(f"-------------\n{text}\n")
        doc = nlp(text)
        
        print(doc_toks_to_text(doc))
        print(doc_ents_to_text(doc))

