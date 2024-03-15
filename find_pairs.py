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
from spacy.tokens import Doc #, Span, Token
from rematch2 import EntityPair, EntityPairs, PeriodoRuler, VocabularyRuler, NegationRuler, DocSummary
from Util import *
from decorators import run_timed # form local run timing


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


def results_to_json_file(file_name: str="", results: dict={}):
    # construct suitable file name if not passed in
    if len(file_name) == 0:
        timestamp = DT.now().strftime(("%Y%m%dT%H%M%S"))
        file_name = f"{Path(__file__).stem}_results_{timestamp}.json"

    def result_to_json(result):
        id = result.get("identifier", "")
        doc = result.get("doc", None)        
        return { 
            "identifier": id, 
            "doc": doc.to_json() 
        }

    with open(file_name, "w") as json_file:  
        json_file.write(json.dumps({
            "metadata": results["metadata"], 
            "results": list(map(result_to_json , results["results"]))
        }))


def results_to_text_file(file_name: str="", results: dict={}):    
    lines = []   
    # write metadata header
    metadata = results.get("metadata", {})
    lines.append(f"title:                {metadata.get('title', '')}")
    lines.append(f"description:          {metadata.get('description', '')}")
    lines.append(f"started:              {metadata.get('timestamp', '')}")
    lines.append(f"periodo authority ID: {metadata.get('periodo_authority_id', '')}")

    # write results
    lines.append("results:")
    for result in results.get("results", []):            
            
        # write result header
        identifier = result.get("identifier", "")
        doc = result.get("doc")
        input_text = doc.text 

        lines.append("\n=============================================================")
        lines.append(f"{identifier}")
        lines.append(f"\"{input_text}\"")
            
        # write entity counts (by desc count)             
        lines.append("\nEntity Counts:")  
        entity_counts = DocSummary(doc).entcounts(format="text")  
        lines.append(entity_counts)           
        '''
        entity_counts = get_entity_counts_by_id(doc)
        for item in entity_counts:                    
            lines.append("[{type}] {id:<60} {text:>20} ({count})".format(
                type = item["type"],
                id = item["id"],
                text = item["text"],
                count = item["count"]
                )
            )
        '''
            
        # write entity pairs as fixed width string values
        lines.append("\nEntity Pairs:")
        entity_pairs = DocSummary(doc).entpairs(
            format="text",
            rel_ops=[ "<", ">", "<<", ">>", ".", ";" ], 
            left_types=["PERIOD", "YEARSPAN"], 
            right_types=["OBJECT"]
        )
        lines.append(entity_pairs)
        '''
        entity_pairs = EntityPairs(
            doc=doc, 
            rel_ops=[ "<", ">", "<<", ">>", ".", ";" ], 
            left_types=["PERIOD", "YEARSPAN"], 
            right_types=["OBJECT"]
        ).pairs
        if len(entity_pairs) == 0:
            lines.append("NONE FOUND")
        else:
            for pair in entity_pairs:
                lines.append(f"{str(pair)}")
        '''
        # write negated entities
        lines.append("\nNegated Entities:")
        negated_ents = list(filter(lambda ent: ent._.is_negated == True, doc.ents))
        if len(negated_ents) == 0:
            lines.append("NONE FOUND")
        else:
            for ent in negated_ents:
                lines.append("({start}->{end}) [{type}] {id:<60} {text}".format(
                    start = ent.start,
                    end = ent.end,
                    type = ent.label_,
                    id = ent.ent_id_,
                    text = ent.text
                ))

    # construct suitable file name if not passed in
    if len(file_name) == 0:
        timestamp = DT.now().strftime(("%Y%m%dT%H%M%S"))
        file_name = f"{Path(__file__).stem}_results_{timestamp}.txt"

    with open(file_name, "w") as text_file:
        text_file.write("\n".join(lines))


def results_to_html_file(file_name: str="", results: dict={}):
    html = []

    # write header tags
    html.append("<!DOCTYPE html>")
    html.append("<html>")
        
    # write CSS from file to style tag (so no file dependency)
    html.append("<head>")
    with open('find_pairs.css', 'r', encoding='utf8') as css_file:
        css_text = css_file.read()
        html.append(f'<style>{css_text}</style>')    
    
    html.append("</head>")
    html.append("<body>")

     # write metadata header
    metadata = results.get("metadata", {})
    html.append("<h3>Metadata:</h3>")
    html.append("<ul>")
    html.append(f"<li><strong>title:</strong> {metadata.get('title', '')}</li>")
    html.append(f"<li><strong>description:</strong> {metadata.get('description', '')}</li>")
    html.append(f"<li><strong>started:</strong>              {metadata.get('timestamp', '')}</li>")
    html.append(f"<li><strong>periodo authority ID:</strong> {metadata.get('periodo_authority_id', '')}</li>")
    html.append(f"<li><strong>input records count:</strong>  {metadata.get('input_record_count', '')}</li>")
    html.append("</ul>")

    # write results in body tag
    html.append("<h3>results:</h3>")
    for result in results.get("results", []):  
        identifier = result.get("identifier", "")
        doc = result.get("doc", None)           
        html.append(result_to_html_string(identifier, doc))

    # write footer tags
    html.append("</body>")
    html.append("</html>")
    
    # construct suitable output file name if not passed in
    if len(file_name) == 0:
        timestamp = DT.now().strftime(("%Y%m%dT%H%M%S"))
        file_name = f"{Path(__file__).stem}_results_{timestamp}.html"

    # open (or create) and write to the output file
    with open(file_name, "w") as html_file:
        html_file.write( "".join(html))


# write single results as a HTML string for presentation output
def result_to_html_string(identifier: str = "", doc: Doc = None) -> str:

    html = []
    # start with horizontal line break
    html.append("<hr>") 
    
    # write identifier as heading
    html.append("<h4>")
    if(identifier.startswith("http")):
        html.append(f"<a href='{identifier}'>{identifier}</a>")
    else:
        html.append(f"{escape(identifier)}")
    html.append("</h4>")

    # write displacy HTML rendering of doc text as paragraph with highlighted entities 
    '''
    options = { 
        "ents": None, # to display all
        "colors": { 
            "NEGATION": "lightgray",
            "PERIOD": "yellow", 
            "YEARSPAN": "moccasin", 
            "OBJECT": "plum" 
        } 
    }        
    html.append("<p>{rendered}</p>".format(
        rendered = displacy.render(doc, style="ent", minify=True, options=options) 
    ))
    '''
    doctext = DocSummary(doc).doctext(format="html")
    html.append(f"<p>{doctext}</p>")

    # write entity counts
    html.append("<h3>Entity Counts:</h3>")
    html.append(DocSummary(doc).entcounts(format="htmlc"))
    '''
    entity_counts = get_entity_counts_by_id(doc)
    if len(entity_counts) == 0:
        html.append("<p>NONE FOUND</p>")
    else:
        html.append("<table><tbody>")
        for item in entity_counts:
            html.append("<tr>")
            html.append("<td style='text-align:right; vertical-align: middle;'>")
            html.append(f"<div class='entity {escape(item['type'].lower())}'>")
            if(item['id'].startswith("http")):
                html.append(f"<a href='{item['id']}'>{escape(item['text'])}</a>")
            else:
                html.append(f"{escape(item['text'])}")
            html.append("</div>")
            html.append("</td>")
            html.append(f"<td>({item['count']})</td>")
            html.append("</tr>")
        html.append("</tbody></table>")
    '''

    # get and write entity pairs
    html.append("<h3>Entity Pairs:</h3>")
    pairs = DocSummary(doc).entpairs(
        format="htmlc", 
        rel_ops=[ "<", ">", "<<", ">>", ".", ";" ], 
        left_types=["PERIOD", "YEARSPAN"], 
        right_types=["OBJECT"]
        )
    html.append(pairs)

    '''
    entity_pairs = EntityPairs(
        doc=doc, 
        rel_ops=[ "<", ">", "<<", ">>", ".", ";" ], 
        left_types=["PERIOD", "YEARSPAN"], 
        right_types=["OBJECT"]
    ).pairs

    if len(entity_pairs) == 0:
        html.append("<p>NONE FOUND</p>")
    else:
        html.append("<table><tbody>")
        for pair in entity_pairs:
            html.append("<tr>")
            html.append("<td style='text-align:right; vertical-align: middle;'>")
            html.append(f"<div class='entity {escape(pair.ent1.label_.lower())}'>")
            if(pair.ent1.ent_id_.startswith("http")):
                html.append(f"<a href='{pair.ent1.ent_id_}'>{escape(pair.ent1.text)}</a>")
            else:
                html.append(f"{escape(pair.ent1.text)}")
            html.append("</div></td>")                    
            html.append(f"<td style='text-align:left; vertical-align: middle'>")
            html.append(f"<div class='entity {escape(pair.ent2.label_.lower())}'>")
            if(pair.ent2.ent_id_.startswith("http")):
                html.append(f"<a href='{pair.ent2.ent_id_}'>{escape(pair.ent2.text)}</a>")
            else:
                html.append(f"{escape(pair.ent2.text)}")
            html.append("</div></td>")
            html.append(f"<td>({pair.score})</td>")
            html.append("</tr>")
        html.append("</tbody></table>")
    '''
    
    # write list of negated entities
    html.append("<h3>Negated Entities:</h3>")
    negated_ents = list(filter(lambda ent: ent._.is_negated == True, doc.ents))
    if len(negated_ents) == 0:
        html.append("<p>NONE FOUND</p>")
    else:
        html.append("<table><tbody>")
        for ent in negated_ents: 
            html.append("<tr>")
            html.append("<td style='text-align:right; vertical-align: middle;'>")
            html.append(f"<div class='negated entity {escape(ent.label_.lower())}'>")
            if ent.ent_id_.startswith("http"):
                html.append(f"<a href='{ent.ent_id_}'>{escape(ent.text)}</a>") 
            else:
                html.append(f"<span>{escape(ent.text)}</span>")
            html.append("</div>")
            html.append("</td>")
            html.append(f"<td>({ent.start_char} &#8594; {ent.end_char - 1})</td>")
            html.append("</tr>")      
        html.append("</tbody></table>")

    # write list of tokens (trying out DocSummary class...)
    html.append(DocSummary(doc).tokens("htmll"))

    # finally, return the built HTML string
    return "".join(html)


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
    nlp.add_pipe("fish_archobjects_ruler", last=True)
    nlp.add_pipe("fish_monument_types_ruler", last=True)  
    # make sure negation_ruler is placed last in the pipeline, 
    # as it flags "is_negated" property for existing entities
    nlp.add_pipe("negation_ruler", last=True)    
    #print(nlp.pipe_names)

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
    
        # normalise white space prior to annotation
        # (extra spaces frustrate pattern matching)
        cleaned = normalize_whitespace(input_text)

        # perform the annotation
        doc = nlp(cleaned)

        # append to results
        results["results"].append({ "identifier": identifier, "doc": doc })

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
    results_to_text_file(file_name=f"{ results_file_name }.txt", results=test_results)
    results_to_html_file(file_name=f"{ results_file_name }.html", results=test_results)
    
    print(f"{__file__} done")
