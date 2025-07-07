"""
=============================================================================
Package :   rematch2
Module  :   OrdinalRuler.py
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy custom pipeline component to identify ordinals in free text 
            SPan label will be "ORDINAL"
Imports :   os, sys, spacy, SpanRuler
Example :   nlp.add_pipe("ordinal_ruler", last=True)           
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History :   
03/08/2022 CFB Initially created script
27/10/2023 CFB type hints added for function signatures
16/02/2024 CFB remove BaseRuler inheritance, use EntityRuler directly
28/03/2024 CFB based on SpanRuler instead of EntityRuler
02/07/2025 CFB based on BaseRuler instead of SpanRuler(!)
=============================================================================
"""
# Third party imports
import spacy
#from spacy.pipeline import SpanRuler

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

from .spacypatterns import *
from .Util import *
from .BaseRuler import BaseRuler
from .DocSummary import DocSummary


@Language.factory("ordinal_ruler", default_config={"patterns": []})
def create_ordinal_ruler(nlp: Language, name: str="ordinal_ruler", patterns: list=[]) -> BaseRuler:
    

    ruler = BaseRuler(
        nlp=nlp,        
        name=name,
        spans_key="rematch",
        phrase_matcher_attr="LOWER",
        validate=False,
        overwrite=False
    ) 

    normalized_patterns = BaseRuler.normalize_patterns(
        nlp=nlp, 
        patterns=patterns,
        default_label="ORDINAL",
        lemmatize=False,
        min_term_length=2
    )

    ruler.add_patterns(normalized_patterns)
    return ruler 


@German.factory("ordinal_ruler")
def create_ordinal_ruler_de(nlp: Language, name: str = "ordinal_ruler") -> BaseRuler:
    return create_ordinal_ruler(nlp, name, patterns_de_ORDINAL)


@English.factory("ordinal_ruler")
def create_ordinal_ruler_en(nlp: Language, name: str = "ordinal_ruler") -> BaseRuler:
    return create_ordinal_ruler(nlp, name, patterns_en_ORDINAL)


@Spanish.factory("ordinal_ruler")
def create_ordinal_ruler_es(nlp: Language, name: str = "ordinal_ruler") -> BaseRuler:
    return create_ordinal_ruler(nlp, name, patterns_es_ORDINAL)


@French.factory("ordinal_ruler")
def create_ordinal_ruler_fr(nlp: Language, name: str = "ordinal_ruler") -> BaseRuler:
    return create_ordinal_ruler(nlp, name, patterns_fr_ORDINAL)


@Italian.factory("ordinal_ruler")
def create_ordinal_ruler_it(nlp: Language, name: str = "ordinal_ruler") -> BaseRuler:
    return create_ordinal_ruler(nlp, name, patterns_it_ORDINAL)


@Dutch.factory("ordinal_ruler")
def create_ordinal_ruler_nl(nlp: Language, name: str = "ordinal_ruler") -> BaseRuler:
    return create_ordinal_ruler(nlp, name, patterns_nl_ORDINAL)


@Norwegian.factory("ordinal_ruler")
def create_ordinal_ruler_no(nlp: Language, name: str = "ordinal_ruler") -> BaseRuler:
    return create_ordinal_ruler(nlp, name, patterns_no_ORDINAL)


@Swedish.factory("ordinal_ruler")
def create_ordinal_ruler_sv(nlp: Language, name: str = "ordinal_ruler") -> BaseRuler:
    return create_ordinal_ruler(nlp, name, patterns_sv_ORDINAL)


# Polish as temp experimental substitute until Czech is available
@Polish.factory("ordinal_ruler")
def create_ordinal_ruler_cs(nlp: Language, name: str = "ordinal_ruler") -> BaseRuler:
    return create_ordinal_ruler(nlp, name, patterns_cs_ORDINAL)


# test the material_ruler pipeline component
if __name__ == "__main__":

    tests = [
        {"lang": "de", "text": "vom ersten, vierten und sechsten bis zum 19. oder 20. Jahrhundert"},
        {"lang": "en", "text": "the artefact dates from the 7th to 6th century BC but may be older"},
        {"lang": "es", "text": "desde el primero, el cuarto y el sexto hasta el siglo XIX o XX"},
        {"lang": "fr", "text": "du premier, quatrième et sixième au XIXe ou XXe siècle"},
        {"lang": "it", "text": "dal primo, quarto e sesto al XIX o XX secolo"},
        {"lang": "nl", "text": "van de eerste, de vierde en de zesde tot de 19e of 20e eeuw"},
        {"lang": "no", "text": "fra det første, det fjerde og det sjette til det 19. eller 20. århundre"},
        {"lang": "sv", "text": "från det första, det fjärde och det sjätte till 1800- eller 1900-talet"},
        {"lang": "cs", "text": "artefakt pochází ze 7. až 6. století př. n. l., ale může být i starší"}
    ]
    for test in tests:
        lang = test.get("lang", "")
        text = test.get("text", "")

        print(f"-------------\nlanguage = {lang}")
        nlp = get_pipeline_for_language(lang)
        nlp.add_pipe("ordinal_ruler", last=True)
        
        doc = nlp(text)

        print("Tokens:\n" + DocSummary(doc).tokens_to_text())
        print("Spans:\n" + DocSummary(doc).spans_to_text())
       
