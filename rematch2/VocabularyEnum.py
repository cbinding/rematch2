"""
=============================================================================
Package   : rematch2
Module    : VocabularyEnum.py
Classes   : VocabularyEnum
Version   : 20231027
Project   : 
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : Enum for use with BaseRuler - 
                predefined (JSON) vocabulary resources
Imports   : Enum
Example   : 
    VocabularyEnum.AAT_ACTIVITIES.name  ["AAT_ACTIVITIES"]
    VocabularyEnum.AAT_ACTIVITIES.value ["vocab_en_AAT_ACTIVITIES_20231018.json"]
License   : https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History
27/10/2023 CFB Initially created script
=============================================================================
"""
from enum import Enum


class VocabularyEnum(Enum):
    AMCR = "vocab_cs_AMCR_20221208.json" # experimental
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

    '''
    @staticmethod
    def to_ruler(value: VocabularyEnum):
        ruler_name = ""
        match value:
            case VocabularyEnum.AAT_ACTIVITIES:
                ruler_name = "aat_activities_ruler"
        return ruler_name
    '''
