# build configured pipeline for use by ATRIUM T4_1_2_IE.py
#from dataclasses import dataclass, asdict, field
from os import name, path
from typing import Any
from spacy.language import Language
from decorators import run_once
from components.Util import load_pipeline_for_language, read_json_file
 
default_config: dict = { 
    "language": "en",
    "span_scorer": {
        "sig_proximity": 3,     # token window size - proximity for 'significance' terms
        "sig_score": 1.0,       # score for spans within proximity to 'significance' indicator terms
        "sec_scores": {         # score for spans according to location within document sections
            "title": 40.0,      # score for spans occurring within the title section of a document
            "abstract": 2.0,    # score for spans occurring within the abstract section of a document
            "body": 0.1,        # score for spans occurring within the body section of a document
            "end_matter": 0.0   # score for spans occurring within the end matter section of a document               
        },
        "sections": []          # overridden for each doc e.g. [{"section": "title", "start": 0, "end": 12}]
    } 
}

# takes an optional dict of config values to override defaults; 
# output is configured spacy pipeline with custom IE components
# pipeline is cached so that subsequent calls with same config return the same pipeline instance
# the current configured pipeline is: 
# text_normalizer               - normalizes whitespace, puctuation and spelling to improve pattern matching 
# attribute_ruler               - adds custom rules to override default POS tagging for specific cases
# yearspan_ruler                - identifies year spans (e.g. "1450 - 1530 AD") 
# periodo_ruler                 - identifies named periods (e.g. "Medieval") from the Perio.do dataset
# vocabulary_ruler (multiple)   - identifies object types, monument types and object materials from FISH vocabularies
# child_span_remover            - removes child spans from matches to avoid nested entities (e.g. "BRONZE AGE" occurring within "LATE BRONZE AGE")
# span_scorer                   - scores identified spans based on their likelihood of being relevant
@run_once
def create_configured_pipeline(config: dict[str, Any]={}) -> Language:
    
    # default vocabulary patterns defined here
    # these may be overriden by local files 
    vocab_folder = path.join(path.dirname(__file__),"vocabularies")

    # merge passed values overriding defaults; 
    # create config object from merged values
    cfg: dict = { **default_config, **config }

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
    patterns = read_json_file(f"{vocab_folder}/patterns_FISH_MONUMENT_ATTRIBUTE_RULES.json")
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
            "supp_list": read_json_file(f"{vocab_folder}/supp_list_FISH_PERIODS.json"), 
            "stop_list": []
        }
    ) 

    # object types (from FISH object types vocabulary)
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
            "patt_list": read_json_file(f"{vocab_folder}/patterns_FISH_mda_obj_20260513.json"),
            "supp_list": read_json_file(f"{vocab_folder}/supp_list_FISH_ARCHOBJECTS.json"), 
            "stop_list": read_json_file(f"{vocab_folder}/stop_list_FISH_ARCHOBJECTS.json")
        }
    ) 

    # monument types (from FISH monument types vocabulary)
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
            "patt_list": read_json_file(f"{vocab_folder}/patterns_FISH_eh_tmt2_20260513.json"),
            "supp_list": read_json_file(f"{vocab_folder}/supp_list_FISH_MONUMENTS.json"), 
            "stop_list": read_json_file(f"{vocab_folder}/stop_list_FISH_MONUMENTS.json")
        }
    ) 

    # object materials (from FISH object materials vocabulary)
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
            "patt_list": read_json_file(f"{vocab_folder}/patterns_FISH_73_20260513.json"),
            "supp_list": [], 
            "stop_list": []
        }
    ) 

    # removes child spans from matches to avoid nested entities 
    # (e.g. "BRONZE AGE" occurring within "LATE BRONZE AGE")
    # this is optional, but improves accuracy of results
    nlp.add_pipe("child_span_remover", last=True)
    
    # adds ._.score attribute to spans for confidence scoring of identified entities

    nlp.add_pipe(
        "span_scorer", 
        last=True, 
        config = {
            "sig_proximity": cfg["span_scorer"]["sig_proximity"],           # token window size - proximity for 'significance' terms
            "sig_score": cfg["span_scorer"]["sig_score"],                   # score for spans within proximity to 'significance' indicator terms
            "sec_scores": {                                                 # score for spans according to location within document sections
                "title": cfg["span_scorer"]["sec_scores"]["title"],         # score for spans occurring within the title section of a document
                "abstract": cfg["span_scorer"]["sec_scores"]["abstract"],   # score for spans occurring within the abstract section of a document
                "body": cfg["span_scorer"]["sec_scores"]["body"],           # score for spans occurring within the body section of a document
                "end_matter": cfg["span_scorer"]["sec_scores"]["end_matter"]   # score for spans occurring within the end matter section of a document               
            },
            "sections": cfg["span_scorer"]["sections"]                      # overridden for each doc e.g. [{"section": "title", "start": 0, "end": 12}]
        }
    ) 

    # return the configured pipeline
    return nlp
