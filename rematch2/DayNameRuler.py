"""
=============================================================================
Package :   rematch2
Module  :   DayNameRuler.py
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy custom pipeline component (specialized SpanRuler)
            Language-sensitive component to identify day names
            in free text. Span label will be "DAYNAME"
Imports :   os, sys, spacy, Language, SpanRuler, Doc
Example :   
    nlp = spacy.load("en_core_web_sm", disable=['ner'])
    nlp.add_pipe("dateprefix_ruler", last=True)  
    doc = nlp("On Monday, Tuesday or even Wednesday")   
    # tags ["Monday", "Tuesday", "Wednesday"] as "DAYNAME"          
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History :   
03/08/2022 CFB Initially created script
27/10/2023 CFB type hints added for function signatures
16/02/2024 CFB remove BaseRuler inheritance, use EntityRuler directly
28/03/2024 CFB base on SpanRuler instead of EntityRuler
=============================================================================
"""
import os
import sys
import spacy            # NLP library
from spacy.pipeline import SpanRuler

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
    from DocSummary import DocSummary
else:
    # uses current package visibility
    from .spacypatterns import *
    from .Util import *
    from .DocSummary import DocSummary


@Language.factory("dayname_ruler", default_config={"patterns": []})
def create_dayname_ruler(nlp: Language, name: str="dayname_ruler", patterns: list=[]) -> SpanRuler:
    normalized_patterns = normalize_patterns(
        nlp=nlp, 
        patterns=patterns,
        default_label="DAYNAME",
        lemmatize=False,
        min_term_length=3
    )

    ruler = SpanRuler(
        nlp=nlp,        
        name=name,
        spans_key="rematch",
        phrase_matcher_attr="LOWER",
        validate=False,
        overwrite=False
    )  
      
    ruler.add_patterns(normalized_patterns)
    return ruler 
    

@German.factory("dayname_ruler")
def create_dayname_ruler_de(nlp: Language, name: str = "dayname_ruler") -> SpanRuler:
    return create_dayname_ruler(nlp, name, patterns_de_DAYNAME)


@English.factory("dayname_ruler")
def create_dayname_ruler_en(nlp: Language, name: str = "dayname_ruler") -> SpanRuler:
    return create_dayname_ruler(nlp, name, patterns_en_DAYNAME)


@Spanish.factory("dayname_ruler")
def create_dayname_ruler_es(nlp: Language, name: str = "dayname_ruler") -> SpanRuler:
    return create_dayname_ruler(nlp, name, patterns_es_DAYNAME)


@French.factory("dayname_ruler")
def create_dayname_ruler_fr(nlp: Language, name: str = "dayname_ruler") -> SpanRuler:
    return create_dayname_ruler(nlp, name, patterns_fr_DAYNAME)


@Italian.factory("dayname_ruler")
def create_dayname_ruler_it(nlp: Language, name: str = "dayname_ruler") -> SpanRuler:
    return create_dayname_ruler(nlp, name, patterns_it_DAYNAME)


@Dutch.factory("dayname_ruler")
def create_dayname_ruler_nl(nlp: Language, name: str = "dayname_ruler") -> SpanRuler:
    return create_dayname_ruler(nlp, name, patterns_nl_DAYNAME)


@Norwegian.factory("dayname_ruler")
def create_dayname_ruler_no(nlp: Language, name: str = "dayname_ruler") -> SpanRuler:
    return create_dayname_ruler(nlp, name, patterns_no_DAYNAME)


@Swedish.factory("dayname_ruler")
def create_dayname_ruler_sv(nlp: Language, name: str = "dayname_ruler") -> SpanRuler:
    return create_dayname_ruler(nlp, name, patterns_sv_DAYNAME)

# Using Polish as temp experimental substitute until Czech is available
@Polish.factory("dayname_ruler")
def create_dayname_ruler_cs(nlp: Language, name: str = "dayname_ruler") -> SpanRuler:
    return create_dayname_ruler(nlp, name, patterns_cs_DAYNAME)

# test the DayNameRuler class
if __name__ == "__main__":

    tests = [
        {"lang": "de", "text": "Am Montag oder Dienstag oder vielleicht sogar am Mittwoch"},
        {"lang": "en", "text": "On Monday or Tuesday or maybe even on Wednesday"},
        {"lang": "es", "text": "El lunes o el martes o tal vez incluso el miércoles"},
        {"lang": "fr", "text": "Le lundi ou le mardi ou peut-être même le mercredi"},
        {"lang": "it", "text": "Il lunedì o il martedì o forse anche il mercoledì"},
        {"lang": "nl", "text": "Op maandag of dinsdag of misschien zelfs op woensdag"},
        {"lang": "no", "text": "På mandag eller tirsdag eller kanskje til og med på onsdag"},
        {"lang": "sv", "text": "På måndag eller tisdag eller kanske till och med på onsdag"}
    ]
    for test in tests:
        lang = test.get("lang", "")
        text = test.get("text", "")

        print(f"-------------\nlanguage = {lang}")
        nlp = get_pipeline_for_language(lang)
        nlp.add_pipe("dayname_ruler", last=True)
        doc = nlp(text)

        print("Tokens:\n" + DocSummary(doc).tokens("text"))
        print("Entities:\n" + DocSummary(doc).spans("text"))

