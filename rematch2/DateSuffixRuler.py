"""
=============================================================================
Package :   rematch2
Module  :   DateSuffixRuler.py
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy custom pipeline component (specialized SpanRuler)
Imports :   os, sys, spacy, SpanRuler, Language
Example :   
    nlp = spacy.load("en_core_web_sm", disable=['ner'])
    nlp.add_pipe("datesuffix_ruler", last=True)  
    doc = nlp("from 1st century BC to 5th century A.D., and circa 1500 BP")   
    # identifies ["BC", "A.D.", "BP"] as "DATESUFFIX"      
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History :   
03/08/2022 CFB Initially created script
27/10/2023 CFB type hints added for function signatures
16/02/2024 CFB remove BaseRuler inheritance, use EntityRuler directly
28/03/2024 CFB base on SpanRuler instead of EntityRuler
02/07/2025 CFB based on BaseRuler instead of SpanRuler(!)
=============================================================================
"""

from spacy.language import Language
from spacy.lang.de import German
from spacy.lang.en import English
from spacy.lang.es import Spanish
from spacy.lang.fr import French
from spacy.lang.it import Italian
from spacy.lang.nl import Dutch
from spacy.lang.nb import Norwegian
from spacy.lang.sv import Swedish
# from spacy.lang.cs import Czech # doesn't exist yet..
from spacy.lang.pl import Polish # experimental substitute for Czech

from .spacypatterns import *
from .Util import *
from .BaseRuler import BaseRuler
from .DocSummary import DocSummary


@Language.factory(name="datesuffix_ruler", default_config={"patterns": []})
def create_datesuffix_ruler(nlp: Language, name: str="datesuffix_ruler", patterns: list=[]) -> BaseRuler:
    
    
    ruler = BaseRuler(
        nlp=nlp,        
        name=name,
        spans_key="rematch",
        phrase_matcher_attr="LOWER",
        validate=False,
        overwrite=False
    )  

    normalized_patterns =  BaseRuler.normalize_patterns(
        nlp=nlp, 
        patterns=patterns,
        default_label="DATESUFFIX",
        lemmatize=False,
        min_term_length=2
    ) 

    ruler.add_patterns(normalized_patterns)
    return ruler 
    

@German.factory("datesuffix_ruler")
def create_datesuffix_ruler_de(nlp: Language, name: str = "datesuffix_ruler") -> BaseRuler:
    return create_datesuffix_ruler(nlp, name, patterns_de_DATESUFFIX)
    

@English.factory("datesuffix_ruler")
def create_datesuffix_ruler_en(nlp: Language, name: str = "datesuffix_ruler") -> BaseRuler:
   return create_datesuffix_ruler(nlp, name, patterns_en_DATESUFFIX)


@Spanish.factory("datesuffix_ruler")
def create_datesuffix_ruler_es(nlp: Language, name: str = "datesuffix_ruler") -> BaseRuler:
    return create_datesuffix_ruler(nlp, name, patterns_es_DATESUFFIX)


@French.factory("datesuffix_ruler")
def create_datesuffix_ruler_fr(nlp: Language, name: str = "datesuffix_ruler") -> BaseRuler:
    return create_datesuffix_ruler(nlp, name, patterns_fr_DATESUFFIX)


@Italian.factory("datesuffix_ruler")
def create_datesuffix_ruler_it(nlp: Language, name: str = "datesuffix_ruler") -> BaseRuler:
    return create_datesuffix_ruler(nlp, name, patterns_it_DATESUFFIX)


@Dutch.factory("datesuffix_ruler")
def create_datesuffix_ruler_nl(nlp: Language, name: str = "datesuffix_ruler") -> BaseRuler:
    return create_datesuffix_ruler(nlp, name, patterns_nl_DATESUFFIX)


@Norwegian.factory("datesuffix_ruler")
def create_datesuffix_ruler_no(nlp: Language, name: str = "datesuffix_ruler") -> BaseRuler:
    return create_datesuffix_ruler(nlp, name, patterns_no_DATESUFFIX)


@Swedish.factory("datesuffix_ruler")
def create_datesuffix_ruler_sv(nlp: Language, name: str = "datesuffix_ruler") -> BaseRuler:
    return create_datesuffix_ruler(nlp, name, patterns_sv_DATESUFFIX)


# Polish as temp experimental substitute until Czech is available
@Polish.factory("datesuffix_ruler")
def create_datesuffix_ruler_cs(nlp: Language, name: str = "datesuffix_ruler") -> BaseRuler:
    return create_datesuffix_ruler(nlp, name, patterns_cs_DATESUFFIX)


# test the pipeline component
if __name__ == "__main__":

    tests = [
        {"lang": "de", "text": "aus dem 1. Jahrhundert v. Chr. Bis zum 5. Jahrhundert n. Chr. Oder 1500 BP"},
        {"lang": "en", "text": "dating from 1st century BC to 5th century A.D., or 1500 BP"},
        {"lang": "es", "text": "que data del siglo I a.C. al siglo V d.C., o 1500 a.C., o 1850 a. C."},
        {"lang": "fr", "text": "datant du 1er siècle avant JC au 5ème siècle après JC, ou 1500 BP ou IIe siècle de notre ère"},
        {"lang": "it", "text": "databile dal I secolo a.C. al V secolo d.C., o 1500 a.C"},
        {"lang": "nl", "text": "daterend uit de 1e eeuw voor Christus tot de 5e eeuw na Christus, of 1500 BP"},
        {"lang": "no", "text": "dateres fra 1. århundre f.Kr. til 5. århundre e.Kr., eller 1500 f.Kr"},
        {"lang": "sv", "text": "från 1:a århundradet f.Kr. till 500-talet e.Kr., eller 1500 f.Kr"},
        {"lang": "cs", "text": "artefakt pochází ze 7. až 6. století př. n. l., ale může být i starší"}
    ]

    for test in tests:
        lang = test.get("lang", "")
        text = test.get("text", "")

        print(f"-------------\nlanguage = {lang}")
        nlp = get_pipeline_for_language(lang)
        nlp.add_pipe("datesuffix_ruler", last=True)
        doc = nlp(text)
        
        print("Tokens:\n" + DocSummary(doc).tokens_to_text())
        print("Spans:\n" + DocSummary(doc).spans_to_text())