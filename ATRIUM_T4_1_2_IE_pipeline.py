# build configured pipeline for ATRIUM T-4-1-2
import argparse
from dataclasses import dataclass, asdict, field
from datetime import datetime as DT # for timestamps
import os
from typing import Any
import spacy, json 
import pandas as pd
from spacy.language import Language
from components.Util import load_pipeline_for_language, read_json_file

 
# takes an optional dict of config values to override defaults; 
# output is configured spacy pipeline with custom IE components
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
    # i.e. nlp.get_pipe("attribute_ruler").add_patterns(patterns_en_ATTRIBUTE_RULES)    
    # so inserting another one directly after it and adding the rules to that one    
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
            "patt_list": read_json_file("./vocabularies/patterns_en_FISH_73.json"),
            "supp_list": [], 
            "stop_list": []
        }
    ) 

    # remove child spans from matches to avoid nested entities 
    # (e.g. "BRONZE AGE" occurring within "LATE BRONZE AGE")
    # this is optional but helps with precision of results
    nlp.add_pipe("child_span_remover", last=True)
    
    # add ._.score attribute to spans for confidence scoring of matches
    nlp.add_pipe("span_scorer", last=True) 

    # return the configured pipeline
    return nlp


# test the pipeline configuration and output results to files
if __name__ == "__main__":
    import os

    # initiate the input arguments parser
    parser = argparse.ArgumentParser(
        prog=__file__, description="ATRIUM T4_1_2 information extraction pipeline")

    # add long and short argument descriptions
    parser.add_argument("--inputpath", "-i", required=False,
        help="Input directory containing files to be processed")
    
    # add long and short argument descriptions
    parser.add_argument("--outputpath", "-o", required=False,
        help="Output directory for processed data files")
    
    # add long and short argument descriptions
    parser.add_argument("--outputformat", "-f", required=False,
        help="Output format for processed data files")


    # parse command line arguments
    args = parser.parse_args()

    # timestamp for use in directory names
    timestamp = DT.now().strftime('%Y%m%d')   

    # clean required arguments
    if args.inputpath:
        input_directory = args.inputpath.strip()
    else:
        # temp harcoded test..
        input_directory = "./data/ads/journals_july_2024"
    if args.outputpath:
        output_directory = args.outputpath.strip()
    else:
        output_directory = os.path.join(input_directory, f"ie-output-{timestamp}")
    if args.outputformat:
        output_format = args.outputformat.strip()
    else:        
        output_format = "json" # default to JSON format for output files

    # create output file path if it does not already exist    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # creat a pre-configured information extraction pipeline
    print("Creating configured pipeline...")
    nlp = create_configured_pipeline() 
    print(f"Pipeline created with components: {nlp.pipe_names}")

    # process each eligible file in the input directory
    print(f"Processing files in input directory '{input_directory}'")
    for entry in os.scandir(input_directory):
        if not entry.is_file(): # or not entry.name.lower().endswith(".pdf"):  
            continue

        input_file_name = entry.name
        input_file_path = entry.path
        
        print(f"Processing file '{input_file_name}'...")
        #input_file_content = read_json_file(entry.path)        
        print(f"Done")

        # set up metadata to include in output
        metadata = {
            "identifier": entry.name,
            "title": "vocabulary-based IE results",
            "description": f"vocabulary-based information extraction results for file {entry.name}",
            "creator": "ATRIUM_T4_1_2_IE_pipeline.py",
            "pipeline": nlp.pipe_names,
            "input_file_name": entry.name,
            "input_record_count": 1
        }
