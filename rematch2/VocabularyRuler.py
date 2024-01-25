"""
=============================================================================
Package :   rematch2
Module  :   VocabularyRuler.py
Classes :   VocabularyRuler
Version :   20231027
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy custom pipeline component (specialized EntityRuler)
Imports :   EntityRuler, Language
Example :   N/A - superclass for more specialized components    
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History :   
10/10/2023 CFB Added language factory function
27/10/2023 CFB type hints added for function signatures
=============================================================================
"""
import json
import os
import sys
from pathlib import Path
from collections.abc import MutableSequence
from enum import Enum
import spacy
from spacy.pipeline import EntityRuler
from spacy.tokens import Doc
from spacy.language import Language
from pprint import pprint

import pandas as pd

if __package__ is None or __package__ == '':
    # uses current directory visibility
    from VocabularyEnum import VocabularyEnum
else:
    # uses current package visibility
    from . VocabularyEnum import VocabularyEnum


class VocabularyRuler(EntityRuler):

    def __init__(
        self,
        nlp: Language,
        name: str = "vocabulary_ruler",
        lemmatize: bool = True,
        pos: MutableSequence = [],
        min_term_length: int = 3,
        min_lemmatize_length: int = 4,
        default_label: str = "UNKNOWN",
        default_language: str = "en",
        vocabulary: MutableSequence = []
    ) -> None:

        EntityRuler.__init__(
            self,
            nlp=nlp,
            name=name,
            phrase_matcher_attr="LOWER",
            validate=False,
            overwrite_ents=True,
            ent_id_sep="||"
        )
        '''
        # is this the same as saying:
        super().__init__(
            self,
            nlp=nlp,
            name=name,
            phrase_matcher_attr="LOWER",
            validate=False,
            overwrite_ents=True,
            ent_id_sep="||"
        )'''

        # add terms from vocabulary as generated patterns
        # vocabulary: [ { id, term }, { id, term }]
        # patterns: [{id, label, language, term, pattern}, {id, label, language, term, pattern}]
        patterns = []
        for item in vocabulary:
            # clean input values before using
            clean_id = item.get("id", "").strip()
            clean_label = item.get("label", default_label).strip()
            clean_language = item.get("language", default_language).strip()
            clean_term = item.get("term", "").strip()

            # don't use if clean term length < min_term_length
            if (len(clean_term) < min_term_length):
                continue

            # create new pattern object based on clean term
            pattern = VocabularyRuler._term_to_pattern(
                nlp, clean_term, lemmatize, min_lemmatize_length, pos)

            # add new pattern to list of patterns
            patterns.append({
                "id": clean_id,
                "label": clean_label,
                "language": clean_language,
                "term": clean_term,
                "pattern":  pattern
            })

        # add the new patterns to the underlying EntityRuler
        self.add_patterns(patterns)

    def __call__(self, doc: Doc) -> Doc:
        EntityRuler.__call__(self, doc)
        return doc

    @staticmethod
    def _vocabulary_from_enum(vocab: VocabularyEnum):

        base_path = (Path(__file__).parent / "vocabularies").resolve()
        file_path = os.path.join(base_path, vocab.value)

        vocabulary = []
        with open(file_path, "r") as f:
            vocabulary = json.load(f)

        return vocabulary

    # (optionally) lemmatize each word in phrase for better chance of free-text match
    # using SAME nlp pipeline for terms being compared and document text being analysed

    @staticmethod
    def _term_to_pattern(nlp: Language, term: str = "", lemmatize: bool = False, min_lemmatize_length: int = 4, pos: MutableSequence = []):
        # normalise whitespace and force lowercase
        # (whitespace could frustrate matching and
        # lemmatization won't work if capitalised)
        clean_term = ' '.join(term.strip().lower().split())
        doc = nlp(clean_term)
        # lem = ' '.join(tok.lemma_ for tok in doc)
        pattern = []
        phrase_length = len(doc)
        term_length = len(clean_term)

        # for each term in the phrase
        for n, tok in enumerate(doc, 1):
            pat = {}

            # lemmatize term if required (and if term long enough)
            # e.g. "skirting boards":
            # { "LEMMA": "skirt" }, { "LEMMA": "board" } or
            # { "LOWER": "skirt" }, { "LOWER": "board" }
            if (lemmatize and term_length >= min_lemmatize_length):
                pat["LEMMA"] = tok.lemma_
            else:
                pat["LOWER"] = tok.text

            # add pos tags if passed in
            # note POS only applied to LAST term if multi-word phrase
            # e.g. { "LEMMA": "board", "POS": { "IN": ["NOUN", "PROPN"] }}
            if (len(pos) > 0 and n == phrase_length):
                pat["POS"] = {"IN": pos}

            pattern.append(pat)

        return pattern


@Language.factory(name="aat_activities_ruler")
def create_aat_activities_ruler(nlp: Language, name: str = "aat_activities_ruler") -> VocabularyRuler:
    return VocabularyRuler(
        nlp=nlp,
        name=name,
        default_label="ACTIVITY",
        default_language="en",
        vocabulary=VocabularyRuler._vocabulary_from_enum(
            VocabularyEnum.AAT_ACTIVITIES)
    )


@Language.factory("aat_agents_ruler")
def create_aat_agents_ruler(nlp: Language, name: str = "aat_agents_ruler") -> VocabularyRuler:
    return VocabularyRuler(
        nlp=nlp,
        name=name,
        pos=["NOUN", "PROPN"],
        default_label="AGENT",
        default_language="en",
        vocabulary=VocabularyRuler._vocabulary_from_enum(
            VocabularyEnum.AAT_AGENTS)
    )


@Language.factory("aat_associated_concepts_ruler")
def create_aat_associated_concepts_ruler(nlp: Language, name: str = "aat_associated_concepts_ruler") -> VocabularyRuler:
    return VocabularyRuler(
        nlp=nlp,
        name=name,
        default_label="ASSOCIATED_CONCEPT",
        default_language="en",
        vocabulary=VocabularyRuler._vocabulary_from_enum(
            VocabularyEnum.AAT_ASSOCIATED_CONCEPTS)
    )


@Language.factory("aat_materials_ruler")
def create_aat_materials_ruler(nlp: Language, name: str = "aat_materials_ruler") -> VocabularyRuler:
    return VocabularyRuler(
        nlp=nlp,
        name=name,
        default_label="MATERIAL",
        default_language="en",
        vocabulary=VocabularyRuler._vocabulary_from_enum(
            VocabularyEnum.AAT_MATERIALS)
    )


@Language.factory("aat_objects_ruler")
def create_aat_objects_ruler(nlp: Language, name: str = "aat_objects_ruler") -> VocabularyRuler:
    return VocabularyRuler(
        nlp=nlp,
        name=name,
        pos=["NOUN", "PROPN"],
        default_label="OBJECT",
        default_language="en",
        vocabulary=VocabularyRuler._vocabulary_from_enum(
            VocabularyEnum.AAT_OBJECTS)
    )


@Language.factory("aat_physical_attributes_ruler")
def create_aat_physical_attributes_ruler(nlp: Language, name: str = "aat_physical_attributes_ruler") -> VocabularyRuler:
    return VocabularyRuler(
        nlp=nlp,
        name=name,
        default_label="PHYSICAL_ATTRIBUTE",
        default_language="en",
        vocabulary=VocabularyRuler._vocabulary_from_enum(
            VocabularyEnum.AAT_PHYSICAL_ATTRIBUTES)
    )


@Language.factory("aat_styleperiods_ruler")
def create_aat_styleperiods_ruler(nlp: Language, name: str = "aat_styleperiods_ruler") -> VocabularyRuler:
    return VocabularyRuler(
        nlp=nlp,
        name=name,
        default_label="STYLEPERIOD",
        default_language="en",
        vocabulary=VocabularyRuler._vocabulary_from_enum(
            VocabularyEnum.AAT_STYLEPERIODS)
    )


@Language.factory("fish_archobjects_ruler")
def create_fish_archobjects_ruler(nlp: Language, name: str = "fish_archobjects_ruler") -> VocabularyRuler:
    return VocabularyRuler(
        nlp=nlp,
        name=name,
        pos=["NOUN", "PROPN"],
        default_label="OBJECT",
        default_language="en",
        vocabulary=VocabularyRuler._vocabulary_from_enum(
            VocabularyEnum.FISH_ARCHOBJECTS)
    )


@Language.factory("fish_archsciences_ruler")
def create_fish_archsciences_ruler(nlp: Language, name: str = "fish_archsciences_ruler") -> VocabularyRuler:
    return VocabularyRuler(
        nlp=nlp,
        name=name,
        default_label="ARCHSCIENCE",
        default_language="en",
        vocabulary=VocabularyRuler._vocabulary_from_enum(
            VocabularyEnum.FISH_ARCHSCIENCES)
    )


@Language.factory("fish_building_materials_ruler")
def create_fish_building_materials_ruler(nlp: Language, name: str = "fish_building_materials_ruler") -> VocabularyRuler:
    return VocabularyRuler(
        nlp=nlp,
        name=name,
        default_label="MATERIAL",
        default_language="en",
        vocabulary=VocabularyRuler._vocabulary_from_enum(
            VocabularyEnum.FISH_BUILDING_MATERIALS)
    )


@Language.factory("fish_components_ruler")
def create_fish_components_ruler(nlp: Language, name: str = "fish_components_ruler") -> VocabularyRuler:
    return VocabularyRuler(
        nlp=nlp,
        name=name,
        pos=["NOUN", "PROPN"],
        default_label="OBJECT",
        default_language="en",
        vocabulary=VocabularyRuler._vocabulary_from_enum(
            VocabularyEnum.FISH_COMPONENTS)
    )


@Language.factory("fish_event_types_ruler")
def create_fish_event_types_ruler(nlp: Language, name: str = "fish_event_types_ruler") -> VocabularyRuler:
    return VocabularyRuler(
        nlp=nlp,
        name=name,
        default_label="EVENT",
        default_language="en",
        vocabulary=VocabularyRuler._vocabulary_from_enum(
            VocabularyEnum.FISH_EVENT_TYPES)
    )


@Language.factory("fish_evidence_ruler")
def create_fish_evidence_ruler(nlp: Language, name: str = "fish_evidence_ruler") -> VocabularyRuler:
    return VocabularyRuler(
        nlp=nlp,
        name=name,
        default_label="EVIDENCE",
        default_language="en",
        vocabulary=VocabularyRuler._vocabulary_from_enum(
            VocabularyEnum.FISH_EVIDENCE)
    )


@Language.factory("fish_maritime_craft_ruler")
def create_fish_maritime_craft_ruler(nlp: Language, name: str = "fish_maritime_craft_ruler") -> VocabularyRuler:
    return VocabularyRuler(
        nlp=nlp,
        name=name,
        pos=["NOUN", "PROPN"],
        default_label="OBJECT",
        default_language="en",
        vocabulary=VocabularyRuler._vocabulary_from_enum(
            VocabularyEnum.FISH_MARITIME_CRAFT)
    )


@Language.factory("fish_monument_types_ruler")
def create_fish_monument_types_ruler(nlp: Language, name: str = "fish_monument_types_ruler") -> VocabularyRuler:
    return VocabularyRuler(
        nlp=nlp,
        name=name,
        pos=["NOUN", "PROPN"],
        default_label="OBJECT",
        default_language="en",
        vocabulary=VocabularyRuler._vocabulary_from_enum(
            VocabularyEnum.FISH_MONUMENT_TYPES)
    )


@Language.factory("fish_periods_ruler")
def create_fish_periods_ruler(nlp: Language, name: str = "fish_periods_ruler") -> VocabularyRuler:
    return VocabularyRuler(
        nlp=nlp,
        name=name,
        default_label="NAMEDPERIOD",
        default_language="en",
        vocabulary=VocabularyRuler._vocabulary_from_enum(
            VocabularyEnum.FISH_PERIODS)
    )


# test the VocabularyRuler class
if __name__ == "__main__":

    # sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    # from rematch2.spacypatterns import vocab_en_AAT_OBJECTS
    # from ..spacypatterns import vocab_en_AAT_OBJECTS

    test_text = '''Aside from three residual flints, none closely datable, the earliest remains comprised a small assemblage of Roman pottery and ceramic building material, also residual and most likely derived from a Roman farmstead found immediately to the north within the Phase II excavation area. A single sherd of Anglo-Saxon grass-tempered pottery was also residual. The earliest features, which accounted for the majority of the remains on site, relate to medieval agricultural activity focused within a large enclosure. There was little to suggest domestic occupation within the site: the pottery assemblage was modest and well abraded, whilst charred plant remains were sparse, and, as with some metallurgical residues, point to waste disposal rather than the locations of processing or consumption. A focus of occupation within the Rodley Manor site, on higher ground 160m to the north-west, seems likely, with the currently site having lain beyond this and providing agricultural facilities, most likely corrals and pens for livestock. Animal bone was absent, but the damp, low-lying ground would have been best suited to cattle. An assemblage of medieval coins recovered from the subsoil during a metal detector survey may represent a dispersed hoard.'''
    test_text = '''
    mola conducted an archaeological desk-based heritage assessment of land at fakenham road, great ryburgh, norfolk. the earliest archaeological evidence found dates from the mesolithic period. neolithic flint tools have been found close to the west and north-west of the site. a possible bronze age ring ditch has been identified to the north-east and finds dating to the period have been discovered through metal detecting surveys. iron age remains including pits and pottery have been found within the area of proposed development through trial trenching. the site lies between two roman settlements on the south-western banks of the river wensum. one lies nearby to the north-west of the site and numerous finds including coins have been discovered during a fieldwalking survey. a further roman settlement lies to the south-east where two enclosures, two kilns and two burials have recently been excavated. a middle saxon cemetery, drainage ditches, an enclosure, land divisions and a substantial boundary ditch have also recently been discovered to the south-east of the site. metal finds dating to the period have also been found to the north-west and to the east of the site during metal detecting surveys. the site lies beyond the historic core of great ryburgh. the medieval settlement developed around the junction of fakenham road and bridge road to the west of the river wensum, flanked by the medieval moated manor of ryburgh at the northern end and by st andrew's church to the south. cartographic evidence suggests that the site lay to the rear of properties fronting fakenham road during the post-medieval period and had remained as undeveloped farmland.'''

    test_text = '''
    The Excavation revealed a wealth of archaeological information. The earliest period was represented by residual finds of a Mesolithic worked flint axe in a medieval plough furrow and Bronze Age aurochs bone in an Iron Age pit. The Iron Age period consisted of several phases of a Banjo Enclosure with associated roundhouses, four-post structures, boundary ditches, pits and a quarry. In the early Roman period there was little activity other than quarrying, but later a farmstead was established with an agricultural system reminiscent of a vineyard. No evidence was recovered for the Saxon period, even as residual finds in later contexts, and thus it is assumed that the site was either unused by the population at that time, or subject to a regime that has left no trace in the archaeological record. In the medieval period a ridge and furrow cultivation system was established that cut across many earlier features but incorporated surprisingly little material from earlier periods. After the medieval period, the site appears to have been largely abandoned until Enclosure. The two phases of work took place between March - May 2000 and subsequently between August - October 2001 by CAM ARC, Cambridgeshire County Council (formerly the Archaeological Field Unit).
    '''
    # create pipeline and add one or more custom pipeline components
    nlp = spacy.load("en_core_web_sm", disable=['ner'])
    # AAT vocabulary pipeline components
    # nlp.add_pipe("aat_activities_ruler", last=True)
    # nlp.add_pipe("aat_agents_ruler", last=True)
    # nlp.add_pipe("aat_associated_concepts_ruler", last=True)
    # nlp.add_pipe("aat_materials_ruler", last=True)
    # nlp.add_pipe("aat_objects_ruler", last=True)
    # nlp.add_pipe("aat_physical_attributes_ruler", last=True)
    # nlp.add_pipe("aat_styleperiods_ruler", last=True)
    # FISH vocabulary pipeline components

    nlp.add_pipe("fish_archobjects_ruler", last=True)
    nlp.add_pipe("fish_monument_types_ruler", last=True)

    # nlp.add_pipe("fish_archsciences_ruler", last=True)
    # nlp.add_pipe("fish_building_materials_ruler", last=True)
    # nlp.add_pipe("fish_components_ruler", last=True)
    # nlp.add_pipe("fish_event_types_ruler", last=True)
    # nlp.add_pipe("fish_evidence_ruler", last=True)
    # nlp.add_pipe("fish_maritime_craft_ruler", last=True)
    # nlp.add_pipe("fish_periods_ruler", last=True)

    doc = nlp(test_text.lower())
    # explacy.print_parse_info(nlp, test_text.lower())
    # quick and dirty examination of results:
    # for ent in doc.ents:
    # print(ent.ent_id_, ent.text, ent.label_)
    for tok in doc:
        print(tok.text, tok.pos_, tok.lemma_)

    # better...
    results = [{
        "from": ent.start_char,
        "to": ent.end_char - 1,
        "id": ent.ent_id_,
        "text": ent.text,
        "type": ent.label_
    } for ent in doc.ents]

    # load results into a DataFrame object:
    df = pd.DataFrame(results)
    print(df)
