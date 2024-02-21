"""
=============================================================================
Package :   rematch2
Module  :   BaseRulers.py
Version :   20231025
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy custom pipeline component (specialized BaseRuler)
Imports :   os, sys, spacy, EntityRuler, Doc, Language
Example :   nlp.add_pipe("aat_objects_ruler", last=True)           
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
History :   25/10/2023 CFB Initially created script
=============================================================================
"""
# from . import PatternRuler
import os
import sys
import spacy            # NLP library
import json
from enum import Enum
from pathlib import Path
import pandas as pd

# Language-specific pipelines
from spacy.language import Language

if __package__ is None or __package__ == '':
    # uses current directory visibility
    from BaseRuler import create_base-ruler
else:
    # uses current package visibility
    from .BaseRuler import create_base-ruler


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

def _patterns_from_json_file(file_name: str) -> list:
        base_path = (Path(__file__).parent / "vocabularies").resolve()
        file_path = os.path.join(base_path, file_name)
        patterns = []
        with open(file_path, "r") as f:
            patterns = json.load(f)

        return patterns


@Language.factory("aat_activities_ruler")
def create_aatactivities_ruler(nlp, name="aat_activities_ruler"):
    return create_base-ruler(
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
    return create_base-ruler(
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
    return create_base-ruler(
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
    return create_base-ruler(
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
    return create_base-ruler(
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
    return create_base-ruler(
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
    return create_base-ruler(
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
    return create_base-ruler(
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
    return create_base-ruler(
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
    return create_base-ruler(
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
    return create_base-ruler(
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
    return create_base-ruler(
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
    return create_base-ruler(
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
    return create_base-ruler(
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
    return create_base-ruler(
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
    return create_base-ruler(
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


# test the component
if __name__ == "__main__":

    test_text = '''Aside from three residual flints, none closely datable, the earliest remains comprised a small assemblage of Roman pottery and ceramic building material, also residual and most likely derived from a Roman farmstead found immediately to the north within the Phase II excavation area. A single sherd of Anglo-Saxon grass-tempered pottery was also residual. The earliest features, which accounted for the majority of the remains on site, relate to medieval agricultural activity focused within a large enclosure. There was little to suggest domestic occupation within the site: the pottery assemblage was modest and well abraded, whilst charred plant remains were sparse, and, as with some metallurgical residues, point to waste disposal rather than the locations of processing or consumption. A focus of occupation within the Rodley Manor site, on higher ground 160m to the north-west, seems likely, with the currently site having lain beyond this and providing agricultural facilities, most likely corrals and pens for livestock. Animal bone was absent, but the damp, low-lying ground would have been best suited to cattle. An assemblage of medieval coins recovered from the subsoil during a metal detector survey may represent a dispersed hoard.'''

    nlp = spacy.load("en_core_web_sm", disable=['ner'])
    nlp.add_pipe("aat_activities_ruler", last=True)
    #nlp.add_pipe("aat_agents_ruler", last=True)
    #nlp.add_pipe("aat_associated_concepts_ruler", last=True)
    #nlp.add_pipe("aat_materials_ruler", last=True)
    #nlp.add_pipe("aat_objects_ruler", last=True)
    #nlp.add_pipe("aat_physical_attributes_ruler", last=True)
    #nlp.add_pipe("aat_styleperiods_ruler", last=True)
    #nlp.add_pipe("fish_archobjects_ruler", last=True)
    #nlp.add_pipe("fish_archsciences_ruler", last=True)
    #nlp.add_pipe("fish_building_materials_ruler", last=True)
    #nlp.add_pipe("fish_components_ruler", last=True)
    #nlp.add_pipe("fish_event_types_ruler", last=True)
    #nlp.add_pipe("fish_evidence_ruler", last=True)
    #nlp.add_pipe("fish_maritime_craft_ruler", last=True)
    #nlp.add_pipe("fish_monument_types_ruler", last=True)
    #nlp.add_pipe("fish_periods_ruler", last=True)
    doc = nlp(test_text)

    #for ent in doc.ents:
        #print(ent.start_char, ent.end_char - 1, ent.ent_id_, ent.text, ent.label_)

    results = [{
        "from": ent.start_char, 
        "to": ent.end_char - 1, 
        "id": ent.ent_id_, 
        "text": ent.text, 
        "type": ent.label_
        } for ent in doc.ents]
    # load data into a DataFrame object:
    df = pd.DataFrame(results)
    print(df)
