"""
=============================================================================
Package   : 
Module    : find_pairs.py
Classes   : 
Project   : 
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : experimentation - identifying 'paired' entities
            e.g. "medieval furrow", "iron age barrow", "Roman villa" etc.
Imports   : pandas, spacy, lxml, json
Example   : 
License   : https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History
31/09/2023 CFB Initially created script
27/02/2024 CFB verbose results to JSON file, readable results to TXT file
               LogFile class moved to separate script
=============================================================================
"""
import json
import itertools  # for product
import pandas as pd
import spacy
from pathlib import Path
from spacy.tokens import Doc
from spacy.matcher import DependencyMatcher
from test_examples_english import test_examples_english
from test_examples_oasis import test_examples_oasis
from collections.abc import MutableSequence
from rematch2.PeriodoRuler import create_periodo_ruler
from rematch2.VocabularyRuler import *
from lxml import etree as ET
from datetime import datetime as DT
from Util import *
from decorators import run_timed


def get_pipeline(periodo_authority_id: str = ""):
    # use predefined spaCy pipeline, disable default NER component
    nlp = spacy.load("en_core_web_sm", disable=['ner'])

    # add rematch2 component(s) to the end of the pipeline
    nlp.add_pipe("periodo_ruler", last=True, config={
        "periodo_authority_id": periodo_authority_id})
    nlp.add_pipe("fish_archobjects_ruler", last=True)
    nlp.add_pipe("fish_monument_types_ruler", last=True)
    return nlp


# parse and extract list of records from source XML file 
# [{"id", "text"}, {"id", "text"}, ...] for subsequent processing
def get_records_from_xml_file(file_path: str="")-> list:
    records = []
    try:
        # read XML file
        tree = ET.parse(file_path)
        root = tree.getroot()
    except:
        print(f"Could not read from {sourceFilePath}")
        return records

    # find rows to be processed in the XML file
    rows = tree.xpath("/table/rows/row")

    for row in rows:
        # find abstract(s) in the current item
        abstracts = row.xpath("value[@columnNumber='1']/text()")
       
        # if multiple abstracts, get first one
        if (len(abstracts) > 0):
            abstract = abstracts[0]
        else:
            abstract = ""

         # find identifier(s) in the current item
        identifiers = row.xpath("value[@columnNumber='0']/text()")

        # if multiple identifiers, get first one (remove URL prefix if present)
        if (len(identifiers) > 0):
            identifier = identifiers[0]
            identifier = identifier.replace(
                "https://archaeologydataservice.ac.uk/archsearch/record?titleId=", "")
        else:
            identifier = ""

        ## create new (cleaned) record and add it
        record = {}
        record["id"] = identifier.strip()
        record["text"] = abstract.strip()
        records.append(record)

    # finally, return the extracted list
    return records

    
def find_period_object_pairs(nlp=None, input_text: str = "") -> dict:
    
    # set up overall single result structure to be returned
    result = {
        "input_text": input_text,
        "tokens": [],
        "entities": [],
        "noun_chunk_pairs": [],
        "dependency_match_pairs": []
    }

    # normalise white space before annotation
    # (extra spaces frustrate pattern matching)
    cleaned = normalize_whitespace(input_text)

    # perform the annotation
    doc = nlp(cleaned)
    
    # add tokens to result
    result["tokens"] = [{
        "from": tok.i,
        "to": tok.i + len(tok.text),
        "text": tok.text,
        "pos": tok.pos_,
        "lemma": tok.lemma_
    } for tok in doc]

    # add entities to result
    result["entities"] = [{
        "from": ent.start_char,
        "to": ent.end_char - 1,
        "id": ent.ent_id_,
        "text": ent.text,
        "lemma": ent.lemma_,
        "type": ent.label_
    } for ent in doc.ents]

    # add noun_chunk pairs to result
    noun_chunk_pairs = get_noun_chunk_pairs(doc)

    result["noun_chunk_pairs"] = [{
        #"label": f"[{ent1.label_} - {ent2.label_}] [{ent1.ent_id_}] '{ent1}' - '{ent2}' [{ent2.ent_id_}]",
        "ent1": {  
            "from": ent1.start_char,
            "to": ent1.end_char - 1,
            "id": ent1.ent_id_ ,
            "text": ent1.text,
            "type": ent1.label_
        },
        "ent2": {  
            "from": ent2.start_char,
            "to": ent2.end_char - 1,
            "id": ent2.ent_id_ ,
            "text": ent2.text,
            "type": ent2.label_
        }
    } for ent1, ent2 in noun_chunk_pairs]

    # add dependency match pairs to result
    # semgrex symbols for dependency relationship between terms
    # see https://spacy.io/usage/rule-based-matching#dependencymatcher-operators
    for rel_op in [
        "<",    # A is the immediate dependent of B
        ">",    # A is the immediate head of B
        "<<",   # A is the dependent in a chain to B following dep → head paths
        ">>",   # A is the head in a chain to B following head → dep paths
        ".",    # A immediately precedes B, i.e. A.i == B.i - 1, and both are within the same dependency tree
        ".*",   # A precedes B, i.e. A.i < B.i, and both are within the same dependency tree
        ";",    # A immediately follows B, i.e. A.i == B.i + 1, and both are within the same dependency tree
        ";*",   # A follows B, i.e. A.i > B.i, and both are within the same dependency tree
        "$+",   # B is a right immediate sibling of A, i.e. A and B have the same parent and A.i == B.i - 1
        "$-",   # B is a left immediate sibling of A, i.e. A and B have the same parent and A.i == B.i + 1
        "$++",  # B is a right sibling of A, i.e. A and B have the same parent and A.i < B.i
        "$--",  # B is a left sibling of A, i.e. A and B have the same parent and A.i > B.i
        ">+",   # B is a right immediate child of A, i.e. A is a parent of B and A.i == B.i - 1
        ">-",   # B is a left immediate child of A, i.e. A is a parent of B and A.i == B.i + 1
        ">++",  # B is a right child of A, i.e. A is a parent of B and A.i < B.i
        ">--",  # B is a left child of A, i.e. A is a parent of B and A.i > B.i
        "<+",   # B is a right immediate parent of A, i.e. A is a child of B and A.i == B.i - 1
        "<-",   # B is a left immediate parent of A, i.e. A is a child of B and A.i == B.i + 1
        "<++",  # B is a right parent of A, i.e. A is a child of B and A.i < B.i
        "<--"   # B is a left parent of A, i.e. A is a child of B and A.i > B.i
    ]:
        dependency_match_pairs = get_dependency_match_pairs(doc, rel_op)
        for ent1, ent2 in dependency_match_pairs:
            result["dependency_match_pairs"].append({
                #"label": f"[{ent1.label_} {rel_op} {ent2.label_}] [{ent1.ent_id_}] '{ent1}' - '{ent2}' [{ent2.ent_id_}]",
                #"label": f"{ent1.ent_id_} [{ent1.label_}] '{ent1}' {op} '{ent2}' [{ent2.label_}] {ent2.ent_id_}",
                "rel_op": rel_op,
                "ent1": {  
                    "from": ent1.start_char,
                    "to": ent1.end_char - 1,
                    "id": ent1.ent_id_ ,
                    "text": ent1.text,
                    "type": ent1.label_
                },
                "ent2": {  
                    "from": ent2.start_char,
                    "to": ent2.end_char - 1,
                    "id": ent2.ent_id_ ,
                    "text": ent2.text,
                    "type": ent2.label_
                }
            })
    return result
   

# using dependency matcher..
# https://spacy.io/usage/rule-based-matching#dependencymatcher
# look for PERIOD - OBJECT dependency pairs, return as tuple array [[ent, ent], [ent, ent]]
def get_dependency_match_pairs(doc: Doc, rel_op: str = ".") -> MutableSequence:
    pattern = [
        {
            "RIGHT_ID": "period",
            "RIGHT_ATTRS": {"ENT_TYPE": "PERIOD"}
        },
        {
            "LEFT_ID": "period",
            "REL_OP": rel_op,
            "RIGHT_ID": "object",
            "RIGHT_ATTRS": {"ENT_TYPE": "OBJECT"}
        }
    ]
    matcher = DependencyMatcher(doc.vocab)
    matcher.add("PERIOD_OBJECT", [pattern])
    matches = matcher(doc)

    matched = dict()
    for match_id, token_ids in matches:
        # get all PERIOD entities token_ids match
        periods = filter(lambda ent: ent.label_ == "PERIOD" and any(
            ent.start <= id and ent.end > id for id in token_ids), doc.ents)
        # get all OBJECT entities token_ids match
        objects = filter(lambda ent: ent.label_ == "OBJECT" and any(
            ent.start <= id and ent.end > id for id in token_ids), doc.ents)
        # using cartesian product to give all PERIOD - OBJECT pair combinations
        for ent1, ent2 in itertools.product(periods, objects):
            # using dict to eliminate duplicates
            matched[f"{ent1.ent_id_}|{ent2.ent_id_}"] = tuple([ent1, ent2])
    # return as array of tuple
    return matched.values()


# look for PERIOD - OBJECT pairs in noun chunks,
# return as tuple array [[ent, ent], [ent, ent]]
def get_noun_chunk_pairs(doc: Doc) -> MutableSequence:
   
    matched = dict()
    for chunk in doc.noun_chunks:
        # get all PERIOD entities in the noun chunk
        periods = filter(lambda ent: ent.label_ == "PERIOD", chunk.ents)
        # get all OBJECT entities in the noun chunk
        objects = filter(lambda ent: ent.label_ == "OBJECT", chunk.ents)
        # Use cartesian product to give all PERIOD - OBJECT pairs
        for ent1, ent2 in itertools.product(periods, objects):
            # using dict to eliminate duplicate pairs
            matched[f"{ent1.ent_id_}|{ent2.ent_id_}"] = tuple([ent1, ent2])           
     # return as array of tuple
    return matched.values()


def results_to_json_file(file_name: str="", results: dict={}):
    # construct suitable file name if not passed in
    if len(file_name) == 0:
        timestamp = DT.now().strftime(("%Y%m%dT%H%M%S"))
        file_name = f"{Path(__file__).stem}_results_{timestamp}.json"

    with open(file_name, "w") as json_file:     
        json.dump(results, json_file)


def results_to_text_file(file_name: str="", results: dict={}):
    # construct suitable file name if not passed in
    if len(file_name) == 0:
        timestamp = DT.now().strftime(("%Y%m%dT%H%M%S"))
        file_name = f"{Path(__file__).stem}_results_{timestamp}.txt"

    with open(file_name, "w") as text_file:
        
        # write metadata header
        metadata = results.get("metadata", {})
        text_file.write(f"title:         {metadata.get('title', '')}\n")
        text_file.write(f"description:   {metadata.get('description', '')}\n")
        text_file.write(f"timestamp:     {metadata.get('timestamp', '')}\n")
        text_file.write(f"periodo ID:    \"{metadata.get('periodo_authority_id', '')}\"\n")
        text_file.write(f"input records: {metadata.get('input_record_count', '')}\n")
        text_file.write("results:\n")

        for r in results.get("results", []):            
            
            # write record header
            identifier = r.get("identifier", "")
            input_text = r.get("input_text", "")            
            text_file.write("\n=============================================================\n")
            text_file.write(f"identifier: {identifier}\n")
            text_file.write(f"input text:\n\"{input_text}\"\n")
            
            # summarise identified entities (by desc count)             
            text_file.write("\nEntity occurrence counts:\n")
            # load entities into a DataFrame object:
            entities = r.get("entities", [])
            pd.set_option('display.max_rows', None)
            df = pd.DataFrame([{
                "from": e.get("from", ""),
                "to": e.get("to", ""),
                "id": e.get("id", ""),
                "text": e.get('text', ''),
                "lemma": f"\"{e.get('lemma', '').lower()}\"",
                "type": f"[{e.get('type', '')}]"
            } for e in entities])   
            # write structured table to output file         
            text_file.write(df.groupby(["id", "type", "lemma"]).size().sort_values(ascending=False).to_string())

            # write noun chunk pairs as fixed width string values
            text_file.write("\n\nNoun chunk pairs:\n")
            noun_chunk_pairs = r.get("noun_chunk_pairs", [])
            if len(noun_chunk_pairs) == 0:
                text_file.write("NONE FOUND\n")
            else:
                for pair in noun_chunk_pairs:
                    text_file.write("{id_1:<40} [{type_1:<}] {text_1:>20} {sep:^5} {text_2:<20} [{type_2:>}] {id_2:<40}\n".format(
                        type_1 = pair['ent1']['type'],
                        type_2 = pair['ent2']['type'],
                        id_1 = pair['ent1']['id'],
                        id_2 = pair['ent2']['id'],                  
                        text_1 = f"\"{pair['ent1']['text']}\"",                        
                        text_2 = f"\"{pair['ent2']['text']}\"",
                        sep = "-"                       
                    ))

            # write dependency match pairs as fixed width string values
            text_file.write("\nDependency match pairs:\n")
            dependency_match_pairs = r.get("dependency_match_pairs", [])
            if len(dependency_match_pairs) == 0:
                text_file.write("NONE FOUND\n")
            else:
                for pair in dependency_match_pairs:
                    text_file.write("{id_1:<40} [{type_1:<}] {text_1:>20} {sep:^5} {text_2:<20} [{type_2:>}] {id_2:<40}\n".format(
                        type_1 = pair['ent1']['type'],
                        type_2 = pair['ent2']['type'],
                        id_1 = pair['ent1']['id'],
                        id_2 = pair['ent2']['id'],                  
                        text_1 = f"\"{pair['ent1']['text']}\"",                        
                        text_2 = f"\"{pair['ent2']['text']}\"",
                        sep = pair["rel_op"]
                    ))
      

# run using record list of [{"id", "text"}, {"id", "text"}, ...]
@run_timed
def main(records: list=[], periodo_authority_id: str="p0kh9ds") -> dict:
    input_record_count = len(records)        
    
    # print number of records found 
    print(f"processing {input_record_count} records")
    
    # set up configured pipeline once only (faster than per record)
    nlp = get_pipeline(periodo_authority_id=periodo_authority_id)    

     # create structured results (inc diagnostic information)
    results = {
        "metadata": {
            "title": "find_pairs.py results",
            "description": "find paired entities in text",
            "timestamp": DT.now().strftime("%d/%m/%y %H:%M:%S"),
            "periodo_authority_id": periodo_authority_id,
            "input_record_count": input_record_count        
        },
        "results": []
    }

     # process each record
    current_record = 0
    for record in records:        
        current_record += 1
        # process this record
        identifier = record.get("id", "")
        input_text = record.get("text", "")
        print(f"processing record {current_record} of {input_record_count} [ID: {identifier}]")
        
        result = find_period_object_pairs(
            nlp=nlp, 
            input_text=input_text.lower()
        )
        
        if result is None:
            result = {}

        result["identifier"] = identifier
        result["input_text"] = input_text

        results["results"].append(result)

    return results
       

if __name__ == '__main__':

    # override - set to False for local testing of small example textss
    from_xml = False

    if(from_xml):
        # get list of records to be processed [{"id", "text"},{"id", "text"}]
        # (XML file is OASIS example data received from Tim @ ADS)      
        records = get_records_from_xml_file("./oasis_descr_examples.xml")
    else:
        # example records for testing
        records = test_examples_oasis    
    
    results = main(records=records, periodo_authority_id="p0kh9ds")
    timestamp = DT.now().strftime(("%Y%m%dT%H%M%S"))
    filename = f"{Path(__file__).stem}_results_{timestamp}"
    print("writing results to file...")
    results_to_json_file(file_name=f"{filename}.json", results=results)
    results_to_text_file(file_name=f"{filename}.txt", results=results)
    print("done")
