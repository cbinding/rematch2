"""
=============================================================================
Package :   rematch2
Module  :   DateSeparatorRuler.py
Version :   20231027
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy custom pipeline component (specialized EntityRuler)
            Language-sensitive component to identify date separators
            in free text. Entity type added will be "DATESEPARATOR"
Imports :   os, sys, spacy, Language, EntityRuler, Doc
Example :   nlp.add_pipe("dateseparator_ruler", last=True)           
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History :   
03/08/2022 CFB Initially created script
27/10/2023 CFB type hints added for function signatures
=============================================================================
"""
import os
import sys
import spacy            # NLP library
from collections.abc import MutableSequence
#from spacy.pipeline import EntityRuler

from spacy.language import Language
#from spacy.lang.cs import Czech #doesn't exist yet..
from spacy.lang.de import German
from spacy.lang.en import English
from spacy.lang.es import Spanish
from spacy.lang.fr import French
from spacy.lang.it import Italian
from spacy.lang.nl import Dutch
from spacy.lang.nb import Norwegian
from spacy.lang.sv import Swedish
from spacy.lang.pl import Polish # experimental substitute for Czech as it doesn't exist yet..

if __package__ is None or __package__ == '':
    # uses current directory visibility
    from spacypatterns import *
    from BaseRuler import *
else:
    # uses current package visibility
    from .spacypatterns import *
    from .BaseRuler import *


@Language.factory("dateseparator_ruler")
def create_dateseparator_ruler(nlp: Language, name: str="dateseparator_ruler", patterns: MutableSequence=[]) -> BaseRuler:
   return BaseRuler(
       nlp=nlp,
       name=name,
       default_label="DATESEPARATOR",
       lemmatize=False,
       min_term_length=2,
       patterns=patterns
   )   


@German.factory("dateseparator_ruler")
def create_dateseparator_ruler_de(nlp: Language, name: str = "dateseparator_ruler") -> BaseRuler:
    return create_dateseparator_ruler(nlp, name, patterns_de_DATESEPARATOR)


@English.factory("dateseparator_ruler")
def create_dateseparator_ruler_en(nlp: Language, name: str = "dateseparator_ruler") -> BaseRuler:
    return create_dateseparator_ruler(nlp, name, patterns_en_DATESEPARATOR)


@Spanish.factory("dateseparator_ruler")
def create_dateseparator_ruler_es(nlp: Language, name: str = "dateseparator_ruler") -> BaseRuler:
    return create_dateseparator_ruler(nlp, name, patterns_es_DATESEPARATOR)


@French.factory("dateseparator_ruler")
def create_dateseparator_ruler_fr(nlp: Language, name: str = "dateseparator_ruler") -> BaseRuler:
    return create_dateseparator_ruler(nlp, name, patterns_fr_DATESEPARATOR)


@Italian.factory("dateseparator_ruler")
def create_dateseparator_ruler_it(nlp: Language, name: str = "dateseparator_ruler") -> BaseRuler:
    return create_dateseparator_ruler(nlp, name, patterns_it_DATESEPARATOR)


@Dutch.factory("dateseparator_ruler")
def create_dateseparator_ruler_nl(nlp: Language, name: str = "dateseparator_ruler") -> BaseRuler:
    return create_dateseparator_ruler(nlp, name, patterns_nl_DATESEPARATOR)


@Norwegian.factory("dateseparator_ruler")
def create_dateseparator_ruler_no(nlp: Language, name: str = "dateseparator_ruler") -> BaseRuler:
    return create_dateseparator_ruler(nlp, name, patterns_no_DATESEPARATOR)


@Swedish.factory("dateseparator_ruler")
def create_dateseparator_ruler_sv(nlp: Language, name: str = "dateseparator_ruler") -> BaseRuler:
    return create_dateseparator_ruler(nlp, name, patterns_sv_DATESEPARATOR)

# Polish as temp experimental substitute until Czech is available
@Polish.factory("dateseparator_ruler")
def create_dateseparator_ruler_cs(nlp: Language, name: str = "dateseparator_ruler") -> BaseRuler:
    return create_dateseparator_ruler(nlp, name, patterns_cs_DATESEPARATOR)

# test the DateSeparatorRuler class
if __name__ == "__main__":

    tests = [
        {"lang": "de", "pipe": "de_core_news_sm",
            "text": "erbaut 1480 bis 1275 oder 1500-1600"},
        {"lang": "en", "pipe": "en_core_web_sm",
            "text": "constructed in 1480 to 1275, or 1500-1600"},
        {"lang": "es", "pipe": "es_core_news_sm",
            "text": "construido en 1480 a 1275, o 1500-1600"},
        {"lang": "fr", "pipe": "fr_core_news_sm",
            "text": "construit en 1480 à 1275, ou 1500-1600"},
        {"lang": "it", "pipe": "it_core_news_sm",
            "text": "costruito nel 1480-1275, o 1500-1600"},
        {"lang": "nl", "pipe": "nl_core_news_sm",
            "text": "gebouwd in 1480 tot 1275, of 1500-1600"},
        {"lang": "no", "pipe": "nb_core_news_sm",
            "text": "bygget i 1480 til 1275, eller 1500-1600"},
        {"lang": "sv", "pipe": "sv_core_news_sm",
            "text": "byggd 1480 till 1275, eller 1500-1600"}
    ]
    for test in tests:
        print(f"-------------\nlanguage = {test['lang']}")
        nlp = spacy.load(test["pipe"], disable=['ner'])
        nlp.add_pipe("dateseparator_ruler", last=True)
        doc = nlp(test["text"])
        for ent in doc.ents:
            print(ent.ent_id_, ent.text, ent.label_)
