"""
=============================================================================
Package :   rematch2.components
Module  :   VocabularyRuler.py
Version :   20231010
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   ARIADNEplus
Summary :   spaCy custom pipeline component (specialized EntityRuler)
Imports :   EntityRuler, Language
Example :   N/A - superclass for more specialized components    
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
History :   
10/10/2023 CFB Added language factory function
=============================================================================
"""
import json
import os
import sys
from pathlib import Path
import spacy
from spacy.pipeline import EntityRuler
from spacy.tokens import Doc
from spacy.language import Language
from pprint import pprint
from enum import Enum
import pandas as pd


class VocabularyEnum(Enum):
    AAT_ACTIVITIES = "vocab_en_AAT_ACTIVITIES_20231018.json"
    AAT_AGENTS = "vocab_en_AAT_AGENTS_20231018.json"
    AAT_ASSOCIATED_CONCEPTS = "vocab_en_AAT_ASSOCIATED_CONCEPTS_20231018.json"
    AAT_MATERIALS = "vocab_en_AAT_MATERIALS_20231018.json"
    AAT_OBJECTS = "vocab_en_AAT_OBJECTS_20231018.json"
    AAT_PHYSICAL_ATTRIBUTES = "vocab_en_AAT_PHYSICAL_ATTRIBUTES_20231018.json"
    AAT_STYLEPERIODS = "vocab_en_AAT_STYLEPERIODS_20231018.json"
    FISH_ARCHOBJECTS = "vocab_en_FISH_ARCHOBJECTS_20210921.json"
    FISH_ARCHSCIENCES = "vocab_en_FISH_ARCHSCIENCES_20210921.json"
    FISH_BUILDING_MATERIALS = "vocab_en_FISH_BUILDING_MATERIALS_20210921.json"
    FISH_COMPONENTS = "vocab_en_FISH_COMPONENTS_20210921.json"
    FISH_EVENT_TYPES = "vocab_en_FISH_EVENT_TYPES_20210921.json"
    FISH_EVIDENCE = "vocab_en_FISH_EVIDENCE_20210921.json"
    FISH_MARITIME_CRAFT = "vocab_en_FISH_MARITIME_CRAFT_20221104.json"
    FISH_MONUMENT_TYPES = "vocab_en_FISH_MONUMENT_TYPES_20210921.json"
    FISH_PERIODS = "vocab_en_FISH_PERIODS_20211011.json"


def _get_vocabulary(vocab: VocabularyEnum = VocabularyEnum.AAT_OBJECTS):

    base_path = (Path(__file__).parent / "vocabularies").resolve()
    file_path = os.path.join(base_path, vocab.value)

    vocabulary = []
    with open(file_path, "r") as f:
        vocabulary = json.load(f)

    return vocabulary


@Language.factory("aat_activities_ruler")
def create_aatactivities_ruler(nlp, name="aat_activities_ruler"):
    return create_vocabulary_ruler(
        nlp=nlp,
        name=name,
        min_lemmatize_length=4,
        min_term_length=3,
        lemmatize=True,
        pos=["VERB"],
        default_label="ACTIVITY",
        default_language="en",
        vocabulary=_get_vocabulary(VocabularyEnum.AAT_ACTIVITIES)
    )


@Language.factory("aat_agents_ruler")
def create_aat_agents_ruler(nlp, name="aat_agents_ruler"):
    return create_vocabulary_ruler(
        nlp=nlp,
        name=name,
        min_lemmatize_length=4,
        min_term_length=3,
        lemmatize=True,
        pos=["NOUN"],
        default_label="AGENT",
        default_language="en",
        vocabulary=_get_vocabulary(VocabularyEnum.AAT_AGENTS)
    )


@Language.factory("aat_associated_concepts_ruler")
def create_aat_associated_concepts_ruler(nlp, name="aat_associated_concepts_ruler"):
    return create_vocabulary_ruler(
        nlp=nlp,
        name=name,
        min_lemmatize_length=4,
        min_term_length=3,
        lemmatize=True,
        pos=[],
        default_label="ASSOCIATED_CONCEPT",
        default_language="en",
        vocabulary=_get_vocabulary(VocabularyEnum.AAT_ASSOCIATED_CONCEPTS)
    )


@Language.factory("aat_materials_ruler")
def create_aat_materials_ruler(nlp, name="aat_materials_ruler"):
    return create_vocabulary_ruler(
        nlp=nlp,
        name=name,
        min_lemmatize_length=4,
        min_term_length=3,
        lemmatize=True,
        pos=[],
        default_label="MATERIAL",
        default_language="en",
        vocabulary=_get_vocabulary(VocabularyEnum.AAT_MATERIALS)
    )


@Language.factory("aat_objects_ruler")
def create_aat_objects_ruler(nlp, name="aat_objects_ruler"):
    return create_vocabulary_ruler(
        nlp=nlp,
        name=name,
        min_lemmatize_length=4,
        min_term_length=3,
        lemmatize=True,
        pos=["NOUN"],
        default_label="OBJECT",
        default_language="en",
        vocabulary=_get_vocabulary(VocabularyEnum.AAT_OBJECTS)
    )


@Language.factory("aat_physical_attributes_ruler")
def create_aat_physical_attributes_ruler(nlp, name="aat_physical_attributes_ruler"):
    return create_vocabulary_ruler(
        nlp=nlp,
        name=name,
        min_lemmatize_length=4,
        min_term_length=3,
        lemmatize=True,
        pos=[],
        default_label="PHYSICAL_ATTRIBUTE",
        default_language="en",
        vocabulary=_get_vocabulary(VocabularyEnum.AAT_PHYSICAL_ATTRIBUTES)
    )


@Language.factory("aat_styleperiods_ruler")
def create_aat_styleperiods_ruler(nlp, name="aat_styleperiods_ruler"):
    return create_vocabulary_ruler(
        nlp=nlp,
        name=name,
        min_lemmatize_length=4,
        min_term_length=3,
        lemmatize=True,
        pos=[],
        default_label="STYLEPERIOD",
        default_language="en",
        vocabulary=_get_vocabulary(VocabularyEnum.AAT_STYLEPERIODS)
    )


@Language.factory("fish_archobjects_ruler")
def create_fish_archobjects_ruler(nlp, name="fish_archobjects_ruler"):
    return create_vocabulary_ruler(
        nlp=nlp,
        name=name,
        min_lemmatize_length=4,
        min_term_length=3,
        lemmatize=True,
        pos=["NOUN"],
        default_label="OBJECT",
        default_language="en",
        vocabulary=_get_vocabulary(VocabularyEnum.FISH_ARCHOBJECTS)
    )


@Language.factory("fish_archsciences_ruler")
def create_fish_archsciences_ruler(nlp, name="fish_archsciences_ruler"):
    return create_vocabulary_ruler(
        nlp=nlp,
        name=name,
        min_lemmatize_length=4,
        min_term_length=3,
        lemmatize=True,
        pos=[],
        default_label="ARCHSCIENCE",
        default_language="en",
        vocabulary=_get_vocabulary(VocabularyEnum.FISH_ARCHSCIENCES)
    )


@Language.factory("fish_building_materials_ruler")
def create_fish_building_materials_ruler(nlp, name="fish_building_materials_ruler"):
    return create_vocabulary_ruler(
        nlp=nlp,
        name=name,
        min_lemmatize_length=4,
        min_term_length=3,
        lemmatize=True,
        pos=[],
        default_label="MATERIAL",
        default_language="en",
        vocabulary=_get_vocabulary(VocabularyEnum.FISH_BUILDING_MATERIALS)
    )


@Language.factory("fish_components_ruler")
def create_fish_components_ruler(nlp, name="fish_components_ruler"):
    return create_vocabulary_ruler(
        nlp=nlp,
        name=name,
        min_lemmatize_length=4,
        min_term_length=3,
        lemmatize=True,
        pos=["NOUN"],
        default_label="OBJECT",
        default_language="en",
        vocabulary=_get_vocabulary(VocabularyEnum.FISH_COMPONENTS)
    )


@Language.factory("fish_event_types_ruler")
def create_fish_event_types_ruler(nlp, name="fish_event_types_ruler"):
    return create_vocabulary_ruler(
        nlp=nlp,
        name=name,
        min_lemmatize_length=4,
        min_term_length=3,
        lemmatize=True,
        pos=[],
        default_label="EVENT",
        default_language="en",
        vocabulary=_get_vocabulary(VocabularyEnum.FISH_EVENT_TYPES)
    )


@Language.factory("fish_evidence_ruler")
def create_fish_evidence_ruler(nlp, name="fish_evidence_ruler"):
    return create_vocabulary_ruler(
        nlp=nlp,
        name=name,
        min_lemmatize_length=4,
        min_term_length=3,
        lemmatize=True,
        pos=[],
        default_label="EVIDENCE",
        default_language="en",
        vocabulary=_get_vocabulary(VocabularyEnum.FISH_EVIDENCE)
    )


@Language.factory("fish_maritime_craft_ruler")
def create_fish_maritime_craft_ruler(nlp, name="fish_maritime_craft_ruler"):
    return create_vocabulary_ruler(
        nlp=nlp,
        name=name,
        min_lemmatize_length=4,
        min_term_length=3,
        lemmatize=True,
        pos=["NOUN"],
        default_label="OBJECT",
        default_language="en",
        vocabulary=_get_vocabulary(VocabularyEnum.FISH_MARITIME_CRAFT)
    )


@Language.factory("fish_monument_types_ruler")
def create_fish_monument_types_ruler(nlp, name="fish_monument_types_ruler"):
    return create_vocabulary_ruler(
        nlp=nlp,
        name=name,
        min_lemmatize_length=4,
        min_term_length=3,
        lemmatize=True,
        pos=["NOUN"],
        default_label="OBJECT",
        default_language="en",
        vocabulary=_get_vocabulary(VocabularyEnum.FISH_MONUMENT_TYPES)
    )


@Language.factory("fish_periods_ruler")
def create_fish_periods_ruler(nlp, name="fish_periods_ruler"):
    return create_vocabulary_ruler(
        nlp=nlp,
        name=name,
        min_lemmatize_length=4,
        min_term_length=3,
        lemmatize=True,
        pos=[],
        default_label="NAMEDPERIOD",
        default_language="en",
        vocabulary=_get_vocabulary(VocabularyEnum.FISH_PERIODS)
    )

@Language.factory("vocabulary_ruler", default_config={
    "lemmatize": True,         # whether to lemmatize vocabulary terms
    "pos": [],                  # POS to include in pattern
    "min_term_length": 3,       # min term length to make a pattern for
    "min_lemmatize_length": 4,  # min term length to lemmatize
    "default_label": "UNKNOWN",  # label to tag identified terms
    "default_language": "en",   # language of term
    "vocabulary": []})               # vocabulary terms - expects [{"id": "123", "term": "xyz"}, {"id": "234", "term": "abc"}]
def create_vocabulary_ruler(nlp,
                            name: str,
                            lemmatize: bool,
                            pos,
                            min_term_length: int,
                            min_lemmatize_length: int,
                            default_label: str,
                            default_language: str,
                            vocabulary):

    return VocabularyRuler(nlp,
                           name=name,
                           lemmatize=lemmatize,
                           pos=pos,
                           min_term_length=min_term_length,
                           min_lemmatize_length=min_lemmatize_length,
                           default_label=default_label,
                           default_language=default_language,
                           vocabulary=vocabulary)


class VocabularyRuler(EntityRuler):

    def __init__(self,
                 nlp: Language,
                 name: str,
                 lemmatize: bool,
                 pos,
                 min_term_length: int,
                 min_lemmatize_length: int,
                 default_label: str,
                 default_language: str,
                 vocabulary) -> None:

        EntityRuler.__init__(
            self,
            nlp=nlp,
            name=name,
            phrase_matcher_attr="LOWER",
            validate=False,
            overwrite_ents=True,
            ent_id_sep="||"
        )

        # add terms from vocabulary as generated patterns
        # vocabulary: [{id, term}, {id, term}]
        # patterns: [{id, label, language, term, pattern}, {id, label, language, term, pattern}]
        patterns = []
        for item in vocabulary:
            # clean input values before using
            clean_id = item.get("id", "").strip()
            clean_label = item.get("label", default_label).strip()
            clean_language = item.get("language", default_language).strip()
            clean_term = item.get("term", "").strip()

            # don't use if term length < min_term_length
            if (len(clean_term) < min_term_length):
                continue

            # add cleaned values to new pattern object
            pattern = VocabularyRuler._term_to_pattern(
                nlp, clean_term, lemmatize, min_lemmatize_length, pos)

            patterns.append({
                "id": clean_id,
                "label": clean_label,
                "language": clean_language,
                "term": clean_term,
                "pattern":  pattern
            })
        # pprint(patterns)
        self.add_patterns(patterns)

    def __call__(self, doc: Doc) -> Doc:
        EntityRuler.__call__(self, doc)
        return doc

    # (optionally) lemmatize each word in phrase for better chance of free-text match
    # using SAME nlp pipeline for patterns and terms being compared,
    @staticmethod
    def _term_to_pattern(nlp, term="", lemmatize=False, min_lemmatize_length=4, pos=[]):
        # normalise whitespace and force lowercase
        # (whitespace could frustrate matching and
        # lemmatization won't work if capitalised)
        clean_term = ' '.join(term.strip().lower().split())
        doc = nlp(clean_term)
        # lem = ' '.join(tok.lemma_ for tok in doc)
        pattern = []
        phrase_length = len(doc)
        term_length = len(clean_term)

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

            # add any required pos tags if passed in
            # note POS only applied to LAST term if multi-word phrase
            # e.g. { "LEMMA": "board", "POS": { "IN": ["NOUN"] }}
            if (len(pos) > 0 and n == phrase_length):
                pat["POS"] = { "IN": pos }
            
            pattern.append(pat)

        # pat = [{"LEMMA": tok.lemma_} for tok in doc]
        # e.g. {"LEMMA": "tools", "POS": "NOUN"}
        return pattern


# test the VocabularyRuler class
if __name__ == "__main__":

    # sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    # from rematch2.components.spacypatterns import vocab_en_AAT_OBJECTS
    # from ..spacypatterns import vocab_en_AAT_OBJECTS

    test_text = '''Aside from three residual flints, none closely datable, the earliest remains comprised a small assemblage of Roman pottery and ceramic building material, also residual and most likely derived from a Roman farmstead found immediately to the north within the Phase II excavation area. A single sherd of Anglo-Saxon grass-tempered pottery was also residual. The earliest features, which accounted for the majority of the remains on site, relate to medieval agricultural activity focused within a large enclosure. There was little to suggest domestic occupation within the site: the pottery assemblage was modest and well abraded, whilst charred plant remains were sparse, and, as with some metallurgical residues, point to waste disposal rather than the locations of processing or consumption. A focus of occupation within the Rodley Manor site, on higher ground 160m to the north-west, seems likely, with the currently site having lain beyond this and providing agricultural facilities, most likely corrals and pens for livestock. Animal bone was absent, but the damp, low-lying ground would have been best suited to cattle. An assemblage of medieval coins recovered from the subsoil during a metal detector survey may represent a dispersed hoard.'''

    nlp = spacy.load("en_core_web_sm", disable=['ner'])
    nlp.add_pipe("aat_activities_ruler", last=True)

    doc = nlp(test_text)

    for ent in doc.ents:
        print(ent.ent_id_, ent.text, ent.label_)

    # for tok in doc:
        # print(tok.text, tok.pos_, tok.lemma_)