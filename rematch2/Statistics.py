"""
=============================================================================
Package   : rematch2
Module    : Statistics.py
Classes   : 
Project   : 
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : Calculating TF/IDF type stats for rematch2 results
Imports   : os, glob, json
Example   : 
License   : https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History
14/02/2025 CFB Initially created script
=============================================================================
"""
import os, glob, json, math
from pandas import DataFrame
from collections import Counter

def read_spans_from_file(file_name: str) -> list:
    data = {}

    with open(file_name, "r") as f:
        data = json.load(f)

    spans = data.get("spans", []) 

    return spans


def write_spans_to_file(file_name: str, spans: list):
    data = {}

    with open(file_name, "r") as f:
        data = json.load(f)

    data["spans"] = spans

    with open(file_name, "w") as f:
        json.dump(data, f)

    
def get_spans_cf_idf_for_file(file_name: str, idf_index: dict):
    spans = read_spans_from_file(file_name)
    
    for span in spans:
        id = span.get("id", "blank")
        cf_value = span.get("cf", 0)
        idf_item = idf_index.get(id, {})
        idf_value = idf_item.get("idf", 0)
        print(f"{id} {cf_value} {idf_value}")
        span["idf"] = float(idf_value)
        span["cf_idf"] = float(cf_value) * float(idf_value)

     # Write 'enriched' data back to json file
    write_spans_to_file(file_name, spans)



def get_file_names_for_path(path: str) -> list:
    # get list of all files/directories on the given path
    file_list = glob.glob(path, recursive=False)
    # filter down to names of files only (no directories)
    file_list = list(filter(lambda file_name: os.path.isfile(file_name), file_list))
    return file_list


def get_spans_cf_idf_for_path(path: str, idf_index: dict) -> None:
    file_list = get_file_names_for_path(path)
    for file_name in file_list:
        get_spans_cf_idf_for_file(file_name, idf_index)


def get_unique_span_ids(json_file_name: str) -> list:
    spans = read_spans_from_file(json_file_name)
    span_ids = list(set(filter(lambda id: id != "", map(lambda s: s.get("id",""), spans))))  
    return span_ids
   
        

# IDF for spans is calculated after we have NER results
# as we need to calculate stats across all result files
# IDF = log (doc_count / (docs_containing_given_span_id + 1))
def get_spans_idf_for_path(path: str) -> dict:
    file_list = get_file_names_for_path(path)

    count = len(file_list)
    index = dict()

    for file_name in file_list:
        span_ids = get_unique_span_ids(file_name)
        for id in span_ids:
            if index.get(id) == None:
                index[id] = {"idf": 0, "files": [file_name]}
            else:
                if not file_name in index[id]["files"]:
                    #uniques = set(index[id]["files"])
                    index[id]["files"].append(file_name) # todo check if exists first
    
    # now calculate idf values
    for item in index.values():
        frequency = len(item["files"])
        item["idf"] = math.log(count / (frequency + 1), 2)
        item["explain"] = f"count={count}, freq={frequency + 1}"
    
    # Serializing json
    #json_object = json.dumps(index, indent=4, default=list)
    
    # Writing to sample.json
    #with open("idf_values.json", "w") as outfile:
        #outfile.write(json_object)

    with open("idf_values.json", "w") as outfile:
        json.dump(index, outfile)

    return index


# aggregate ALL span results to single list, 
# to then be supplemented with cf/idf etc.
def aggregate_spans(path: str) -> list:  
    file_list = get_file_names_for_path(path)
    lst = []
    for file_name in file_list:
        spans = read_spans_from_file(file_name)
        basename = os.path.basename(file_name)
        # add source file name so file source 
        # can be identified once aggregated
        for span in spans:
            span["file_name"] = basename
        lst += spans

    return lst


# calculate concept frequency (cf) for each span
def calculate_cf_for_spans(spans: list) -> list:
    lst = spans.copy() # so we don't alter original

    # get unique source file names
    file_names = set(map(lambda x: x["file_name"], lst))

    for file_name in file_names:
        filtered = list(filter(lambda x: x["file_name"] == file_name, lst))
        ident_count = Counter(map(lambda x: x["id"], filtered))
        label_count = Counter(map(lambda x: x["label"], filtered))
        for span in filtered:
            id = span.get("id", "")
            lbl = span.get("label", "")
            id_count = ident_count.get(id, 0) 
            lbl_count = label_count.get(lbl, 1)
            span["cf"] = float(id_count) /  float(lbl_count)
            span["cf_explain"] = f"id_count={id_count}, lbl_count={lbl_count}"
            

    return lst

# calculate and add cf*idf to spans in list
def calculate_cf_idf_for_spans(spans: list) -> list:
    lst = spans.copy() # so we don't alter original
    for span in lst:
        cf = float(span.get("cf", 0))
        idf = float(span.get("idf", 0))
        span["cf_idf"] = cf * idf
    return lst


# calculate inverse document frequency (idf) for each span
def calculate_idf_for_spans(spans: list) -> list:
    lst = spans.copy() # so we don't alter original

    file_count = len(set(map(lambda x: x["file_name"], lst)))
    
    # create index to count unique files per span id
    index = dict()
    for span in list(filter(lambda x: x.get("id", "") != "", lst)):
        id = span.get("id")
        file_name = span.get("file_name", "NO_VALUE")
        if index.get(id) == None:
            index[id] = {"files": {file_name}}
        else:
            index[id]["files"].add(file_name)

    # now calculate idf values
    for item in index.values():
        frequency = len(item["files"])
        item["idf"] = math.log(file_count / (frequency + 1), 2)
        item["idf_explain"] = f"count={file_count}, frequency={frequency + 1}"

    # create new copy of spans so we don't alter the original
    # add idf values and return as a new list
    for span in filter(lambda x: x.get("id", "") != "", lst):
        id = span.get("id", "")
        span["idf"] = index[id]["idf"]
        span["idf_explain"] = index[id]["idf_explain"]

    return lst


# testing the script
if __name__ == "__main__":
    input_file_path = "../data/ner-output/ner-output-oasis-report-metadata-20250228/*.json"
    idf_index = get_spans_idf_for_path(input_file_path)
    get_spans_cf_idf_for_path(input_file_path, idf_index)

    # 07/03/2025 - aggregation / calculation and CSV output?
    spans = aggregate_spans(input_file_path)
    spans = calculate_cf_for_spans(spans)
    spans = calculate_idf_for_spans(spans)   
    spans = calculate_cf_idf_for_spans(spans)
    output_file_path = os.path.dirname(input_file_path)
    output_file_name = os.path.join(output_file_path, "all_spans.csv")
    df = DataFrame(spans).drop_duplicates()
    cols = ["file_name","id", "start", "end", "token_start", "token_end", "label","text", "cf","idf", "cf_idf", "cf_explain", "idf_explain"]
    df.to_csv(output_file_name, index=False, columns=cols)