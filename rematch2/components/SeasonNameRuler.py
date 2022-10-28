"""
=============================================================================
Package :   rematch2.components
Module  :   SeasonNameRuler.py
Version :   20220803
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   ARIADNEplus
Summary :   spaCy custom pipeline component (specialized EntityRuler)
            Language-sensitive component to identify season names
            in free text. Entity type added will be "SEASONNAME"
Imports :   os, sys, spacy, Language, EntityRuler, Doc
Example :   nlp.add_pipe("seasonname_ruler", last=True)           
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

import rematch2.patterns

from ..patterns import \
    patterns_de_SEASONNAME, \
    patterns_en_SEASONNAME, \
    patterns_es_SEASONNAME, \
    patterns_fr_SEASONNAME, \
    patterns_it_SEASONNAME, \
    patterns_nl_SEASONNAME, \
    patterns_no_SEASONNAME, \
    patterns_sv_SEASONNAME

from .PatternRuler import PatternRuler

#module_path = os.path.abspath(os.path.join('..', 'src'))
# if module_path not in sys.path:
# sys.path.append(module_path)


@Language.factory("seasonname_ruler")
def create_seasonname_ruler(nlp, name="seasonname_ruler", patterns=[]):
    return PatternRuler(nlp, name, patterns)


@German.factory("seasonname_ruler")
def create_seasonname_ruler_de(nlp, name="seasonname_ruler_de"):
    return create_seasonname_ruler(nlp, name, patterns_de_SEASONNAME)


@English.factory("seasonname_ruler")
def create_seasonname_ruler_en(nlp, name="seasonname_ruler_en"):
    return create_seasonname_ruler(nlp, name, patterns_en_SEASONNAME)


@Spanish.factory("seasonname_ruler")
def create_seasonname_ruler_es(nlp, name="seasonname_ruler_es"):
    return create_seasonname_ruler(nlp, name, patterns_es_SEASONNAME)


@French.factory("seasonname_ruler")
def create_seasonname_ruler_fr(nlp, name="seasonname_ruler_fr"):
    return create_seasonname_ruler(nlp, name, patterns_fr_SEASONNAME)


@Italian.factory("seasonname_ruler")
def create_seasonname_ruler_it(nlp, name="seasonname_ruler_it"):
    return create_seasonname_ruler(nlp, name, patterns_it_SEASONNAME)


@Dutch.factory("seasonname_ruler")
def create_seasonname_ruler_nl(nlp, name="seasonname_ruler_nl"):
    return create_seasonname_ruler(nlp, name, patterns_nl_SEASONNAME)


@Norwegian.factory("seasonname_ruler")
def create_seasonname_ruler_no(nlp, name="seasonname_ruler_no"):
    return create_seasonname_ruler(nlp, name, patterns_no_SEASONNAME)


@Swedish.factory("seasonname_ruler")
def create_seasonname_ruler_sv(nlp, name="seasonname_ruler_sv"):
    return create_seasonname_ruler(nlp, name, patterns_sv_SEASONNAME)


# test the SeasonNameRuler class
if __name__ == "__main__":

    tests = [
        {"language": "de", "pipe": "de_core_news_sm",
            "text": "Im Frühling oder im Sommer oder im Herbst oder im Winter"},
        {"language": "en", "pipe": "en_core_web_sm",
            "text": "In Spring, or in Summer, or in Autumn or in Winter"},
        {"language": "es", "pipe": "es_core_news_sm",
            "text": "En primavera, o en verano, o en otoño o en invierno"},
        {"language": "fr", "pipe": "fr_core_news_sm",
            "text": "Au printemps, ou en été, ou en automne ou en hiver"},
        {"language": "it", "pipe": "it_core_news_sm",
            "text": "In primavera, o in estate, o in autunno o in inverno"},
        {"language": "nl", "pipe": "nl_core_news_sm",
            "text": "In de lente, of in de zomer, of in de herfst of in de winter"},
        {"language": "no", "pipe": "nb_core_news_sm",
            "text": "Om våren, eller om sommeren, eller om høsten eller om vinteren"},
        {"language": "sv", "pipe": "sv_core_news_sm",
            "text": "På våren, eller på sommaren, eller på hösten eller på vintern"}
    ]
    for test in tests:
        print(f"-------------\nlanguage = {test['language']}")
        nlp = spacy.load(test["pipe"], disable=['ner'])
        nlp.add_pipe("seasonname_ruler", last=True)
        doc = nlp(test["text"])
        for ent in doc.ents:
            print(ent.ent_id_, ent.text, ent.label_)
