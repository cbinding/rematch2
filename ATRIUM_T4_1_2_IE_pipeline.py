# build configured pipeline for ATRIUM T-4-1-2
#from dataclasses import dataclass, asdict, field
from os import name
from typing import Any
from spacy.language import Language
from decorators import run_once
from components.Util import load_pipeline_for_language, read_json_file
 
# takes an optional dict of config values to override defaults; 
# output is configured spacy pipeline with custom IE components
@run_once
def create_configured_pipeline(config: dict[str, Any]={}) -> Language:
    # default config values
    defaults: dict = { "language": "en" }

    # merge passed values overriding defaults; 
    # create config object from merged values
    cfg: dict = { **defaults, **config }

    # create pre-configured information extraction pipeline, then
    # add custom information extraction component(s) to the pipeline
    nlp: Language = load_pipeline_for_language(cfg["language"])
   
    # text normalisation to improve pattern matching 
    nlp.add_pipe("text_normalizer", first=True)
    
    # adding custom rules to override default POS tagging for specific cases
    # NOTE: adding rules to existing attribute_ruler component doesn't work:
    # (i.e. nlp.get_pipe("attribute_ruler").add_patterns(patterns_en_ATTRIBUTE_RULES))    
    # so - inserting another one directly after it, and adding the rules to that one    
    component = nlp.add_pipe("attribute_ruler", name="custom_attribute_ruler", after="attribute_ruler")
    patterns = read_json_file("./vocabularies/patterns_FISH_MONUMENT_ATTRIBUTE_RULES.json")
    component.add_patterns(patterns)  # type: ignore

    # year spans (e.g. "1450 - 1530 AD") 
    nlp.add_pipe("yearspan_ruler", last=True)

    # named periods (from specified authority of Perio.do dataset)
    nlp.add_pipe(
        "periodo_ruler", 
        name = "periodo_ruler",
        last = True, 
        config = {
            "default_label": "PERIOD",
            "periodo_authority_id": "p0kh9ds", # Historic England periods authority ID in Periodo dataset
            "supp_list": read_json_file("./vocabularies/supp_list_FISH_PERIODS.json"), 
            "stop_list": []
        }
    ) 

    # object types from FISH object types vocabulary 
    nlp.add_pipe(
        "vocabulary_ruler", 
        name = "object_types_ruler",
        last = True, 
        config = {
            "default_label": "FISH_OBJECT",
            "token_pos": ["NOUN"],
            "lemmatize": True,
            "min_lemm_length": 3,
            "min_term_length": 3,
            "patt_list": read_json_file("./vocabularies/patterns_FISH_mda_obj_20260513.json"),
            "supp_list": read_json_file("./vocabularies/supp_list_FISH_ARCHOBJECTS.json"), 
            "stop_list": read_json_file("./vocabularies/stop_list_FISH_ARCHOBJECTS.json")
        }
    ) 

    # monument types from FISH monument types vocabulary
    nlp.add_pipe(
        "vocabulary_ruler", 
        name = "monument_types_ruler",
        last = True, 
        config ={
            "default_label": "FISH_MONUMENT",
            "token_pos": ["NOUN"],
            "lemmatize": True,
            "min_lemm_length": 3,
            "min_term_length": 3,
            "patt_list": read_json_file("./vocabularies/patterns_FISH_eh_tmt2_20260513.json"),
            "supp_list": read_json_file("./vocabularies/supp_list_FISH_MONUMENTS.json"), 
            "stop_list": read_json_file("./vocabularies/stop_list_FISH_MONUMENTS.json")
        }
    ) 

    # object materials from FISH object materials vocabulary
    nlp.add_pipe(
        "vocabulary_ruler", 
        name = "object_materials_ruler",
        last = True, 
        config = {
            "default_label": "FISH_MATERIAL",
            "token_pos": ["ADJ"],
            "lemmatize": True,
            "min_lemm_length": 3,
            "min_term_length": 3,
            "patt_list": read_json_file("./vocabularies/patterns_FISH_73_20260513.json"),
            "supp_list": [], 
            "stop_list": []
        }
    ) 

    # remove child spans from matches to avoid nested entities 
    # (e.g. "BRONZE AGE" occurring within "LATE BRONZE AGE")
    # this is optional but helps with precision of results
    nlp.add_pipe("child_span_remover", last=True)
    
    # add ._.score attribute to spans for confidence scoring of matches
    nlp.add_pipe(
        "span_scorer", 
        last=True, 
        config = {
            "sig_proximity": 3,
            "sig_score": 1.0,
            "sec_scores": {   
                "title": 40.0,      # score for spans occurring in the title section of a document
                "abstract": 2.0,    # score for spans occurring in the abstract section of a document
                "body": 0.1,        # score for spans occurring in the body section of a document
                "end_matter": 0.0   # score for spans occurring in the end matter section of a document               
            },
            "sections": []          # override for each doc e.g. [{"section": "title", "start": 0, "end": 12}]
        }
    ) 

    # return the configured pipeline
    return nlp


