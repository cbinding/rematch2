"""
=============================================================================
Package :   rematch2
Module  :   DateSeparatorRuler.py
Version :   20220803
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   ARIADNEplus
Summary :   spaCy custom pipeline component (specialized EntityRuler)
            Language-sensitive component to identify date separators
            in free text. Entity type added will be "DATESEPARATOR"
Imports :   os, sys, spacy, Language, EntityRuler, Doc
Example :   nlp.add_pipe("dateseparator_ruler", last=True)           
License :   https://creativecommons.org/licenses/by/4.0/ [CC-BY]
History :   03/08/2022 CFB Initially created script
=============================================================================
""" 
import os
import sys
import spacy            # NLP library

from spacy.language import Language
from spacy.lang.de import German
from spacy.lang.en import English
from spacy.lang.es import Spanish
from spacy.lang.fr import French
from spacy.lang.it import Italian
from spacy.lang.nl import Dutch
from spacy.lang.nb import Norwegian
from spacy.lang.sv import Swedish

from ..patterns import \
    patterns_de_DATESEPARATOR, \
    patterns_en_DATESEPARATOR, \
    patterns_es_DATESEPARATOR, \
    patterns_fr_DATESEPARATOR, \
    patterns_it_DATESEPARATOR, \
    patterns_nl_DATESEPARATOR, \
    patterns_no_DATESEPARATOR, \
    patterns_sv_DATESEPARATOR

from .PatternRuler import PatternRuler

#module_path = os.path.abspath(os.path.join('..', 'src'))
#if module_path not in sys.path:
    #sys.path.append(module_path)

@Language.factory("dateseparator_ruler")
def create_dateseparator_ruler(nlp, name="dateseparator_ruler", patterns=[]):
    return PatternRuler(nlp, name, patterns)   

@German.factory("dateseparator_ruler")
def create_dateseparator_ruler_de(nlp, name="dateseparator_ruler_de"):
    return create_dateseparator_ruler(nlp, name, patterns_de_DATESEPARATOR)

@English.factory("dateseparator_ruler")
def create_dateseparator_ruler_en(nlp, name="dateseparator_ruler_en"):
    return create_dateseparator_ruler(nlp, name, patterns_en_DATESEPARATOR)

@Spanish.factory("dateseparator_ruler")
def create_dateseparator_ruler_es(nlp, name="dateseparator_ruler_es"):
    return create_dateseparator_ruler(nlp, name, patterns_es_DATESEPARATOR)

@French.factory("dateseparator_ruler")
def create_dateseparator_ruler_fr(nlp, name="dateseparator_ruler_fr"):
    return create_dateseparator_ruler(nlp, name, patterns_fr_DATESEPARATOR)

@Italian.factory("dateseparator_ruler")
def create_dateseparator_ruler_it(nlp, name="dateseparator_ruler_it"):
    return create_dateseparator_ruler(nlp, name, patterns_it_DATESEPARATOR)

@Dutch.factory("dateseparator_ruler")
def create_dateseparator_ruler_nl(nlp, name="dateseparator_ruler_nl"):
    return create_dateseparator_ruler(nlp, name, patterns_nl_DATESEPARATOR)

@Norwegian.factory("dateseparator_ruler")
def create_dateseparator_ruler_no(nlp, name="dateseparator_ruler_no"):
    return create_dateseparator_ruler(nlp, name, patterns_no_DATESEPARATOR)

@Swedish.factory("dateseparator_ruler")
def create_dateseparator_ruler_sv(nlp, name="dateseparator_ruler_sv"):
    return create_dateseparator_ruler(nlp, name, patterns_sv_DATESEPARATOR)


# test the DateSeparatorRuler class
if __name__ == "__main__":    
    
    tests = [
        { "lang": "de", "pipe": "de_core_news_sm", "text": "erbaut 1480 bis 1275 oder 1500-1600" },
        { "lang": "en", "pipe": "en_core_web_sm", "text": "constructed in 1480 to 1275, or 1500-1600" },
        { "lang": "es", "pipe": "es_core_news_sm", "text": "construido en 1480 a 1275, o 1500-1600" },
        { "lang": "fr", "pipe": "fr_core_news_sm", "text": "construit en 1480 à 1275, ou 1500-1600" },
        { "lang": "it", "pipe": "it_core_news_sm", "text": "costruito nel 1480-1275, o 1500-1600" },
        { "lang": "nl", "pipe": "nl_core_news_sm", "text": "gebouwd in 1480 tot 1275, of 1500-1600" },
        { "lang": "no", "pipe": "nb_core_news_sm", "text": "bygget i 1480 til 1275, eller 1500-1600" },
        { "lang": "sv", "pipe": "sv_core_news_sm", "text": "byggd 1480 till 1275, eller 1500-1600" }
    ]
    for test in tests:
        print(f"-------------\nlanguage = {test['lang']}")
        nlp = spacy.load(test["pipe"], disable = ['ner']) 
        nlp.add_pipe("dateseparator_ruler", last=True) 
        doc = nlp(test["text"])
        for ent in doc.ents:
            print (ent.ent_id_, ent.text, ent.label_)
        