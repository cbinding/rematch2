"""
=============================================================================
Package :   rematch2
Module  :   MonthNameRuler.py
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy custom pipeline component (specialized SpanRuler)
            Language-sensitive component to identify month names
            in free text. Span label will be "MONTHNAME"
Imports :   os, sys, spacy, Language, SpanRuler, Doc
Example :   nlp.add_pipe("monthname_ruler", last=True)           
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
from spacy.language import Language
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


@Language.factory("monthname_ruler", default_config={"patterns": []})
def create_monthname_ruler(nlp: Language, name: str="monthname_ruler", patterns: list=[]) -> BaseRuler:
    
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
        default_label="MONTHNAME",
        lemmatize=False,
        min_term_length=3
    )

    ruler.add_patterns(normalized_patterns)
    return ruler 
    

@German.factory("monthname_ruler")
def create_monthname_ruler_de(nlp: Language, name: str = "monthname_ruler") -> BaseRuler:
    return create_monthname_ruler(nlp, name, patterns_de_MONTHNAME)


@English.factory("monthname_ruler")
def create_monthname_ruler_en(nlp: Language, name: str = "monthname_ruler") -> BaseRuler:
    return create_monthname_ruler(nlp, name, patterns_en_MONTHNAME)


@Spanish.factory("monthname_ruler")
def create_monthname_ruler_es(nlp: Language, name: str = "monthname_ruler") -> BaseRuler:
    return create_monthname_ruler(nlp, name, patterns_es_MONTHNAME)


@French.factory("monthname_ruler")
def create_monthname_ruler_fr(nlp: Language, name: str = "monthname_ruler") -> BaseRuler:
    return create_monthname_ruler(nlp, name, patterns_fr_MONTHNAME)


@Italian.factory("monthname_ruler")
def create_monthname_ruler_it(nlp: Language, name: str = "monthname_ruler") -> BaseRuler:
    return create_monthname_ruler(nlp, name, patterns_it_MONTHNAME)


@Dutch.factory("monthname_ruler")
def create_monthname_ruler_nl(nlp: Language, name: str = "monthname_ruler") -> BaseRuler:
    return create_monthname_ruler(nlp, name, patterns_nl_MONTHNAME)


@Norwegian.factory("monthname_ruler")
def create_monthname_ruler_no(nlp: Language, name: str = "monthname_ruler") -> BaseRuler:
    return create_monthname_ruler(nlp, name, patterns_no_MONTHNAME)


@Swedish.factory("monthname_ruler")
def create_monthname_ruler_sv(nlp: Language, name: str = "monthname_ruler") -> BaseRuler:
    return create_monthname_ruler(nlp, name, patterns_sv_MONTHNAME)

# Polish as temp experimental substitute until Czech is available
@Polish.factory("monthname_ruler")
def create_monthname_ruler_cs(nlp: Language, name: str = "monthname_ruler") -> BaseRuler:
    return create_monthname_ruler(nlp, name, patterns_cs_MONTHNAME)


# test the MonthNameRuler class
if __name__ == "__main__":

    tests = [
        {"lang": "de", "text": "Im Januar oder im März oder im Oktober, vielleicht im Dezember?"},
        {"lang": "en", "text": "In January or in March or in October, maybe in Dec"},
        {"lang": "es", "text": "¿En enero o en marzo o en octubre, tal vez en diciembre?"},
        {"lang": "fr", "text": "En janvier ou en mars ou en octobre, peut-être en décembre?"},
        {"lang": "it", "text": "A gennaio o a marzo o a ottobre, forse a dicembre?"},
        {"lang": "nl", "text": "In januari of in maart of in oktober, misschien in december?"},
        {"lang": "no", "text": "I januar eller i mars eller i oktober, kanskje i desember?"},
        {"lang": "sv", "text": "I januari eller i mars eller i oktober, kanske i december?"}
    ]
    
    for test in tests:
        lang = test.get("lang", "")
        text = test.get("text", "")

        print(f"-------------\nlanguage = {lang}")
        nlp = get_pipeline_for_language(lang)
        nlp.add_pipe("monthname_ruler", last=True)
        doc = nlp(text)

        print("Tokens:\n" + DocSummary(doc).tokens("text"))
        print("Spans:\n" + DocSummary(doc).spans("text"))