"""
=============================================================================
Package :   rematch2
Module  :   SeasonNameRuler.py
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy custom pipeline component (specialized EntityRuler)
            Language-sensitive component to identify season names
            in free text. Entity type added will be "SEASONNAME"
Imports :   os, sys, spacy, Language, EntityRuler, Doc
Example :   nlp.add_pipe("seasonname_ruler", last=True)           
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History :   
03/08/2022 CFB Initially created script
27/10/2023 CFB type hints added for function signatures
16/02/2024 CFB remove BaseRuler inheritance, use EntityRuler directly
=============================================================================
"""
import os
import sys
import spacy            # NLP library
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
    from DocSummary import DocSummary
else:
    # uses current package visibility
    from .spacypatterns import *
    from .Util import *
    from .DocSummary import DocSummary


@Language.factory("seasonname_ruler", default_config={"patterns": []})
def create_seasonname_ruler(nlp: Language, name: str = "seasonname_ruler", patterns: list=[]) -> EntityRuler:
    normalized_patterns = normalize_patterns(
        nlp=nlp, 
        patterns=patterns,
        default_label="SEASONNAME",
        lemmatize=False,
        min_term_length=3
    )
    return EntityRuler(
        nlp=nlp, 
        name=name, 
        patterns=normalized_patterns,
        phrase_matcher_attr="LOWER",
        validate=False,
        overwrite_ents=True,
        ent_id_sep="||"
    )


@German.factory("seasonname_ruler")
def create_seasonname_ruler_de(nlp: Language, name: str = "seasonname_ruler") -> EntityRuler:
    return create_seasonname_ruler(nlp, name, patterns_de_SEASONNAME)


@English.factory("seasonname_ruler")
def create_seasonname_ruler_en(nlp: Language, name: str = "seasonname_ruler") -> EntityRuler:
    return create_seasonname_ruler(nlp, name, patterns_en_SEASONNAME)


@Spanish.factory("seasonname_ruler")
def create_seasonname_ruler_es(nlp: Language, name: str = "seasonname_ruler") -> EntityRuler:
    return create_seasonname_ruler(nlp, name, patterns_es_SEASONNAME)


@French.factory("seasonname_ruler")
def create_seasonname_ruler_fr(nlp: Language, name: str = "seasonname_ruler") -> EntityRuler:
    return create_seasonname_ruler(nlp, name, patterns_fr_SEASONNAME)


@Italian.factory("seasonname_ruler")
def create_seasonname_ruler_it(nlp: Language, name: str = "seasonname_ruler") -> EntityRuler:
    return create_seasonname_ruler(nlp, name, patterns_it_SEASONNAME)


@Dutch.factory("seasonname_ruler")
def create_seasonname_ruler_nl(nlp: Language, name: str = "seasonname_ruler") -> EntityRuler:
    return create_seasonname_ruler(nlp, name, patterns_nl_SEASONNAME)


@Norwegian.factory("seasonname_ruler")
def create_seasonname_ruler_no(nlp: Language, name: str = "seasonname_ruler") -> EntityRuler:
    return create_seasonname_ruler(nlp, name, patterns_no_SEASONNAME)


@Swedish.factory("seasonname_ruler")
def create_seasonname_ruler_sv(nlp: Language, name: str = "seasonname_ruler") -> EntityRuler:
    return create_seasonname_ruler(nlp, name, patterns_sv_SEASONNAME)

# Polish as temp experimental substitute until Czech is available
@Polish.factory("seasonname_ruler")
def create_seasonname_ruler_cs(nlp: Language, name: str = "seasonname_ruler") -> EntityRuler:
    return create_seasonname_ruler(nlp, name, patterns_cs_SEASONNAME)

# test the SeasonNameRuler class
if __name__ == "__main__":

    tests = [
        {"lang": "de", "text": "Im Frühling oder im Sommer oder im Herbst oder im Winter"},
        {"lang": "en", "text": "In Spring, or in Summer, or in Autumn or in Winter"},
        {"lang": "es", "text": "En primavera, o en verano, o en otoño o en invierno"},
        {"lang": "fr", "text": "Au printemps, ou en été, ou en automne ou en hiver"},
        {"lang": "it", "text": "In primavera, o in estate, o in autunno o in inverno"},
        {"lang": "nl", "text": "In de lente, of in de zomer, of in de herfst of in de winter"},
        {"lang": "no", "text": "Om våren, eller om sommeren, eller om høsten eller om vinteren"},
        {"lang": "sv", "text": "På våren, eller på sommaren, eller på hösten eller på vintern"}
    ]
    for test in tests:
        lang = test.get("lang", "")
        text = test.get("text", "")

        print(f"-------------\nlanguage = {lang}")
        nlp = get_pipeline_for_language(lang)
        nlp.add_pipe("seasonname_ruler", last=True)
        doc = nlp(text)
        
        print("Tokens:\n" + DocSummary(doc).tokens("text"))
        print("Entities:\n" + DocSummary(doc).entities("text"))

