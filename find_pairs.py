"""
=============================================================================
Package   : 
Module    : find_pairs.py
Classes   : 
Project   : 
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : experimentation - identifying 'paired' spans
            e.g. "medieval furrow", "iron age barrow", "Roman villa" etc.
Imports   : pandas, spacy, lxml, json
Example   : 
License   : https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History
31/09/2023 CFB Initially created script
27/02/2024 CFB verbose results to JSON file, readable results to TXT file
               LogFile class moved to separate script
08/03/2024 CFB SpanPair and SpanPairs classes split out to separate files
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
from rematch2 import SpanPair, SpanPairs, PeriodoRuler, VocabularyRuler, NegationRuler, DocSummary, TextNormalizer, StringCleaning
from rematch2.Util import *
from decorators import run_timed # form local run timing
from .Util import DEFAULT_SPANS_KEY

# parse and extract list of records from source XML file 
# returns [{"id", "text"}, {"id", "text"}, ...] for subsequent processing
def get_records_from_xml_file(file_path: str="")-> list:
    records = []
    try:
        # read XML file
        tree = ET.parse(file_path)
        root = tree.getroot()
    except:
        print(f"Could not read from {file_path}")
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
            
        # write label counts (by desc count)             
        lines.append("\nLabel Counts:")  
        label_counts = DocSummary(doc).labelcounts(format="text")  
        lines.append(label_counts)

        # write span counts (by desc count)             
        lines.append("\nSpan Counts:")  
        span_counts = DocSummary(doc).spancounts(format="text")  
        lines.append(span_counts)           
                    
        # write span pairs as fixed width string values
        lines.append("\nSpan Pairs:")
        pairs = DocSummary(doc).spanpairs(
            format="text",
            rel_ops=[ "<", ">", "<<", ">>", ".", ";" ], 
            left_labels=["PERIOD", "YEARSPAN"], 
            right_labels=["FISH_OBJECT", "FISH_MONUMENT"]
        )
        lines.append(pairs)
        
        # write negated spans
        lines.append("\nNegated Spans:")
        negated_spans = list(filter(lambda span: span._.is_negated == True, doc.spans.get(DEFAULT_SPANS_KEY,[])))
        if len(negated_spans) == 0:
            lines.append("NONE FOUND")
        else:
            for span in negated_spans:
                lines.append("({start}->{end}) [{label}] {id:<60} {text}".format(
                    start = span.start,
                    end = span.end,
                    label = span.label_,
                    id = span.ent_id_,
                    text = span.text
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
    html.append("<details>")
    html.append(f"<summary>Metadata</summary>")
    #html.append("<h3>Metadata:</h3>")
    html.append("<ul>")
    html.append(f"<li><strong>title:</strong> {metadata.get('title', '')}</li>")
    html.append(f"<li><strong>description:</strong> {metadata.get('description', '')}</li>")
    html.append(f"<li><strong>started:</strong>              {metadata.get('timestamp', '')}</li>")
    html.append(f"<li><strong>periodo authority ID:</strong> {metadata.get('periodo_authority_id', '')}</li>")
    html.append(f"<li><strong>input records count:</strong>  {metadata.get('input_record_count', '')}</li>")
    html.append("</ul>")
    html.append("</details>")

    # write results in body tag
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
        html_file.write("".join(html))


# write single results as a HTML string for presentation output
def result_to_html_string(identifier: str = "", doc: Doc = None) -> str:

    html = []
    # start with horizontal line break
    html.append("<hr>") 
    
    # write identifier as heading
    html.append("<h4>")
    if(identifier.startswith("http")):
        html.append(f"<a target='_blank' rel='noopener noreferrer' href='{identifier}'>{identifier}</a>")
    else:
        html.append(f"{escape(identifier)}")
    html.append("</h4>")

    # write displacy HTML rendering of doc text as paragraph with highlighted spans 
    html.append("<details>")
    html.append(f"<summary>Text ({len(DocSummary(doc).doctext())} characters)</summary>")
    doctext = DocSummary(doc).doctext_to_html()
    html.append(f"<p>{doctext}</p>")
    html.append("</details>")

    # write list of tokens
    html.append("<details>")
    html.append(f"<summary>Tokens ({len(DocSummary(doc).tokens('list'))})</summary>")        
    html.append(DocSummary(doc).tokens("htmll"))
    html.append("</details>")

    # write label counts
    html.append("<details>")
    html.append(f"<summary>Label Counts ({len(DocSummary(doc).labelcounts('list'))})</summary>")
    html.append(DocSummary(doc).labelcounts(format="htmlt"))
    html.append("</details>")
    
    # write span counts
    html.append("<details>")
    html.append(f"<summary>Span Counts ({len(DocSummary(doc).spancounts('list'))})</summary>")
    html.append(DocSummary(doc).spancounts(format="htmlt"))
    html.append("</details>")
    
    # get and write span pairs
    html.append("<details>")
    html.append(f"<summary>Span Pairs</summary>")
    pairs = DocSummary(doc).spanpairs(
        format="htmlt", 
        rel_ops=[ "<", ">", "<<", ">>", ".", ";" ], 
        left_labels=["PERIOD", "YEARSPAN"], 
        right_labels=["FISH_OBJECT", "FISH_MONUMENT"]
        )
    html.append(pairs)
    html.append("</details>")

    html.append("<details>")
    html.append(f"<summary>Negation</summary>")
    pairs = DocSummary(doc).spanpairs(
        format="htmlt", 
        rel_ops=[ "<", ">", "<<", ">>", ".", ";" ], 
        left_labels=["NEGATION"], 
        right_labels=["YEARSPAN", "PERIOD", "FISH_OBJECT", "FISH_MONUMENT"]
        )
    html.append(pairs)
    html.append("</details>")
        
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
    # as it flags "is_negated" property for existing spans
    nlp.add_pipe("negation_ruler", last=True)    
    #print(nlp.pipe_names)

    # create structured results (inc diagnostic information)
    results = {
        "metadata": {
            "title": "find_pairs.py results",
            "description": "find paired spans in text",
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
        cleaned = StringCleaning.normalize_whitespace(input_text)

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
        test_records = get_records_from_xml_file("./data/oasis_descr_examples.xml")
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
