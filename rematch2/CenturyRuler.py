"""
=============================================================================
Package :   rematch2.components
Module  :   CenturyRuler.py
Version :   20220803
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   ARIADNEplus
Summary :   spaCy custom pipeline component (specialized EntityRuler)
            Language-sensitive component to identify and tag ordinal centuries
            in free text. Entity type added will be "CENTURY"
Imports :   os, sys, spacy, Language, EntityRuler, Doc
Example :   nlp.add_pipe("century_ruler", last=True)           
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
History :   03/08/2022 CFB Initially created script
=============================================================================
"""
from spacy.lang.sv import Swedish
from spacy.lang.nb import Norwegian
from spacy.lang.nl import Dutch
from spacy.lang.it import Italian
from spacy.lang.fr import French
from spacy.lang.es import Spanish
from spacy.lang.en import English
from spacy.lang.de import German
from spacy.tokens import Doc
from spacy.pipeline import EntityRuler
from spacy.language import Language
import os
import sys
import spacy            # NLP library

if __package__ is None or __package__ == '':
    # uses current directory visibility
    from SeasonNameRuler import create_seasonname_ruler
    from MonthNameRuler import create_monthname_ruler
    from DateSeparatorRuler import create_dateseparator_ruler
    from DateSuffixRuler import create_datesuffix_ruler
    from DatePrefixRuler import create_dateprefix_ruler
    from OrdinalRuler import create_ordinal_ruler
    from spacypatterns import *
else:
    # uses current package visibility
    from .SeasonNameRuler import create_seasonname_ruler
    from .MonthNameRuler import create_monthname_ruler
    from .DateSeparatorRuler import create_dateseparator_ruler
    from .DateSuffixRuler import create_datesuffix_ruler
    from .DatePrefixRuler import create_dateprefix_ruler
    from .OrdinalRuler import create_ordinal_ruler
    from .spacypatterns import *


@Language.factory("century_ruler")
def create_century_ruler(nlp, name="century_ruler", patterns=[]):
    return CenturyRuler(nlp, name, patterns)


@German.factory("century_ruler")
def create_century_ruler_de(nlp, name="century_ruler_de"):
    return create_century_ruler(nlp, name, patterns_de_CENTURY)


@English.factory("century_ruler")
def create_century_ruler_en(nlp, name="century_ruler_en"):
    return create_century_ruler(nlp, name, patterns_en_CENTURY)


@Spanish.factory("century_ruler")
def create_century_ruler_es(nlp, name="century_ruler_es"):
    return create_century_ruler(nlp, name, patterns_es_CENTURY)


@French.factory("century_ruler")
def create_century_ruler_fr(nlp, name="century_ruler_fr"):
    return create_century_ruler(nlp, name, patterns_fr_CENTURY)


@Italian.factory("century_ruler")
def create_century_ruler_it(nlp, name="century_ruler_it"):
    return create_century_ruler(nlp, name, patterns_it_CENTURY)


@Dutch.factory("century_ruler")
def create_century_ruler_nl(nlp, name="century_ruler_nl"):
    return create_century_ruler(nlp, name, patterns_nl_CENTURY)


@Norwegian.factory("century_ruler")
def create_century_ruler_no(nlp, name="century_ruler_no"):
    return create_century_ruler(nlp, name, patterns_no_CENTURY)


@Swedish.factory("century_ruler")
def create_century_ruler_sv(nlp, name="century_ruler_sv"):
    return create_century_ruler(nlp, name, patterns_sv_CENTURY)


# CenturyRuler is a specialized EntityRuler
class CenturyRuler(EntityRuler):

    def __init__(self, nlp: Language, name: str, patterns=[]) -> None:
        EntityRuler.__init__(
            self,
            nlp=nlp,
            name=name,
            phrase_matcher_attr="LOWER",
            validate=True,
            overwrite_ents=True,
            ent_id_sep="||"
        )
        atomic_pipe_names = [
            "ordinal_ruler",
            "monthname_ruler",
            "seasonname_ruler",
            "dateprefix_ruler",
            "datesuffix_ruler",
            "dateseparator_ruler"
        ]
        for name in atomic_pipe_names:
            if not name in nlp.pipe_names:
                nlp.add_pipe(name, last=True)

         # add century patterns to this pipeline component
        self.add_patterns(patterns)

    """
    Note see https://github.com/explosion/spaCy/discussions/6309
    "The EntityRuler is a wrapper around the Matcher and PhraseMatcher, so if you need more control of how overlapping matches are managed, 
    you may want to use the Matcher directly instead of using the EntityRuler. 
    As a starting point, you could have a look at EntityRuler.__call__ to see how entities are matched and filtered."
    []...] If you need to store overlapping spans, you can use custom Doc or Token extensions, see: https://spacy.io/usage/processing-pipelines#custom-components-attributes
    """

    def __call__(self, doc: Doc) -> Doc:
        EntityRuler.__call__(self, doc)
        filtered = [ent for ent in doc.ents if ent.label_ not in [
            "ORDINAL", "DATEPREFIX", "DATESUFFIX", "DATESEPARATOR", "MONTHNAME", "SEASONNAME"]]
        #doc.ents = filtered
        return doc


# test the pipeline component
if __name__ == "__main__":

    tests = [
        {"lang": "de", "pipe": "de_core_news_sm",
            "text": "Das Artefakt stammt aus dem 7. bis 6. Jahrhundert v. Chr., Kann aber älter sein"},
        {"lang": "en", "pipe": "en_core_web_sm",
            "text": "the artefact dates from the 7th to 6th century BC but may be older"},
        {"lang": "es", "pipe": "es_core_news_sm",
            "text": "el artefacto data del siglo VII al VI a. C. pero puede ser más antiguo"},
        {"lang": "fr", "pipe": "fr_core_news_sm",
            "text": "l'artefact date du 7ème au 6ème siècle avant JC mais peut être plus ancien"},
        {"lang": "it", "pipe": "it_core_news_sm",
            "text": "il manufatto risale al VII-VI secolo aC ma potrebbe essere più antico"},
        {"lang": "nl", "pipe": "nl_core_news_sm",
            "text": "het artefact dateert uit de 7e tot 6e eeuw voor Christus, maar kan ouder zijn"},
        {"lang": "no", "pipe": "nb_core_news_sm",
            "text": "gjenstanden stammer fra det 7. til 6. århundre f.Kr., men kan være eldre"},
        {"lang": "sv", "pipe": "sv_core_news_sm",
            "text": "artefakten är från 700- till 600-talet f.Kr. men kan vara äldre"}
    ]
    for test in tests:
        # print header
        print(f"-------------\nlanguage = {test['lang']}")
        # load language-specific pre-built pipeline
        nlp = spacy.load(test["pipe"], disable=['ner'])
        # add custom component at the end of the pipeline
        nlp.add_pipe("century_ruler", last=True)
        # run text through the pipeline
        doc = nlp(test["text"])
        # display the current pipeline components
        print(nlp.pipe_names)

        for token in doc:
            print(f"{token.pos_}\t{token.text}\n")
        # print the doc entities
        for ent in doc.ents:
            print(ent.ent_id_, ent.text, ent.label_)