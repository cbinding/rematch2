"""
=============================================================================
Package :   rematch2
Module  :   DateSuffixRuler.py
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy custom pipeline component (specialized EntityRuler)
Imports :   os, sys, spacy, EntityRuler, Language
Example :   
    nlp = spacy.load("en_core_web_sm", disable=['ner'])
    nlp.add_pipe("datesuffix_ruler", last=True)  
    doc = nlp("from 1st century BC to 5th century A.D., and circa 1500 BP")   
    # tags ["BC", "A.D.", "BP"] as "DATESUFFIX"      
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History :   
03/08/2022 CFB Initially created script
27/10/2023 CFB type hints added for function signatures
16/02/2024 CFB remove BaseRuler inheritance, use EntityRuler directly
=============================================================================
"""
import os
import sys
import spacy            # NLP library
#from collections.abc import MutableSequence
from spacy.pipeline import EntityRuler

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

if __package__ is None or __package__ == '':
    # uses current directory visibility
    from spacypatterns import *
    from Util import *
else:
    # uses current package visibility
    from .spacypatterns import *
    from .Util import *


@Language.factory(name="datesuffix_ruler", default_config={"patterns": []})
def create_datesuffix_ruler(nlp: Language, name: str="datesuffix_ruler", patterns: list=[]) -> EntityRuler:
    normalized_patterns = normalize_patterns(
        nlp=nlp, 
        patterns=patterns,
        default_label="DATESUFFIX",
        lemmatize=False,
        min_term_length=2
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
    

@German.factory("datesuffix_ruler")
def create_datesuffix_ruler_de(nlp: Language, name: str = "datesuffix_ruler") -> EntityRuler:
    return create_datesuffix_ruler(nlp, name, patterns_de_DATESUFFIX)
    

@English.factory("datesuffix_ruler")
def create_datesuffix_ruler_en(nlp: Language, name: str = "datesuffix_ruler") -> EntityRuler:
   return create_datesuffix_ruler(nlp, name, patterns_en_DATESUFFIX)


@Spanish.factory("datesuffix_ruler")
def create_datesuffix_ruler_es(nlp: Language, name: str = "datesuffix_ruler") -> EntityRuler:
    return create_datesuffix_ruler(nlp, name, patterns_es_DATESUFFIX)


@French.factory("datesuffix_ruler")
def create_datesuffix_ruler_fr(nlp: Language, name: str = "datesuffix_ruler") -> EntityRuler:
    return create_datesuffix_ruler(nlp, name, patterns_fr_DATESUFFIX)


@Italian.factory("datesuffix_ruler")
def create_datesuffix_ruler_it(nlp: Language, name: str = "datesuffix_ruler") -> EntityRuler:
    return create_datesuffix_ruler(nlp, name, patterns_it_DATESUFFIX)


@Dutch.factory("datesuffix_ruler")
def create_datesuffix_ruler_nl(nlp: Language, name: str = "datesuffix_ruler") -> EntityRuler:
    return create_datesuffix_ruler(nlp, name, patterns_nl_DATESUFFIX)


@Norwegian.factory("datesuffix_ruler")
def create_datesuffix_ruler_no(nlp: Language, name: str = "datesuffix_ruler") -> EntityRuler:
    return create_datesuffix_ruler(nlp, name, patterns_no_DATESUFFIX)


@Swedish.factory("datesuffix_ruler")
def create_datesuffix_ruler_sv(nlp: Language, name: str = "datesuffix_ruler") -> EntityRuler:
    return create_datesuffix_ruler(nlp, name, patterns_sv_DATESUFFIX)


# Polish as temp experimental substitute until Czech is available
@Polish.factory("datesuffix_ruler")
def create_datesuffix_ruler_cs(nlp: Language, name: str = "datesuffix_ruler") -> EntityRuler:
    return create_datesuffix_ruler(nlp, name, patterns_cs_DATESUFFIX)


# test the pipeline component
if __name__ == "__main__":

    tests = [
        {"lang": "de", "pipe": "de_core_news_sm",
            "text": "aus dem 1. Jahrhundert v. Chr. Bis zum 5. Jahrhundert n. Chr. Oder 1500 BP"},
        {"lang": "en", "pipe": "en_core_web_sm",
            "text": "dating from 1st century BC to 5th century A.D., or 1500 BP"},
        {"lang": "es", "pipe": "es_core_news_sm",
            "text": "que data del siglo I a.C. al siglo V d.C., o 1500 a.C."},
        {"lang": "fr", "pipe": "fr_core_news_sm",
            "text": "datant du 1er siècle avant JC au 5ème siècle après JC, ou 1500 BP ou IIe siècle de notre ère"},
        {"lang": "it", "pipe": "it_core_news_sm",
            "text": "databile dal I secolo a.C. al V secolo d.C., o 1500 a.C"},
        {"lang": "nl", "pipe": "nl_core_news_sm",
            "text": "daterend uit de 1e eeuw voor Christus tot de 5e eeuw na Christus, of 1500 BP"},
        {"lang": "no", "pipe": "nb_core_news_sm",
            "text": "dateres fra 1. århundre f.Kr. til 5. århundre e.Kr., eller 1500 f.Kr"},
        {"lang": "sv", "pipe": "sv_core_news_sm",
            "text": "från 1:a århundradet f.Kr. till 500-talet e.Kr., eller 1500 f.Kr"},
        {"lang": "cs", "pipe": "pl_core_news_sm",
            "text": "artefakt pochází ze 7. až 6. století př. n. l., ale může být i starší"}
    ]

    for test in tests:
        print(f"-------------\nlanguage = {test['lang']}")
        nlp = spacy.load(test["pipe"], disable=['ner'])
        nlp.add_pipe("datesuffix_ruler", last=True)
        doc = nlp(test["text"])
        for ent in doc.ents:
            print(ent.ent_id_, ent.text, ent.label_)
