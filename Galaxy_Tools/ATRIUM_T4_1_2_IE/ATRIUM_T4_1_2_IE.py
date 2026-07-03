import json
from pathlib import Path
from typing import Literal
import argparse

from spacy.tokens import Doc
from spacy.language import Language
from datetime import datetime as DT # for timestamps
from components import DocSummary, SpanScorer
from ATRIUM_T4_1_2_IE_pipeline import create_configured_pipeline

def run_pipeline(nlp: Language, input_data: dict={}) -> Doc: 
    # run the IE pipeline on the 'text' property of the input
    doc = nlp(input_data.get("text",""))
    # add calculated scores to spans
    sections = list(input_data.get("sections", []))    
    scorer = SpanScorer(nlp, sections=sections)
    doc = scorer(doc)
    # return the document
    return doc

def write_report(
    doc: Doc,
    file_name: str="",
    metadata: dict={},
    sections: list = []):
    
    print(f"Summarizing results...")
    ts_sum = DT.now()         
    summary = DocSummary(doc, metadata=metadata)
    print(f"finished summarizing results in {DT.now() - ts_sum}")

    file_name_with_suffix = file_name

    report = summary.report_to_json() 
    # include sections in output for score diagnostics
    report["sections"] = sections 
    # write report to file    
    with open(file_name_with_suffix, "w") as file:
        # converting to JSON string first, for pretty printing
        json_string = json.dumps(report, indent=4, default=str)
        file.write(json_string)

# run configured information extraction pipeline on specified set of input documents
def run_information_extraction(
    nlp: Language,          # pre-configured spaCy pipeline 
    input_path: Path,       # path to input JSON file
    output_path: Path,      # path to output JSON file
    ): 
    
    entry = input_path
    
    print(f"Reading file '{entry.name}'...")
    #file_content = get_file_content(entry)
    with entry.open() as f:    
        file_content = json.load(f)
    
    # get any existing metadata from the input file       
    old_metadata: dict = file_content.get("meta", {})      
    # set up new metadata to include in the output
    new_metadata: dict = {
        #"identifier": entry.name,
        "title": "vocabulary-based IE results",
        #"description": f"vocabulary-based information extraction results for file '{entry.name}'",
        "creator": __file__, 
        #"created": DT.now().isoformat(),
        "pipeline": nlp.pipe_names,
        #"input_file_name": entry.name
    }
    # merge with existing metadata in input_file_content 
    metadata: dict = {**old_metadata, **new_metadata}
    file_content["meta"] = metadata
    
    # run the IE pipeline on the 'text' property of the input 
    print(f"Running IE pipeline on '{entry.name}'...")        
    doc = run_pipeline(nlp, file_content)

    # write results to output file
    #output_file_name = Path(output_path).joinpath(f"ie-output-{slugify(entry.name)}")
    output_file_name = output_path
    print(f"Creating report '{output_file_name}'...")  
    ts_out = DT.now()        
    
    write_report(
        doc=doc, 
        file_name=str(output_file_name), 
        metadata=file_content.get("meta",{}),
        sections=file_content.get("sections", []))
    
    print(f"finished creating report in {DT.now() - ts_out}")

    print(f"Finished running {__file__}")


if __name__ == "__main__":
    
    # initiate the input arguments parser
    parser = argparse.ArgumentParser(
        prog=__file__, description="ATRIUM T4.1.2 IE Component")

    # add long and short argument descriptions for input file path (directory containing files to be processed)
    parser.add_argument(
        "--input", "-i", 
        required=True,
        help="Input JSON File to process")
    
    # add long and short argument descriptions for output file path (directory to write processed files to)
    parser.add_argument(
        "--output", "-o",
        required=False,
        help="Output JSON file")
    
    # parse and clean command line arguments
    args = parser.parse_args()
    input_path: Path = Path(args.input.strip())
    output_path: Path = Path(args.output.strip())
    
    # create the spaCy pipeline to use
    print("Creating configured pipeline")
    pipeline = create_configured_pipeline() 
    print("Created configured pipeline")

    # run the pipeline using cleaned input args
    print("Running information extraction")
    run_information_extraction(
        nlp = pipeline,
        input_path = input_path,
        output_path = output_path
    )
    print("Finished information extraction")