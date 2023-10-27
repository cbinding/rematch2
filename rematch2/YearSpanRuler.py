"""
=============================================================================
Package :   rematch2
Module  :   YearSpanRuler.py
Version :   20231027
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy custom pipeline component (specialized EntityRuler)
            Language-sensitive component to identify and tag ordinal centuries
            in free text. Entity type added will be "YEARSPAN"
Imports :   MutableSequence, Language, Doc
Example :   nlp.add_pipe("yearspan_ruler", last=True)           
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History :   
03/08/2022 CFB Initially created script
27/10/2023 CFB type hints added for function signatures
=============================================================================
"""
from collections.abc import MutableSequence
import spacy
from spacy.language import Language
from spacy.pipeline import EntityRuler
from spacy.tokens import Doc

from spacy.lang.de import German
from spacy.lang.en import English
from spacy.lang.es import Spanish
from spacy.lang.fr import French
from spacy.lang.it import Italian
from spacy.lang.nl import Dutch
from spacy.lang.nb import Norwegian
from spacy.lang.sv import Swedish

if __package__ is None or __package__ == '':
    # uses current directory visibility
    from spacypatterns import *
    from OrdinalRuler import create_ordinal_ruler
    from DatePrefixRuler import create_dateprefix_ruler
    from DateSuffixRuler import create_datesuffix_ruler
    from DateSeparatorRuler import create_dateseparator_ruler
    from MonthNameRuler import create_monthname_ruler
    from SeasonNameRuler import create_seasonname_ruler
else:
    # uses current package visibility
    from .spacypatterns import *
    from .OrdinalRuler import create_ordinal_ruler
    from .DatePrefixRuler import create_dateprefix_ruler
    from .DateSuffixRuler import create_datesuffix_ruler
    from .DateSeparatorRuler import create_dateseparator_ruler
    from .MonthNameRuler import create_monthname_ruler
    from .SeasonNameRuler import create_seasonname_ruler


# YearSpanRuler is a specialized EntityRuler
class YearSpanRuler(EntityRuler):

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
            "dateprefix_ruler",
            "datesuffix_ruler",
            "dateseparator_ruler",
            "ordinal_ruler",
            "monthname_ruler",
            "seasonname_ruler"
        ]

        for n in atomic_pipe_names:
            if not n in nlp.pipe_names:
                nlp.add_pipe(n, last=True)

        # add patterns to this pipeline component
        self.add_patterns(patterns)

    def __call__(self, doc: Doc) -> Doc:

        doc = EntityRuler.__call__(self, doc)

        filtered = [ent for ent in doc.ents if ent.label_ not in [
            "ORDINAL", "DATEPREFIX", "DATESUFFIX", "DATESEPARATOR", "MONTHNAME", "SEASONNAME"]]
        doc.ents = filtered
        return doc


@Language.factory("yearspan_ruler")
def create_yearspan_ruler(nlp: Language, name: str = "yearspan_ruler", patterns: MutableSequence = []) -> YearSpanRuler:
    return YearSpanRuler(nlp, name, patterns)


@German.factory("yearspan_ruler")
def create_yearspan_ruler_de(nlp: Language, name: str = "yearspan_ruler_de") -> YearSpanRuler:
    return create_yearspan_ruler(nlp, name, patterns_de_YEARSPAN)


@English.factory("yearspan_ruler")
def create_yearspan_ruler_en(nlp: Language, name: str = "yearspan_ruler_en") -> YearSpanRuler:
    return create_yearspan_ruler(nlp, name, patterns_en_YEARSPAN)


@Spanish.factory("yearspan_ruler")
def create_yearspan_ruler_es(nlp: Language, name: str = "yearspan_ruler_es") -> YearSpanRuler:
    return create_yearspan_ruler(nlp, name, patterns_es_YEARSPAN)


@French.factory("yearspan_ruler")
def create_yearspan_ruler_fr(nlp: Language, name: str = "yearspan_ruler_fr") -> YearSpanRuler:
    return create_yearspan_ruler(nlp, name, patterns_fr_YEARSPAN)


@Italian.factory("yearspan_ruler")
def create_yearspan_ruler_it(nlp: Language, name: str = "yearspan_ruler_it") -> YearSpanRuler:
    return create_yearspan_ruler(nlp, name, patterns_it_YEARSPAN)


@Dutch.factory("yearspan_ruler")
def create_yearspan_ruler_nl(nlp: Language, name: str = "yearspan_ruler_nl") -> YearSpanRuler:
    return create_yearspan_ruler(nlp, name, patterns_nl_YEARSPAN)


@Norwegian.factory("yearspan_ruler")
def create_yearspan_ruler_no(nlp: Language, name: str = "yearspan_ruler_no") -> YearSpanRuler:
    return create_yearspan_ruler(nlp, name, patterns_no_YEARSPAN)


@Swedish.factory("yearspan_ruler")
def create_yearspan_ruler_sv(nlp: Language, name: str = "yearspan_ruler_sv") -> YearSpanRuler:
    return create_yearspan_ruler(nlp, name, patterns_sv_YEARSPAN)

    
# test the YearSpanRuler class
if __name__ == "__main__":

    tests = [
        {"lang": "de", "pipe": "de_core_news_sm",
            "text": "Das Artefakt wurde von 1650 bis 1800 n. Chr. datiert und war korrodiert"},
        {"lang": "en", "pipe": "en_core_web_sm",
            "text": "The artefact was dated from 1650 to 1800 AD and was corroded"},
        {"lang": "es", "pipe": "es_core_news_sm",
            "text": "El artefacto estaba fechado entre 1650 y 1800 d. C. y estaba corroído."},
        {"lang": "fr", "pipe": "fr_core_news_sm",
            "text": "L'artefact était daté de 1650 à 1800 après JC et a été corrodé"},
        {"lang": "it", "pipe": "it_core_news_sm",
            "text": "Il manufatto fu datato dal 1650 al 1800 d.C. e fu corroso"},
        {"lang": "nl", "pipe": "nl_core_news_sm",
            "text": "Het artefact dateerde van 1650 tot 1800 na Christus en was gecorrodeerd"},
        {"lang": "no", "pipe": "nb_core_news_sm",
            "text": "Gjenstanden ble datert fra 1650 til 1800 e.Kr. og var korrodert"},
        {"lang": "sv", "pipe": "sv_core_news_sm",
            "text": "Artefakten daterades från 1650 till 1800 e.Kr. och var korroderad"}
    ]
    for test in tests:
        # print header
        print(f"-------------\nlanguage = {test['lang']}")
        # load language-specific pre-built pipeline
        nlp = spacy.load(test["pipe"], disable=['ner'])
        # add custom component at the end of the pipeline
        nlp.add_pipe("yearspan_ruler", last=True)
        # run text through the pipeline
        doc = nlp(test["text"])
        # display the current pipeline components
        #print(nlp.pipe_names)

        # for token in doc:
        # print(f"{token.pos_}\t{token.text}\n")
        # print the doc entities
        for ent in doc.ents:
            print(ent.ent_id_, ent.text, ent.label_)
