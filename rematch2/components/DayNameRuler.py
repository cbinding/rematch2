"""
=============================================================================
Package :   rematch2.components
Module  :   DayNameRuler.py
Version :   20220803
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   ARIADNEplus
Summary :   spaCy custom pipeline component (specialized EntityRuler)
            Language-sensitive component to identify day names
            in free text. Entity type added will be "DAYNAME"
Imports :   os, sys, spacy, Language, EntityRuler, Doc
Example :   nlp.add_pipe("dayname_ruler", last=True)           
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
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

from ..spacypatterns import \
    patterns_de_DAYNAME, \
    patterns_en_DAYNAME, \
    patterns_es_DAYNAME, \
    patterns_fr_DAYNAME, \
    patterns_it_DAYNAME, \
    patterns_nl_DAYNAME, \
    patterns_no_DAYNAME, \
    patterns_sv_DAYNAME

from .PatternRuler import PatternRuler

#module_path = os.path.abspath(os.path.join('..', 'src'))
# if module_path not in sys.path:
# sys.path.append(module_path)


@Language.factory("dayname_ruler")
def create_dayname_ruler(nlp, name="dayname_ruler", patterns=[]):
    return PatternRuler(nlp, name, patterns)


@German.factory("dayname_ruler")
def create_dayname_ruler_de(nlp, name="dayname_ruler_de"):
    return create_dayname_ruler(nlp, name, patterns_de_DAYNAME)


@English.factory("dayname_ruler")
def create_dayname_ruler_en(nlp, name="dayname_ruler_en"):
    return create_dayname_ruler(nlp, name, patterns_en_DAYNAME)


@Spanish.factory("dayname_ruler")
def create_dayname_ruler_es(nlp, name="dayname_ruler_es"):
    return create_dayname_ruler(nlp, name, patterns_es_DAYNAME)


@French.factory("dayname_ruler")
def create_dayname_ruler_fr(nlp, name="dayname_ruler_fr"):
    return create_dayname_ruler(nlp, name, patterns_fr_DAYNAME)


@Italian.factory("dayname_ruler")
def create_dayname_ruler_it(nlp, name="dayname_ruler_it"):
    return create_dayname_ruler(nlp, name, patterns_it_DAYNAME)


@Dutch.factory("dayname_ruler")
def create_dayname_ruler_nl(nlp, name="dayname_ruler_nl"):
    return create_dayname_ruler(nlp, name, patterns_nl_DAYNAME)


@Norwegian.factory("dayname_ruler")
def create_dayname_ruler_no(nlp, name="dayname_ruler_no"):
    return create_dayname_ruler(nlp, name, patterns_no_DAYNAME)


@Swedish.factory("dayname_ruler")
def create_dayname_ruler_sv(nlp, name="dayname_ruler_sv"):
    return create_dayname_ruler(nlp, name, patterns_sv_DAYNAME)


# test the DayNameRuler class
if __name__ == "__main__":

    tests = [
        {"lang": "de", "pipe": "de_core_news_sm",
            "text": "Am Montag oder Dienstag oder vielleicht sogar am Mittwoch"},
        {"lang": "en", "pipe": "en_core_web_sm",
            "text": "On Monday or Tuesday or maybe even on Wednesday"},
        {"lang": "es", "pipe": "es_core_news_sm",
            "text": "El lunes o el martes o tal vez incluso el miércoles"},
        {"lang": "fr", "pipe": "fr_core_news_sm",
            "text": "Le lundi ou le mardi ou peut-être même le mercredi"},
        {"lang": "it", "pipe": "it_core_news_sm",
            "text": "Il lunedì o il martedì o forse anche il mercoledì"},
        {"lang": "nl", "pipe": "nl_core_news_sm",
            "text": "Op maandag of dinsdag of misschien zelfs op woensdag"},
        {"lang": "no", "pipe": "nb_core_news_sm",
            "text": "På mandag eller tirsdag eller kanskje til og med på onsdag"},
        {"lang": "sv", "pipe": "sv_core_news_sm",
            "text": "På måndag eller tisdag eller kanske till och med på onsdag"}
    ]
    for test in tests:
        print(f"-------------\nlanguage = {test['lang']}")
        nlp = spacy.load(test["pipe"], disable=['ner'])
        nlp.add_pipe("dayname_ruler", last=True)
        doc = nlp(test["text"])
        for ent in doc.ents:
            print(ent.ent_id_, ent.text, ent.label_)
