"""
=============================================================================
Package :   rematch2
Module  :   DatePrefixRuler.py
Version :   20220803
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   ARIADNEplus
Summary :   spaCy custom pipeline component (specialized EntityRuler)
Imports :   os, sys, spacy, EntityRuler, Doc, Language
Example :   nlp.add_pipe("material_ruler", last=True)           
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

#module_path = os.path.abspath(os.path.join('..', 'src'))
#if module_path not in sys.path:
    #sys.path.append(module_path)

from ..patterns import \
    patterns_de_DATEPREFIX, \
    patterns_en_DATEPREFIX, \
    patterns_es_DATEPREFIX, \
    patterns_fr_DATEPREFIX, \
    patterns_it_DATEPREFIX, \
    patterns_nl_DATEPREFIX, \
    patterns_no_DATEPREFIX, \
    patterns_sv_DATEPREFIX

from .PatternRuler import PatternRuler

@Language.factory("dateprefix_ruler")
def create_dateprefix_ruler(nlp, name="dateprefix_ruler", patterns=[]):
    return PatternRuler(nlp, name, patterns)    

@German.factory("dateprefix_ruler")
def create_dateprefix_ruler_de(nlp, name="dateprefix_ruler_de"):
    return create_dateprefix_ruler(nlp, name, patterns_de_DATEPREFIX)
    
@English.factory("dateprefix_ruler")
def create_dateprefix_ruler_en(nlp, name="dateprefix_ruler_en"):
    return create_dateprefix_ruler(nlp, name, patterns_en_DATEPREFIX)
    
@Spanish.factory("dateprefix_ruler")
def create_dateprefix_ruler_es(nlp, name="dateprefix_ruler_es"):
    return create_dateprefix_ruler(nlp, name, patterns_es_DATEPREFIX)
   
@French.factory("dateprefix_ruler")
def create_dateprefix_ruler_fr(nlp, name="dateprefix_ruler_fr"):
    return create_dateprefix_ruler(nlp, name, patterns_fr_DATEPREFIX)    

@Italian.factory("dateprefix_ruler")
def create_dateprefix_ruler_it(nlp, name="dateprefix_ruler_it"):
    return create_dateprefix_ruler(nlp, name, patterns_it_DATEPREFIX)
    
@Dutch.factory("dateprefix_ruler")
def create_dateprefix_ruler_nl(nlp, name="dateprefix_ruler_nl"):
    return create_dateprefix_ruler(nlp, name, patterns_nl_DATEPREFIX)

@Norwegian.factory("dateprefix_ruler")
def create_dateprefix_ruler_no(nlp, name="dateprefix_ruler_no"):
    return create_dateprefix_ruler(nlp, name, patterns_no_DATEPREFIX)

@Swedish.factory("dateprefix_ruler")
def create_dateprefix_ruler_sv(nlp, name="dateprefix_ruler_sv"):
    return create_dateprefix_ruler(nlp, name, patterns_sv_DATEPREFIX)

# test the material_ruler pipeline component
if __name__ == "__main__":
    
    tests = [
        { "lang": "de", "pipe": "de_core_news_sm", "text": "erbaut Anfang bis Mitte 1480 bis Ende 1275 oder Anfang des 16. Jahrhunderts" },
        { "lang": "en", "pipe": "en_core_web_sm", "text": "constructed in early to mid 1480 to late 1275, or early 1500s" },
        { "lang": "es", "pipe": "es_core_news_sm", "text": "construido a principios o mediados de 1480 hasta finales de 1275 o principios del siglo XVI" },
        { "lang": "fr", "pipe": "fr_core_news_sm", "text": "construit du début au milieu de 1480 à la fin de 1275 ou au début des années 1500" },
        { "lang": "it", "pipe": "it_core_news_sm", "text": "costruito dall'inizio alla metà del 1480 fino alla fine del 1275 o all'inizio del 1500" },
        { "lang": "nl", "pipe": "nl_core_news_sm", "text": "gebouwd in het begin tot midden 1480 tot eind 1275, of begin 1500" },
        { "lang": "no", "pipe": "nb_core_news_sm", "text": "konstruert tidlig til midten av 1480 til slutten av 1275, eller tidlig på 1500-tallet" },
        { "lang": "sv", "pipe": "sv_core_news_sm", "text": "byggd i början till mitten av 1480 till slutet av 1275, eller tidigt 1500-tal" }
    ]

    for test in tests:
        print(f"-------------\nlanguage = {test['lang']}")
        nlp = spacy.load(test["pipe"], disable = ['ner']) 
        nlp.add_pipe("dateprefix_ruler", last=True) 
        doc = nlp(test["text"])
        for ent in doc.ents:
            print (ent.ent_id_, ent.text, ent.label_)
     
    