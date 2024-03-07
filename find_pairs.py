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
import json
from html import escape
from pathlib import Path
from spacy import displacy
from spacy.tokens import Doc, Span
#from spacy.tokens import Span
from spacy.matcher import DependencyMatcher
from collections.abc import MutableSequence
from rematch2 import create_periodo_ruler
from rematch2.VocabularyRuler import *
from rematch2.NegationRuler import *
from lxml import etree as ET
from datetime import datetime as DT
from Util import *
from decorators import run_timed

# parse and extract list of records from source XML file 
# returns [{"id", "text"}, {"id", "text"}, ...] for subsequent processing
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

    
# scoring used to rank pairs results
def get_score_for_rel_op(rel_op: str="") -> float:
    score = float(0)

    match (rel_op or "").strip().lower():
        case "-": score = 1.0
        case "<": score = 0.8
        case ">": score = 0.8
        case "<<": score = 0.6
        case ">>": score = 0.6
        case ".*": score = 0.2
        case ";*": score = 0.2
        case _: score = 0.0
    return score


# to consistently represent a token in results
def results_token(tok):    
    return {
        "from": tok.i,
        "to": tok.i + len(tok.text),
        "text": tok.text,
        "pos": tok.pos_,
        "lemma": tok.lemma_
    }


# to consistently represent an entity in results
def results_entity(ent: Span):
    return {
        "from": ent.start_char,
        "to": ent.end_char - 1,
        "id": ent.ent_id_ ,
        "text": ent.text,
        "lemma": ent.lemma_,
        "type": ent.label_
    }


# to consistently represent an entity pair in results
def results_pair(ent1: Span, ent2: Span, rel_op: str=""):
    return {
        "rel_op": rel_op,
        "score": get_score_for_rel_op(rel_op),
        "ent1": results_entity(ent1),
        "ent2": results_entity(ent2)
    }


# not used yet, make HTML display easier
# by breaking down into smaller functions?
def ent_for_html_display(ent: Span) -> str:
    html = f"<div class=\"entity {ecape(ent.label_.lower())}\">"
    if ent.ent_id_:
        html += f"<a href=\"{ent.ent_id_}\">{escape(ent.text)}</a>"
    else:
        html += escape(ent.text)
    html +=f"</div>"
    return html


# custom along the lines of displacy but locally controllable
# TODO: not finished or used yet...
def custom_html_rendering(doc: Doc):
    
    def render_in_tag(tag_name: str, content: str):
        return f"<{escape(tag_name)}>{escape(content)}></{escape(tag_name)}>"

    def tok_for_render(tok):
        return {
            "index": tok.idx,
            "text": tok.text_with_ws,
            "label": None
        }

    def ent_for_render(ent):
        return {
            "index": ent.start,
            "text": ent.text,
            "label": ent.label_
        }

    toks_outside_entities = list(filter(lambda t: t.ent_iob_ not in ['B', 'I'], doc)) 
    toks_for_render = list(map(tok_for_render, toks_outside_entities))
    ents_for_render = list(map(ent_for_render, doc.ents))
    items_for_render = sorted(toks_for_render + ents_for_render, key=lambda x: x.get("index", 0))

    html = "<div>"
    for item in items_for_render:
        if item["label"] is not None:
            html += f"<mark class='entity {escape(item['label'].lower())}'>{escape(item['text'])}</mark>"
        else:
            html += item["text"] 
    html += "</div>"
    return html



def find_period_object_pairs(nlp=None, input_text: str = "") -> dict:
    
    # set up overall single result structure to be returned
    result = {
        #"input_text": input_text,
        #"tokens": [],
        #"entities": [],
        "doc": {},
        "displacy_ents": [],
        "counts": [],        
        "pairs": []
    }

    # normalise white space before annotation
    # (extra spaces frustrate pattern matching)
    cleaned = normalize_whitespace(input_text)

    # perform the annotation
    doc = nlp(cleaned)
    result["doc"] = doc.to_json()

    # write text with entities tagged
    options = { "ents": None, "colors": { "NEGATION": "lightgray","PERIOD": "yellow", "OBJECT": "plum" } }
    result["displacy_ents"] = displacy.render(doc, style="ent", minify=True, options=options)           

    # add tokens to result
    #result["tokens"] = list(map(results_token, doc))

    # add entities to result
    #result["entities"] = list(map(results_entity, doc.ents)) #[entity_for_results(ent) for ent in doc.ents]

    # add entity counts to results
    result["counts"] = get_entity_counts(doc)

    #print(custom_html_rendering(doc))

    # add dependency match pairs to results
    # semgrex symbols for dependency relationship between terms
    # see https://spacy.io/usage/rule-based-matching#dependencymatcher-operators
    rel_ops = [
        "<",    # A is the immediate dependent of B
        ">",    # A is the immediate head of B
        "<<",   # A is the dependent in a chain to B following dep → head paths
        ">>",   # A is the head in a chain to B following head → dep paths
        #".",    # A immediately precedes B, i.e. A.i == B.i - 1, and both are within the same dependency tree
        ".*",   # A precedes B, i.e. A.i < B.i, and both are within the same dependency tree
        ";",    # A immediately follows B, i.e. A.i == B.i + 1, and both are within the same dependency tree
        ";*",   # A follows B, i.e. A.i > B.i, and both are within the same dependency tree
        #"$+",   # B is a right immediate sibling of A, i.e. A and B have the same parent and A.i == B.i - 1
        #"$-",   # B is a left immediate sibling of A, i.e. A and B have the same parent and A.i == B.i + 1
        #"$++",  # B is a right sibling of A, i.e. A and B have the same parent and A.i < B.i
        #"$--",  # B is a left sibling of A, i.e. A and B have the same parent and A.i > B.i
        #">+",   # B is a right immediate child of A, i.e. A is a parent of B and A.i == B.i - 1
        #">-",   # B is a left immediate child of A, i.e. A is a parent of B and A.i == B.i + 1
        #">++",  # B is a right child of A, i.e. A is a parent of B and A.i < B.i
        #">--",  # B is a left child of A, i.e. A is a parent of B and A.i > B.i
        #"<+",   # B is a right immediate parent of A, i.e. A is a child of B and A.i == B.i - 1
        #"<-",   # B is a left immediate parent of A, i.e. A is a child of B and A.i == B.i + 1
        #"<++",  # B is a right parent of A, i.e. A is a child of B and A.i < B.i
        #"<--"   # B is a left parent of A, i.e. A is a child of B and A.i > B.i
    ]    
    dependency_pairs = get_dependency_pairs(doc, rel_ops)
    noun_chunk_pairs = get_noun_chunk_pairs(doc)

    # eliminate any duplicate pairs with lower scores
    best_scoring_pairs = {}
    for item in noun_chunk_pairs + dependency_pairs:
        id = f"{item['ent1']['id']}|{item['ent2']['id']}"            
        if (id not in best_scoring_pairs or item['score'] > best_scoring_pairs[id]['score']):
            best_scoring_pairs[id] = item
    best_pairs = list(best_scoring_pairs.values())

    # finally, sort best_scoring_pairs by ascending score and add to overall results
    result["pairs"] = sorted(best_pairs, key=lambda x: x.get("score", 0), reverse=True)
    return result
   

# Using dependency matcher. Find PERIOD - OBJECT dependency pairs
# https://spacy.io/usage/rule-based-matching#dependencymatcher
# returns list of pair result
def get_dependency_pairs(doc: Doc, rel_ops: list=[]) -> list:
    results = []
    for rel_op in rel_ops:
        results += get_dependency_pairs_by_rel_op(doc, rel_op)
    return results
# Find PERIOD - OBJECT dependency pairs for a single rel_op
def get_dependency_pairs_by_rel_op(doc: Doc, rel_op: str = ".") -> list:
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
            id = f"{ent1.ent_id_}|{ent2.ent_id_}"
            matched[id] = results_pair(ent1, ent2, rel_op)
            
    # return list of result items
    return list(matched.values())


# look for PERIOD - OBJECT pairs within noun chunks,
# returns list of pair result
def get_noun_chunk_pairs(doc: Doc) -> list:
   
    matched = dict()
    for chunk in doc.noun_chunks:
        # get all PERIOD entities in the noun chunk
        periods = filter(lambda ent: ent.label_ == "PERIOD", chunk.ents)
        # get all OBJECT entities in the noun chunk
        objects = filter(lambda ent: ent.label_ == "OBJECT", chunk.ents)
        # Use cartesian product to give all PERIOD - OBJECT pairs
        for ent1, ent2 in itertools.product(periods, objects):
            # using dict to eliminate duplicates with lower scores
            id = f"{ent1.ent_id_}|{ent2.ent_id_}"
            matched[id] = results_pair(ent1, ent2, "-")

     # return as array of tuple
    return list(matched.values())


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
        text_file.write(f"title:                {metadata.get('title', '')}\n")
        text_file.write(f"description:          {metadata.get('description', '')}\n")
        text_file.write(f"started:              {metadata.get('timestamp', '')}\n")
        text_file.write(f"periodo authority ID: \"{metadata.get('periodo_authority_id', '')}\"\n")
        text_file.write(f"input records count:  {metadata.get('input_record_count', '')}\n")
        
        # write results
        text_file.write("results:\n")
        for r in results.get("results", []):            
            
            # write result header
            identifier = r.get("identifier", "")
            input_text = r["doc"]["text"]         
            text_file.write("\n=============================================================\n")
            text_file.write(f"identifier: {identifier}\n")
            text_file.write(f"input text:\n\"{input_text}\"\n")
            
            # summarise identified entities (by desc count)             
            text_file.write("\nCounts:\n")
            #doc = Doc.from_json(doc_json=r.get("doc"))

            counts = get_entity_counts(doc)
            for item in counts:                    
                    text_file.write("[{type}] {id:<40} {text:>20} {count}\n".format(
                        type = item["type"],
                        id = item["id"],
                        text = item["text"],
                        count = item["count"]))



            # first load entities into a DataFrame object:
            
            '''ents = doc.ents
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
            # write as structured table to output file         
            text_file.write(df.groupby(["id", "type", "lemma"]).size().sort_values(ascending=False).to_string())'''

            # write noun chunk pairs as fixed width string values
            text_file.write("\n\nPairs:\n")
            pairs = r.get("pairs", [])
            if len(pairs) == 0:
                text_file.write("NONE FOUND\n")
            else:
                for pair in pairs:
                    text_file.write("{score} {id_1:<40} [{type_1:<}] {text_1:>20} - {text_2:<20} [{type_2:>}] {id_2:<40}\n".format(
                        score = pair.get('score',float(0)),
                        type_1 = pair['ent1']['type'],
                        type_2 = pair['ent2']['type'],
                        id_1 = pair['ent1']['id'],
                        id_2 = pair['ent2']['id'],                  
                        text_1 = f"\"{pair['ent1']['text']}\"",                        
                        text_2 = f"\"{pair['ent2']['text']}\""    
                    ))
            

# count entities by id, return list [{id, type, text, count}, {id, type, text, count}, ...] 
# returned in descending count order - note there is probably a more elegant way to do this    
def get_entity_counts(doc: Doc) -> list:
    counts = {}

    for ent in doc.ents:
        # don't include NEGATION in summary counts?
        if ent.label_ == "NEGATION":
            continue

        # get suitable identifier to aggregate counts
        id=""
        if ent.ent_id_:
            id = ent.ent_id_
        elif ent.lemma_:
            id = ent.lemma_
        elif ent.text:
            id = ent.text
        else:
            id = "other"
        
        # create a new record if not encountered before, or increment the count
        if id not in counts:
            counts[id] = { "id": id, "type": ent.label_, "text": ent.lemma_, "count": 1 } 
        else:
            counts[id]["count"] += 1            
    
    # return as list sorted by ascending count
    return sorted(list(counts.values()), key=lambda x: x.get("count", 0), reverse=True)


# TODO: create custom version of displacy rendering
def results_to_html_file(file_name: str="", results: dict={}):
    # construct suitable output file name if not passed in
    if len(file_name) == 0:
        timestamp = DT.now().strftime(("%Y%m%dT%H%M%S"))
        file_name = f"{Path(__file__).stem}_results_{timestamp}.html"

    # open (or create) the output file
    with open(file_name, "w") as html_file:
        # write header tags
        html_file.write('<!DOCTYPE html>')
        html_file.write('<html>')
        html_file.write('<head>')

        # write CSS from file to style tag (so no file dependency)
        with open('find_pairs.css', 'r', encoding='utf8') as css_file:
            css_text = css_file.read()
            html_file.write(f'<style>{css_text}</style>')
                
        html_file.write('</head>')
        html_file.write('<body>')
        
        # write metadata header
        metadata = results.get("metadata", {})
        html_file.write(f"<div><strong>title:</strong> {escape(metadata.get('title', ''))}</div>")
        html_file.write(f"<div><strong>description:</strong> {escape(metadata.get('description', ''))}</div>")
        html_file.write(f"<div><strong>started:</strong> {escape(metadata.get('timestamp', ''))}</div>")
        html_file.write(f"<div><strong>periodo authority ID:</strong> \"{escape(metadata.get('periodo_authority_id', ''))}\"</div>")
        html_file.write(f"<div><strong>input records count:</strong> {metadata.get('input_record_count', '')}</div>")

        # write results
        html_file.write("<h2>results:</h2>")
        for r in results.get("results", []):  

            # write result header
            identifier = escape(r.get("identifier", ""))                 
            html_file.write("<hr>")
            if(identifier.startswith("http")):
                html_file.write(f"<div><strong>ID:</strong> <a href='{identifier}'>{identifier}</a></div>")
            else:
                html_file.write(f"<div><strong>ID:</strong> {identifier}</div>")
            
            html_file.write(f"<p>{r.get('displacy_ents')}</p>")
            
            # write entity counts summary
            html_file.write("<h3>Counts:</h3>") 
            counts = r.get('counts') 
            if len(counts) == 0:
                html_file.write("<p>NONE FOUND</p>")
            else:
                html_file.write("<table>")
                for item in counts:
                    html_file.write("<tr>")                    
                    html_file.write("<td style='text-align:right; vertical-align: middle;'>")
                    html_file.write(f"<div class=\"entity {item['type'].lower()}\">")
                    html_file.write(f"<a href=\"{item['id']}\">{escape(item['text'])}</a>")
                    html_file.write(f"</div>")
                    html_file.write(f"<td>({item['count']})</td>")
                    html_file.write(f"</tr>")
                html_file.write("</table>")  

            # write noun chunk pairs
            html_file.write("<h3>Pairs:</h3>")
            pairs = r.get("pairs", [])
            if len(pairs) == 0:
                html_file.write("<p>NONE FOUND</p>")
            else:
                html_file.write("<table>")
                for pair in pairs:
                    html_file.write("<tr>")
                    #html_file.write(f"<td><small>({pair['ent1']['from']}&#8594;{pair['ent1']['to']})</small></td>")                    
                    #html_file.write(f"<td><small>[{pair['ent1']['type']}]</small></td>")   
                    html_file.write(f"<td style='text-align:right; vertical-align: middle;'>")
                    html_file.write(f"<div class=\"entity {pair['ent1']['type'].lower()}\">")
                    html_file.write(f"<a href=\"{pair['ent1']['id']}\">{escape(pair['ent1']['text'])}</a>")
                    html_file.write(f"</div>")
                    html_file.write(f"</td>")                    
                    html_file.write(f"<td style='text-align:left; vertical-align: middle'>")
                    html_file.write(f"<div class=\"entity {pair['ent2']['type'].lower()}\">")
                    html_file.write(f"<a href=\"{pair['ent2']['id']}\">{escape(pair['ent2']['text'])}</a>")
                    html_file.write(f"</div>")
                    html_file.write(f"</td>")
                    html_file.write(f"<td>({pair['score']})</td>")
                    
                    #html_file.write(f"<td><small>[{pair['ent2']['type']}]</small></td>") 
                    #html_file.write(f"<td><small>({pair['ent2']['from']}&#8594;{pair['ent2']['to']})</small></td>")                                                         
                    html_file.write("</tr>")
                html_file.write("</table>")
            
        # write footer tags       
        html_file.write('</body>')
        html_file.write('</html>')


# run using input record list [{"id", "text"}, {"id", "text"}, ...]
@run_timed
def main(records: list=[], periodo_authority_id: str="p0kh9ds") -> dict:
    input_record_count = len(records)        
    
    # print number of input records 
    print(f"processing {input_record_count} records")
    
    # use predefined spaCy pipeline (English)
    nlp = get_pipeline_for_language("en")
    
    # add rematch2 component(s) to the end of the pipeline
    nlp.add_pipe("periodo_ruler", last=True, config={
        "periodo_authority_id": periodo_authority_id})
    #nlp.add_pipe("aat_objects_ruler", last=True)
    nlp.add_pipe("negation_ruler", last=True)
    nlp.add_pipe("fish_archobjects_ruler", last=True)
    nlp.add_pipe("fish_monument_types_ruler", last=True)  

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
            input_text=input_text
        )
        
        if result is None:
            result = {}

        result["identifier"] = identifier       
        results["results"].append(result)

    return results
       

if __name__ == '__main__':
    test_records = []

    # override - set to False for local testing of small example texts
    from_xml = False
    
    print(f"{__file__} loading test records...")
    if(from_xml):
        # get list of test records to be processed [{"id", "text"},{"id", "text"}]
        # (XML file is OASIS example data received from Tim @ ADS)      
        test_records = get_records_from_xml_file("./oasis_descr_examples.xml")
    else:
        # load some local tests..
        test_file_path = (Path(__file__).parent / "test_examples_english.json").resolve() 
        with open(test_file_path, "r") as f:
            test_records = json.load(f)            
    
    # run using test records
    print(f"{__file__} running against test records...")
    test_results = main(records=test_records, periodo_authority_id="p0kh9ds")
    
    print(f"{__file__} writing results to files...")
    results_file_name = f"{ Path(__file__).stem }_results_{ DT.now().strftime('%Y%m%dT%H%M%S') }"    
    results_to_json_file(file_name=f"{ results_file_name }.json", results=test_results)
    #results_to_text_file(file_name=f"{ results_file_name }.txt", results=test_results)
    results_to_html_file(file_name=f"{ results_file_name }.html", results=test_results)
    
    print(f"{__file__} done")
