"""
=============================================================================
Package   : rematch2
Module    : VocabularyEnum.py
Classes   : VocabularyEnum
Version   : 20260513
Project   : ATRIUM
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : Enum for use with BaseRuler - predefined (JSON) vocabulary resources
Imports   : Enum
Example   : 
    VocabularyEnum.AAT_ACTIVITIES.name  ["AAT_ACTIVITIES"]
    VocabularyEnum.AAT_ACTIVITIES.value ["patterns_AAT_ACTIVITIES_20231018.json"]
License   : https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History
27/10/2023 CFB Initially created script
13/05/2025 CFB Updated to reflect recent changes in vocabulary file naming
=============================================================================
"""
from enum import Enum

class VocabularyEnum(Enum):
    AAT_ACTIVITIES = "patterns_AAT_ACTIVITIES_20231018.json"
    AAT_AGENTS = "patterns_AAT_AGENTS_20231018.json"
    AAT_ASSOCIATED_CONCEPTS = "patterns_AAT_ASSOCIATED_CONCEPTS_20231018.json"
    AAT_MATERIALS = "patterns_AAT_MATERIALS_20231018.json"
    AAT_OBJECTS = "patterns_AAT_OBJECTS_20231018.json"
    AAT_PHYSICAL_ATTRIBUTES = "patterns_AAT_PHYSICAL_ATTRIBUTES_20231018.json"
    AAT_STYLEPERIODS = "patterns_AAT_STYLEPERIODS_20231018.json"
    AMCR = "patterns_AMCR_20221208.json" # experimental    
    FISH_ARCHOBJECTS = "patterns_FISH_mda_obj_20260513.json"
    FISH_ARCHSCIENCES = "patterns_FISH_560_20260513.json"
    FISH_BUILDING_MATERIALS = "patterns_FISH_eh_tbm_20260513.json"
    FISH_COMPONENTS = "patterns_FISH_eh_com_20260513.json"
    FISH_EVENT_TYPES = "patterns_FISH_agl_et_20260513.json"
    FISH_EVIDENCE = "patterns_FISH_eh_evd_20260513.json"
    FISH_MARITIME_CRAFT = "patterns_FISH_eh_tmc_20260513.json"
    FISH_MONUMENT_TYPES = "patterns_FISH_en_tmt2_20260513.json"
        