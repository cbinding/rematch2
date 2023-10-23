"""
=============================================================================
Package :   rematch2.components
Module  :   OrdinalRuler.py
Version :   20220803
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   ARIADNEplus
Summary :   spaCy custom pipeline component to identify ordinals in free text 
            Entity type added will be "ORDINAL"
Imports :   os, sys, spacy, PatternRuler
Example :   nlp.add_pipe("ordinal_ruler", last=True)           
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
History :   03/08/2022 CFB Initially created script
=============================================================================
"""
# Third party imports
import spacy

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

# Local application imports
from ..spacypatterns import \
    patterns_de_ORDINAL, \
    patterns_en_ORDINAL, \
    patterns_es_ORDINAL, \
    patterns_fr_ORDINAL, \
    patterns_it_ORDINAL, \
    patterns_nl_ORDINAL, \
    patterns_no_ORDINAL, \
    patterns_sv_ORDINAL

#from .PatternRuler import PatternRuler


@Language.factory("ordinal_ruler")
def create_ordinal_ruler(nlp, name="ordinal_ruler", patterns=[]):
    return EntityRuler(
        nlp=nlp,
        name=name,
        phrase_matcher_attr="LOWER",
        validate=True,
        overwrite_ents=True,
        ent_id_sep="||",
        patterns=patterns
    )


@German.factory("ordinal_ruler")
def create_ordinal_ruler_de(nlp, name="ordinal_ruler_de"):
    return create_ordinal_ruler(nlp, name, patterns_de_ORDINAL)


@English.factory("ordinal_ruler")
def create_ordinal_ruler_en(nlp, name="ordinal_ruler_en"):
    return create_ordinal_ruler(nlp, name, patterns_en_ORDINAL)


@Spanish.factory("ordinal_ruler")
def create_ordinal_ruler_es(nlp, name="ordinal_ruler_es"):
    return create_ordinal_ruler(nlp, name, patterns_es_ORDINAL)


@French.factory("ordinal_ruler")
def create_ordinal_ruler_fr(nlp, name="ordinal_ruler_fr"):
    return create_ordinal_ruler(nlp, name, patterns_fr_ORDINAL)


@Italian.factory("ordinal_ruler")
def create_ordinal_ruler_it(nlp, name="ordinal_ruler_it"):
    return create_ordinal_ruler(nlp, name, patterns_it_ORDINAL)


@Dutch.factory("ordinal_ruler")
def create_ordinal_ruler_nl(nlp, name="ordinal_ruler_nl"):
    return create_ordinal_ruler(nlp, name, patterns_nl_ORDINAL)


@Norwegian.factory("ordinal_ruler")
def create_ordinal_ruler_no(nlp, name="ordinal_ruler_no"):
    return create_ordinal_ruler(nlp, name, patterns_no_ORDINAL)


@Swedish.factory("ordinal_ruler")
def create_ordinal_ruler_sv(nlp, name="ordinal_ruler_sv"):
    return create_ordinal_ruler(nlp, name, patterns_sv_ORDINAL)


# test the material_ruler pipeline component
if __name__ == "__main__":

    tests = [
        {"lang": "de", "pipe": "de_core_news_sm",
            "text": "vom ersten, vierten und sechsten bis zum 19. oder 20. Jahrhundert"},
        {"lang": "en", "pipe": "en_core_web_sm",
            "text": "from the first, the fourth and the sixth to the 19th or 20th century"},
        {"lang": "es", "pipe": "es_core_news_sm",
            "text": "desde el primero, el cuarto y el sexto hasta el siglo XIX o XX"},
        {"lang": "fr", "pipe": "fr_core_news_sm",
            "text": "du premier, quatrième et sixième au XIXe ou XXe siècle"},
        {"lang": "it", "pipe": "it_core_news_sm",
            "text": "dal primo, quarto e sesto al XIX o XX secolo"},
        {"lang": "nl", "pipe": "nl_core_news_sm",
            "text": "van de eerste, de vierde en de zesde tot de 19e of 20e eeuw"},
        {"lang": "no", "pipe": "nb_core_news_sm",
            "text": "fra det første, det fjerde og det sjette til det 19. eller 20. århundre"},
        {"lang": "sv", "pipe": "sv_core_news_sm",
            "text": "från det första, det fjärde och det sjätte till 1800- eller 1900-talet"}
    ]
    for test in tests:
        print(f"-------------\nlanguage = {test['lang']}")
        nlp = spacy.load(test["pipe"], disable=['ner'])
        nlp.add_pipe("ordinal_ruler", last=True)
        doc = nlp(test["text"])

        # for token in doc:
        # print(f"{token.pos_}\t{token.text}\n")

        for ent in doc.ents:
            print(ent.ent_id_, ent.text, ent.label_)
