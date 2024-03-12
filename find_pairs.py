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
08/03/2024 CFB EntityPair and EntityPairs classes split out to separate files
=============================================================================
"""
import json
import spacy
from lxml import etree as ET
from datetime import datetime as DT
from html import escape
from pathlib import Path
from spacy import displacy
#from spacy.tokens import Doc, Span, Token
#from spacy.tokens import Span
#from rematch2 import create_periodo_ruler
from rematch2 import EntityPair, EntityPairs, PeriodoRuler, VocabularyRuler, NegationRuler
#from rematch2.PeriodoRuler import *
#from rematch2.VocabularyRuler import *
#from rematch2.NegationRuler import *
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


# won't work atm as results not JSON serializable
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
            text_file.write(f"{identifier}\n")
            text_file.write(f"\"{input_text}\"\n")
            
            # write entity counts (by desc count)             
            text_file.write("\nEntity Counts:\n")            
            counts = r.get('entity_counts')
            for item in counts:                    
                text_file.write("[{type}] {id:<60} {text:>20} ({count})\n".format(
                    type = item["type"],
                    id = item["id"],
                    text = item["text"],
                    count = item["count"]
                    )
                )
            
            # write entity pairs as fixed width string values
            text_file.write("\n\nEntity Pairs:\n")
            pairs = r.get("entity_pairs", [])
            if len(pairs) == 0:
                text_file.write("NONE FOUND\n")
            else:
                for pair in pairs:
                    text_file.write(f"{str(pair)}\n")
                

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
                html_file.write(f"<h3><a href='{identifier}'>{identifier}</a></h3>")
            else:
                html_file.write(f"<h3>{identifier}</h3>")
            
            html_file.write(f"<p>{r.get('displacy_ents')}</p>")
            
            # write entity counts summary
            html_file.write("<h3>Entity Counts:</h3>") 
            entity_counts = r.get('entity_counts') 
            if len(entity_counts) == 0:
                html_file.write("<p>NONE FOUND</p>")
            else:
                html_file.write("<table>")
                for item in entity_counts:
                    html_file.write("<tr>")                    
                    html_file.write("<td style='text-align:right; vertical-align: middle;'>")
                    html_file.write(f"<div class=\"entity {item['type'].lower()}\">")
                    if(item['id'].startswith("http")):
                        html_file.write(f"<a href=\"{item['id']}\">{escape(item['text'])}</a>")
                    else:
                        html_file.write(f"{escape(item['text'])}")
                    html_file.write(f"</div>")
                    html_file.write(f"<td>({item['count']})</td>")
                    html_file.write(f"</tr>")
                html_file.write("</table>")  

            # write entity pairs
            html_file.write("<h3>Entity Pairs:</h3>")
            entity_pairs = r.get("entity_pairs", [])
            if len(entity_pairs) == 0:
                html_file.write("<p>NONE FOUND</p>")
            else:
                html_file.write("<table>")
                for pair in entity_pairs:
                    html_file.write("<tr>")
                    #html_file.write(f"<td><small>({pair['ent1']['from']}&#8594;{pair['ent1']['to']})</small></td>")                    
                    #html_file.write(f"<td><small>[{pair['ent1']['type']}]</small></td>")   
                    html_file.write(f"<td style='text-align:right; vertical-align: middle;'>")
                    html_file.write(f"<div class=\"entity {pair.ent1.label_.lower()}\">")
                    if(pair.ent1.ent_id_.startswith("http")):
                        html_file.write(f"<a href=\"{pair.ent1.ent_id_}\">{escape(pair.ent1.text)}</a>")
                    else:
                        html_file.write(f"{escape(pair.ent1.text)}")
                    html_file.write(f"</div>")
                    html_file.write(f"</td>")                    
                    html_file.write(f"<td style='text-align:left; vertical-align: middle'>")
                    html_file.write(f"<div class=\"entity {pair.ent2.label_.lower()}\">")
                    if(pair.ent2.ent_id_.startswith("http")):
                        html_file.write(f"<a href=\"{pair.ent2.ent_id_}\">{escape(pair.ent2.text)}</a>")
                    else:
                        html_file.write(f"{escape(pair.ent2.text)}")
                    html_file.write(f"</div>")
                    html_file.write(f"</td>")
                    html_file.write(f"<td>({pair.score})</td>")                    
                    #html_file.write(f"<td><small>[{pair['ent2']['type']}]</small></td>") 
                    #html_file.write(f"<td><small>({pair['ent2']['from']}&#8594;{pair['ent2']['to']})</small></td>")                                                         
                    html_file.write("</tr>")
                html_file.write("</table>")

            #html_file.write("<h3>Entity Pairs as DF table:</h3>")
            #html_file.write(r.get("entity_pairs_table"))
            
        # write footer tags       
        html_file.write('</body>')
        html_file.write('</html>')

def flag_negated_entities(doc):
    # use predefined spaCy pipeline (English)
    nlp = get_pipeline_for_language("en")
    nlp.add_pipe("negation_ruler", last=True)

    

# run using input record list [{"id", "text"}, {"id", "text"}, ...]
@run_timed
def main(records: list=[], periodo_authority_id: str="p0kh9ds") -> dict:
    input_record_count = len(records)        
    
    # print number of input records 
    print(f"processing {input_record_count} records")
    
    # use predefined spaCy pipeline (English)
    nlp = get_pipeline_for_language("en")
    
    # add rematch2 component(s) to the end of the pipeline
    nlp.add_pipe("yearspan_ruler", last=True)    
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
        
        # set up result structure to be returned
        result = {
            "identifier": identifier,
            "doc": {},
            "displacy_ents": [],
            "entity_counts": [],        
            "entity_pairs": []
        }

        # normalise white space prior to annotation
        # (extra spaces frustrate pattern matching)
        cleaned = normalize_whitespace(input_text)

        # perform the annotation
        doc = nlp(cleaned)
        result["doc"] = doc.to_json()

        # write HTML formatted doc text with entities tagged
        options = { 
            "ents": None, # to display all
            "colors": { 
                "NEGATION": "lightgray",
                "PERIOD": "yellow", 
                "YEARSPAN": "moccasin", 
                "OBJECT": "plum" 
            } 
        }
        result["displacy_ents"] = displacy.render(doc, style="ent", minify=True, options=options)           
        
        # add entity counts to results
        result["entity_counts"] = get_entity_counts_by_id(doc)

        # using semgrex symbols for dependency relationships between terms
        # see https://spacy.io/usage/rule-based-matching#dependencymatcher-operators
        rel_ops = [ "<", ">", "<<", ">>", ".*", ";", ";*" ]   
        result["entity_pairs"] = EntityPairs(doc=doc, rel_ops=rel_ops, left_types=["PERIOD", "YEARSPAN"], right_types=["OBJECT"]).pairs     
        #result["entity_pairs"] = EntityPairs(doc=doc, rel_ops=rel_ops, left_type="NEGATION", right_type="OBJECT").pairs
        #result["entity_pairs_table"] = EntityPairs(doc=doc, rel_ops=rel_ops, left_type="PERIOD", right_type="OBJECT").to_html_table()
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
    #results_to_json_file(file_name=f"{ results_file_name }.json", results=test_results)
    results_to_text_file(file_name=f"{ results_file_name }.txt", results=test_results)
    results_to_html_file(file_name=f"{ results_file_name }.html", results=test_results)
    
    print(f"{__file__} done")
