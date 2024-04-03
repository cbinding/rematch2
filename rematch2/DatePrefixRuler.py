"""
=============================================================================
Package :   rematch2
Module  :   DatePrefixRuler.py
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy custom pipeline component (specialized SpanRuler)
Imports :   os, sys, spacy, SpanRuler, Language
Example :   
    nlp = spacy.load("en_core_web_sm", disable=['ner'])
    nlp.add_pipe("dateprefix_ruler", last=True)  
    doc = nlp("constructed in early to mid 1480 to late 1275, or early 1500s")   
    # tags ["early", "mid", "lateP"] as "DATEPREFIX"      
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
#from collections.abc import MutableSequence
from spacy.pipeline import SpanRuler

# Language-specific pipelines
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


@Language.factory("dateprefix_ruler", default_config={"patterns": []})
def create_dateprefix_ruler(nlp: Language, name: str = "dateprefix_ruler", patterns: list=[]) -> SpanRuler:
    
    if not Token.has_extension("is_ordinal"):
        Token.set_extension(name="is_ordinal", getter=is_ordinal)

    normalized_patterns = normalize_patterns(
        nlp=nlp, 
        patterns=patterns,
        default_label="DATEPREFIX",
        lemmatize=False,
        min_term_length=2
    )

    ruler = SpanRuler(
        nlp=nlp,        
        name=name,
        spans_key="custom",
        phrase_matcher_attr="LOWER",
        validate=False,
        overwrite=False
    )  
      
    ruler.add_patterns(normalized_patterns)
    return ruler 


@German.factory("dateprefix_ruler")
def create_dateprefix_ruler_de(nlp: Language, name: str = "dateprefix_ruler") -> SpanRuler:
    return create_dateprefix_ruler(nlp, name, patterns_de_DATEPREFIX)


@English.factory("dateprefix_ruler")
def create_dateprefix_ruler_en(nlp: Language, name: str = "dateprefix_ruler") -> SpanRuler:
    return create_dateprefix_ruler(nlp, name, patterns_en_DATEPREFIX)


@Spanish.factory("dateprefix_ruler")
def create_dateprefix_ruler_es(nlp: Language, name: str = "dateprefix_ruler") -> SpanRuler:
    return create_dateprefix_ruler(nlp, name, patterns_es_DATEPREFIX)


@French.factory("dateprefix_ruler")
def create_dateprefix_ruler_fr(nlp: Language, name: str = "dateprefix_ruler") -> SpanRuler:
    return create_dateprefix_ruler(nlp, name, patterns_fr_DATEPREFIX)


@Italian.factory("dateprefix_ruler")
def create_dateprefix_ruler_it(nlp: Language, name: str = "dateprefix_ruler") -> SpanRuler:
    return create_dateprefix_ruler(nlp, name, patterns_it_DATEPREFIX)


@Dutch.factory("dateprefix_ruler")
def create_dateprefix_ruler_nl(nlp: Language, name: str = "dateprefix_ruler") -> SpanRuler:
    return create_dateprefix_ruler(nlp, name, patterns_nl_DATEPREFIX)


@Norwegian.factory("dateprefix_ruler")
def create_dateprefix_ruler_no(nlp: Language, name: str = "dateprefix_ruler") -> SpanRuler:
    return create_dateprefix_ruler(nlp, name, patterns_no_DATEPREFIX)


@Swedish.factory("dateprefix_ruler")
def create_dateprefix_ruler_sv(nlp: Language, name: str = "dateprefix_ruler") -> SpanRuler:
    return create_dateprefix_ruler(nlp, name, patterns_sv_DATEPREFIX)

# Polish as temp experimental substitute until Czech is available
@Polish.factory("dateprefix_ruler")
def create__dateprefix_ruler_cs(nlp: Language, name: str = "dateprefix_ruler") -> SpanRuler:
    return create_dateprefix_ruler(nlp, name, patterns_cs_DATEPREFIX)


# test the component
if __name__ == "__main__":

    tests = [
        {"lang": "de", "text": "erbaut Anfang bis Mitte 1480 bis Ende 1275 oder Anfang des 16. Jahrhunderts"},
        {"lang": "en", "text": "constructed in early to mid 1480 to late 1275, or early 1500s"},
        {"lang": "es", "text": "construido a principios o mediados de 1480 hasta finales de 1275 o principios del siglo XVI"},
        {"lang": "fr", "text": "construit du début au milieu de 1480 à la fin de 1275 ou au début des années 1500"},
        {"lang": "it", "text": "costruito dall'inizio alla metà del 1480 fino alla fine del 1275 o all'inizio del 1500"},
        {"lang": "nl", "text": "gebouwd in het begin tot midden 1480 tot eind 1275, of begin 1500"},
        {"lang": "no", "text": "konstruert tidlig til midten av 1480 til slutten av 1275, eller tidlig på 1500-tallet"},
        {"lang": "sv", "text": "byggd i början till mitten av 1480 till slutet av 1275, eller tidigt 1500-tal"}
    ]

    for test in tests:
        lang = test.get('lang', '')
        text = test.get('text', '')

        print(f"-------------\nlanguage = {lang}")
        nlp = get_pipeline_for_language(lang)
        nlp.add_pipe("dateprefix_ruler", last=True)
        doc = nlp(text)
        
        print("Tokens:\n" + DocSummary(doc).tokens("text"))
        print("Spans:\n" + DocSummary(doc).spans("text"))

