"""
=============================================================================
Package :   rematch2
Module  :   OrdinalRuler.py
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy custom pipeline component to identify ordinals in free text 
            Entity type added will be "ORDINAL"
Imports :   os, sys, spacy, EntityRuler
Example :   nlp.add_pipe("ordinal_ruler", last=True)           
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History :   
03/08/2022 CFB Initially created script
27/10/2023 CFB type hints added for function signatures
16/02/2024 CFB remove BaseRuler inheritance, use EntityRuler directly
=============================================================================
"""
# Third party imports
import spacy
from spacy.pipeline import EntityRuler

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
    from Util import *
else:
    # uses current package visibility
    from .spacypatterns import *
    from .Util import *


@Language.factory("ordinal_ruler", default_config={"patterns": []})
def create_ordinal_ruler(nlp: Language, name: str="ordinal_ruler", patterns: list=[]) -> EntityRuler:
    normalized_patterns = normalize_patterns(
        nlp=nlp, 
        patterns=patterns,
        default_label="ORDINAL",
        lemmatize=False,
        min_term_length=2
    )
    #print(normalized_patterns)
    return EntityRuler(
        nlp=nlp, 
        name=name, 
        patterns=normalized_patterns,
        phrase_matcher_attr="LOWER",
        validate=False,
        overwrite_ents=True,
        ent_id_sep="||"
    )


@German.factory("ordinal_ruler")
def create_ordinal_ruler_de(nlp: Language, name: str = "ordinal_ruler") -> EntityRuler:
    return create_ordinal_ruler(nlp, name, patterns_de_ORDINAL)


@English.factory("ordinal_ruler")
def create_ordinal_ruler_en(nlp: Language, name: str = "ordinal_ruler") -> EntityRuler:
    return create_ordinal_ruler(nlp, name, patterns_en_ORDINAL)


@Spanish.factory("ordinal_ruler")
def create_ordinal_ruler_es(nlp: Language, name: str = "ordinal_ruler") -> EntityRuler:
    return create_ordinal_ruler(nlp, name, patterns_es_ORDINAL)


@French.factory("ordinal_ruler")
def create_ordinal_ruler_fr(nlp: Language, name: str = "ordinal_ruler") -> EntityRuler:
    return create_ordinal_ruler(nlp, name, patterns_fr_ORDINAL)


@Italian.factory("ordinal_ruler")
def create_ordinal_ruler_it(nlp: Language, name: str = "ordinal_ruler") -> EntityRuler:
    return create_ordinal_ruler(nlp, name, patterns_it_ORDINAL)


@Dutch.factory("ordinal_ruler")
def create_ordinal_ruler_nl(nlp: Language, name: str = "ordinal_ruler") -> EntityRuler:
    return create_ordinal_ruler(nlp, name, patterns_nl_ORDINAL)


@Norwegian.factory("ordinal_ruler")
def create_ordinal_ruler_no(nlp: Language, name: str = "ordinal_ruler") -> EntityRuler:
    return create_ordinal_ruler(nlp, name, patterns_no_ORDINAL)


@Swedish.factory("ordinal_ruler")
def create_ordinal_ruler_sv(nlp: Language, name: str = "ordinal_ruler") -> EntityRuler:
    return create_ordinal_ruler(nlp, name, patterns_sv_ORDINAL)


# Polish as temp experimental substitute until Czech is available
@Polish.factory("ordinal_ruler")
def create_ordinal_ruler_cs(nlp: Language, name: str = "ordinal_ruler") -> EntityRuler:
    return create_ordinal_ruler(nlp, name, patterns_cs_ORDINAL)


# test the material_ruler pipeline component
if __name__ == "__main__":

    tests = [
        {"lang": "de", "pipe": "de_core_news_sm",
            "text": "vom ersten, vierten und sechsten bis zum 19. oder 20. Jahrhundert"},
        {"lang": "en", "pipe": "en_core_web_sm",
            #"text": "from the first, the fourth and the sixth to the 19th or 20th century"},
            "text": "the artefact dates from the 7th to 6th century BC but may be older"},
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
            "text": "från det första, det fjärde och det sjätte till 1800- eller 1900-talet"},
        {"lang": "cs", "pipe": "pl_core_news_sm",
            "text": "artefakt pochází ze 7. až 6. století př. n. l., ale může být i starší"}
    ]
    for test in tests:
        print(f"-------------\nlanguage = {test['lang']}")
        nlp = spacy.load(test["pipe"], disable=['ner'])
        nlp.add_pipe("ordinal_ruler", last=True)
        doc = nlp(test["text"])

        for token in doc:
            print(f"{token.pos_}\t{token.text}\n")

        for ent in doc.ents:
            print(ent.ent_id_, ent.text, ent.label_)
