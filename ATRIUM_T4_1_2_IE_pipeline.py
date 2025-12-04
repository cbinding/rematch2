# build configured pipeline for ATRIUM T-4-1-2
import spacy, json
from spacy.language import Language
from rematch2.spacypatterns import patterns_en_ATTRIBUTE_RULES # rules to override POS tags in some cases


# read data from JSON file (for supplementary lists and stopword lists)
def read_json(file_name):
    data = []
    try:
        with open(file_name, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Problem reading \"{file_name}\": {e}")
    return data


# get pre-configured information extraction pipeline
def get_pipeline(language: str="en") -> Language:

    clean_language = language.strip().lower()

    nlp: Language

    if(clean_language == "en"):
        # using predefined spaCy pipeline (English)
        nlp = spacy.load("en_core_web_sm", disable = ['ner'])

        # adding custom rules to override default POS tagging for specific cases
        # NOTE: adding rules to existing attribute_ruler component doesn't work
        # so insert another one directly after it and add the rules to that one    
        # nlp.get_pipe("attribute_ruler").add_patterns(patterns_en_ATTRIBUTE_RULES) # didn't work this way
        ar = nlp.add_pipe("attribute_ruler", name="custom_attribute_ruler", after="attribute_ruler")
        ar.add_patterns(patterns_en_ATTRIBUTE_RULES)

        # using "Historic England Archaeological and Cultural Periods" Perio.do authority
        periodo_authority_id = "p0kh9ds" 
        
        # reading supplementary and stopword lists from JSON files
        # supplementary concepts we want to appear in the results (or alternate terms for existing concepts)
        supp_list_obj = read_json("./supp_list_en_FISH_ARCHOBJECTS.json")
        supp_list_mon = read_json("./supp_list_en_FISH_MONUMENTS.json")
        supp_list_per = read_json("./supp_list_en_FISH_PERIODS.json")
        supp_list_mat = [] # object materials
        # existing vocabulary concepts we don't want to appear in the results (even if legitimate matches) 
        stop_list_obj = read_json("./stop_list_en_FISH_ARCHOBJECTS.json")
        stop_list_mon = read_json("./stop_list_en_FISH_MONUMENTS.json")
        stop_list_per = []
        stop_list_mat = [] # object materials

        
        # add rematch2 information extraction component(s) to the pipeline
        nlp.add_pipe("normalize_text", before = "tagger")
        nlp.add_pipe("yearspan_ruler", last=True)   
        nlp.add_pipe("periodo_ruler", last=True, config={"periodo_authority_id": periodo_authority_id, "supp_list": supp_list_per, "stop_list": stop_list_per}) 
        nlp.add_pipe("fish_archobjects_ruler", last=True, config={"supp_list": supp_list_obj, "stop_list": stop_list_obj}) 
        nlp.add_pipe("fish_monument_types_ruler", last=True, config={"supp_list": supp_list_mon, "stop_list": stop_list_mon})   
        nlp.add_pipe("fish_object_materials_ruler", last=True, config={"supp_list": supp_list_mat, "stop_list": stop_list_mat})   
        nlp.add_pipe("child_span_remover", last=True)
    else:
        raise ValueError(f"Unsupported language code \"{language}\"")
    
    return nlp



