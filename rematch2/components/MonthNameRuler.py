"""
=============================================================================
Package :   rematch2
Module  :   MonthNameRuler.py
Version :   20220803
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   ARIADNEplus
Summary :   spaCy custom pipeline component (specialized EntityRuler)
            Language-sensitive component to identify month names
            in free text. Entity type added will be "MONTHNAME"
Imports :   os, sys, spacy, Language, EntityRuler, Doc
Example :   nlp.add_pipe("monthname_ruler", last=True)           
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
    patterns_de_MONTHNAME, \
    patterns_en_MONTHNAME, \
    patterns_es_MONTHNAME, \
    patterns_fr_MONTHNAME, \
    patterns_it_MONTHNAME, \
    patterns_nl_MONTHNAME, \
    patterns_no_MONTHNAME, \
    patterns_sv_MONTHNAME

from .PatternRuler import PatternRuler

#module_path = os.path.abspath(os.path.join('..', 'src'))
#if module_path not in sys.path:
    #sys.path.append(module_path)

@Language.factory("monthname_ruler")
def create_monthname_ruler(nlp, name="monthname_ruler", patterns=[]):
    return PatternRuler(nlp, name, patterns)   

@German.factory("monthname_ruler")
def create_monthname_ruler_de(nlp, name="monthname_ruler_de"):
    return create_monthname_ruler(nlp, name, patterns_de_MONTHNAME)

@English.factory("monthname_ruler")
def create_monthname_ruler_en(nlp, name="monthname_ruler_en"):
    return create_monthname_ruler(nlp, name, patterns_en_MONTHNAME)

@Spanish.factory("monthname_ruler")
def create_monthname_ruler_es(nlp, name="monthname_ruler_es"):
    return create_monthname_ruler(nlp, name, patterns_es_MONTHNAME)

@French.factory("monthname_ruler")
def create_monthname_ruler_fr(nlp, name="monthname_ruler_fr"):
    return create_monthname_ruler(nlp, name, patterns_fr_MONTHNAME)

@Italian.factory("monthname_ruler")
def create_monthname_ruler_it(nlp, name="monthname_ruler_it"):
    return create_monthname_ruler(nlp, name, patterns_it_MONTHNAME)

@Dutch.factory("monthname_ruler")
def create_monthname_ruler_nl(nlp, name="monthname_ruler_nl"):
    return create_monthname_ruler(nlp, name, patterns_nl_MONTHNAME)

@Norwegian.factory("monthname_ruler")
def create_monthname_ruler_no(nlp, name="monthname_ruler_no"):
    return create_monthname_ruler(nlp, name, patterns_no_MONTHNAME)

@Swedish.factory("monthname_ruler")
def create_monthname_ruler_sv(nlp, name="monthname_ruler_sv"):
    return create_monthname_ruler(nlp, name, patterns_sv_MONTHNAME)


# test the MonthNameRuler class
if __name__ == "__main__":    
    
    tests = [
        { "lang": "de", "pipe": "de_core_news_sm", "text": "Im Januar oder im März oder im Oktober, vielleicht im Dezember?" },
        { "lang": "en", "pipe": "en_core_web_sm", "text": "In January or in March or in October, maybe in Dec" },
        { "lang": "es", "pipe": "es_core_news_sm", "text": "¿En enero o en marzo o en octubre, tal vez en diciembre?" },
        { "lang": "fr", "pipe": "fr_core_news_sm", "text": "En janvier ou en mars ou en octobre, peut-être en décembre?" },
        { "lang": "it", "pipe": "it_core_news_sm", "text": "A gennaio o a marzo o a ottobre, forse a dicembre?" },
        { "lang": "nl", "pipe": "nl_core_news_sm", "text": "In januari of in maart of in oktober, misschien in december?" },
        { "lang": "no", "pipe": "nb_core_news_sm", "text": "I januar eller i mars eller i oktober, kanskje i desember?" },
        { "lang": "sv", "pipe": "sv_core_news_sm", "text": "I januari eller i mars eller i oktober, kanske i december?" }
    ]
    for test in tests:
        print(f"-------------\nlanguage = {test['lang']}")
        nlp = spacy.load(test["pipe"], disable = ['ner']) 
        nlp.add_pipe("monthname_ruler", last=True) 
        doc = nlp(test["text"])
        for ent in doc.ents:
            print (ent.ent_id_, ent.text, ent.label_)
        