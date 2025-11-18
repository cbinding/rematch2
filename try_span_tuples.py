import json
import spacy, os
from spacy.lang.en import English 
import itertools
from rematch2 import PeriodoRuler, child_span_remover
from collections import defaultdict

BASE_DIRECTORY = "./data/oasis/journals_july_2024/text extraction - new/"
   
# for reading supplementary lists from JSON files
def read_json(file_name):
    data = []
    try:
        with open(file_name, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Problem reading \"{file_name}\": {e}")
    return data

def get_configured_pipeline():
    supp_list_obj = read_json("./supp_list_en_FISH_ARCHOBJECTS.json")
    supp_list_mon = read_json("./supp_list_en_FISH_MONUMENTS.json")
    supp_list_per = read_json("./supp_list_en_FISH_PERIODS.json")
    # existing vocabulary concepts we don't want to appear in the results (even if legitimate matches) 
    stop_list_obj = read_json("./stop_list_en_FISH_ARCHOBJECTS.json")
    stop_list_mon = read_json("./stop_list_en_FISH_MONUMENTS.json")


    nlp = spacy.load("en_core_web_sm", disable=["ner"])
    nlp.add_pipe("normalize_text", before = "tagger")
    nlp.add_pipe("periodo_ruler", last=True, config={"periodo_authority_id": "p0kh9ds", "supp_list": supp_list_per})
    nlp.add_pipe("fish_archobjects_ruler", last=True, config={"supp_list": supp_list_obj, "stop_list": stop_list_obj})
    nlp.add_pipe("fish_monument_types_ruler", last=True,config={"supp_list": supp_list_mon, "stop_list": stop_list_mon})
    nlp.add_pipe("fish_object_materials_ruler", last=True)
    nlp.add_pipe("fish_event_types_ruler", last=True)
    nlp.add_pipe("child_span_remover", last=True)
    return nlp


def get_span_groups_in_noun_chunks(nlp, input_text: str) -> list:
    doc = nlp(input_text)

    all_spans = doc.spans.get("rematch", [])
    #print("All identified spans:")
    #for span in all_spans:
        #print(span.start, span.label_, span.text)
    results = []
    for chunk in doc.noun_chunks:
        #print("Noun chunk:", chunk.text)

        # get any identified spans occurring within this noun chunk
        spans_in_chunk = list(filter(lambda span: span.start >= chunk.start and span.end <= chunk.end, all_spans))

        # grouping spans for this noun chunk by label into lists
        # { material: [gold, silver], object: [brooch], period: [early roman] }
        spans_by_label = defaultdict(list)
        for span in spans_in_chunk:
            spans_by_label[span.label_].append(span)

        # print groups
        #print("spans by label:")
        #spans_to_text = list(map(lambda s: s.text, spans_by_label))
        #for key, span_list in spans_by_label.items():
           # print(key, spans_to_text(span_list))
        #spans_to_serializable = lambda span_list: [span.text for span in span_list]
        #serializable = list(map(lambda x: spans_to_serializable(x), groups))
        #entry["spangroups"] = serializable   
        # build Cartesian product across the groups' lists
        # [ [gold, brooch, early roman], [silver, brooch, early roman] ]
        groups_lists = list(spans_by_label.values())
        combinations = itertools.product(*groups_lists)
        unique_lists = set(tuple(c) for c in combinations)
        span_groups = []
        for item in unique_lists: #itertools.product(*groups_lists):            
            #lst = list(item)
            if len(item) >=2: # only looking for pairs or more
                # need to serialize spans to JSON so just get the text (for now) 
                #spans_to_serializable = lambda spans: [span.text for span in spans]
                serializable = list(map(lambda s: s.text, item))
                # TODO - there are now duplicate pairs in the results - prevent it
                #result["groups"].append(serializable)
                span_groups.append(serializable)

        if len(span_groups) > 0:
            results.append({ "chunk_text": chunk.text, "span_groups": span_groups })        
    return results




# read input text files 
def get_input_data() -> list[dict]:
    print(f"Reading input text files from {BASE_DIRECTORY}")
    data = []    
     
    # subset of names of text files to read
    file_names = [
        "120_031_097_new.txt",
        "2022_96_001_012_cooper_garton_new.txt",
        "2022_96_013-068_huxley_new.txt",
        "archael547-005-040-breeze_new.txt",
        "archael547-079-116-ceolwulf_new.txt",
        "daj_v023_1901_040-047_new.txt",
        "daj_v086_1966_031-053_new.txt",
        "nas_20_1985_67-86_jackson_new.txt",
        "nas_20_1985_87-112_taylor_new.txt",
        "surreyac103_063-090_lambert_new.txt"
    ]

    # read each specified file and create a data item    
    index = 0
    for entry in os.scandir(BASE_DIRECTORY):        
        if entry.is_file() and entry.name.lower() in file_names:   
            index += 1
            #if index > 1: break   # tmp        
            data_item = { "metadata": { "filename": entry.name }, "text": "" }
            # read text contents of input file        
            with open(entry.path, "r") as input_file:
                input_file_text = input_file.read()
                data_item["text"] = input_file_text
            # add this item to the list for output
            data.append(data_item)

    # return the list of data items
    print("Read", len(data), "files")
    return data


# get the pipeline and input data
print("Configuring NLP pipeline...")
nlp = get_configured_pipeline()
print("done")
print("Reading input data...")
data = get_input_data()
    
for entry in data:
    print(f"Processing file: {entry['metadata']['filename']}")
    groups = get_span_groups_in_noun_chunks(nlp, entry["text"])
    #spans_to_serializable = lambda span_list: [span.text for span in span_list]
    #serializable = list(map(lambda x: spans_to_serializable(x), groups))
    #entry["spangroups"] = serializable   
    entry["spangroups"] = groups
    print("done")

# write out the JSON common format file
dataFileName = os.path.join(BASE_DIRECTORY, "try_span_tuples_output.json")
print(f"Writing results to {dataFileName}")

with open(dataFileName, "w") as outfile:  
    json.dump(data, outfile, indent=4)   

print(f"done")

# check any 3 or more span groups found within a noun chunk??
#for entry in data:
    #print(entry["metadata"]["filename"])
    #for group in list(filter(lambda x: len(x) >= 2, entry["spangroups"])):
        #print(group)