# this will be the main script for bulk processing of the OASIS journal reports
import mimetypes, json
from pathlib import Path
from typing import Literal
import argparse
import srsly # for JSONL serialization/deserialization
from spacy.tokens import Doc
from spacy.language import Language
from datetime import datetime as DT # for timestamps
from slugify import slugify # for valid filenames from identifiers
from weasyprint import HTML
from components import DocSummary, SpanScorer
from ATRIUM_T4_1_2_IE_pipeline import create_configured_pipeline
from atrium_text_extraction import pdf_to_json # Sheffield script in submodule

# returns dict structure with "text" property
def get_file_content(file_path: Path) -> dict:

    if not file_path.is_file(): return {}
           
    file_name: str = file_path.name
    file_type, encoding = mimetypes.guess_type(file_name)
    file_ext: str = file_path.stem.lower()
    file_content: dict = {}

    # get the file content based on file type (e.g. PDF, JSON, TXT, etc.)
    # note: think mimetypes.guess_type only uses file extension anyway,
    # may be more accurate to use python-magic?        
    if file_type == "application/json" or file_ext == "json": 
        with file_path.open() as f:    
            file_content = json.load(f)
    elif file_type == "text/plain" or file_ext == "txt":     
        with file_path.open() as f:          
            file_content = {"text": f.read()}
    elif file_type == "application/pdf" or file_ext == "pdf": 
        file_content = pdf_to_json.convert(file_path)   
    else:
        print(f"Unsupported file type '{file_type}' (expected JSON, TXT or PDF)")
        
    return file_content


def run_pipeline(nlp: Language, input_data: dict={}) -> Doc: 
    # run the IE pipeline on the 'text' property of the input
    doc = nlp(input_data.get("text",""))
    # add calculated scores to spans
    sections = list(input_data.get("sections", []))    
    scorer = SpanScorer(nlp, sections=sections)
    doc = scorer(doc)
    # return the document
    return doc

valid_formats = Literal["pdf", "txt", "csv", "json"]
def write_reports(
    doc: Doc,
    file_name: str="",
    metadata: dict={},
    sections: list = [], 
    formats: list[valid_formats]=["json"]):
    
    print(f"Summarizing results...")
    ts_sum = DT.now()         
    summary = DocSummary(doc, metadata=metadata)
    print(f"finished summarizing results in {DT.now() - ts_sum}")
    
    for format in formats:
        file_name_with_suffix = f"{file_name.strip()}.{format.strip()}"
        match format:
            case "json": 
                report = summary.report_to_json() 
                # include sections in output for score diagnostics
                report["sections"] = sections 
                # write report to file    
                with open(file_name_with_suffix, "w") as file:
                    # converting to JSON string first, for pretty printing
                    json_string = json.dumps(report, indent=4, default=str)
                    file.write(json_string)
            case "txt":
                report = summary.report_to_text()
                with open(file_name_with_suffix, "w") as file:
                    file.write(report)
            case "csv":
                report = summary.spans_to_csv()
                with open(file_name_with_suffix, "w") as file:
                    file.write(report)
            case "pdf":
                report = summary.report_to_html()
                HTML(None, string=report, encoding="utf-8").write_pdf(target=file_name_with_suffix)    
            case _:
                print(f"Format '{format}' not currently handled") 


# run configured information extraction pipeline on specified set of input documents
def run_information_extraction(
    nlp: Language,          # pre-configured spaCy pipeline 
    input_path: Path,       # directory containing input files 
    output_path: Path,      # directory to write output files (will be created if it doesn't exist)    
    input_patt: str="*",    # file name pattern to restrict to particular input files (e.g. "*.pdf")
    output_formats: list[valid_formats]=["json"] #Literal["pdf", "txt", "csv", "json"]="json" # format to write output
    ): 
    # if output folder structure does not already exist, build it
    if not Path.exists(output_path): Path.mkdir(output_path)
    
    # processing each file in the specified input path
    print(f"Processing files in input path '{input_path}'")
    file_names = input_path.rglob(input_patt) # file names filtered by pattern 
    for entry in file_names:        
        
        if not entry.is_file(): continue 
        print(f"Reading file '{entry.name}'...")
        file_content = get_file_content(entry)
        
        # get any existing metadata from the input file       
        old_metadata: dict = file_content.get("meta", {})      
        # set up new metadata to include in the output
        new_metadata: dict = {
            "identifier": entry.name,
            "title": "vocabulary-based IE results",
            "description": f"vocabulary-based information extraction results for file '{entry.name}'",
            "creator": __file__, 
            "created": DT.now().isoformat(),
            "pipeline": nlp.pipe_names,
            "input_file_name": entry.name
        }
        # merge with existing metadata in input_file_content 
        metadata: dict = {**old_metadata, **new_metadata}
        file_content["meta"] = metadata
      
        # run the IE pipeline on the 'text' property of the input 
        print(f"Running IE pipeline on '{entry.name}'...")        
        doc = run_pipeline(nlp, file_content)

        # write results to output file
        output_file_name = Path(output_path).joinpath(f"ie-output-{slugify(entry.name)}")
        print(f"Creating report '{output_file_name}'...")  
        ts_out = DT.now()        
        
        write_reports(
            doc=doc, 
            file_name=str(output_file_name), 
            metadata=file_content.get("meta",{}),
            sections=file_content.get("sections", []),
            formats=output_formats)
        
        print(f"finished creating report in {DT.now() - ts_out}")

    print(f"Finished running {__file__}")


# Input parameters for running from terminal/command line. Example:
# python ./ATRIUM_T4_1_2_IE_OASIS_journal_reports.py -i './data/oasis/journals_july_2024' -p '*.pdf' -f "json,csv"
# python ./ATRIUM_T4_1_2_IE_OASIS_journal_reports.py -i './data/oasis/journals_july_2024' -p '120_001*.pdf' -f "json,csv"
if __name__ == "__main__":
    
    # initiate the input arguments parser
    parser = argparse.ArgumentParser(
        prog=__file__, description="ATRIUM T4_1_2 IE for OASIS journal reports")

    # add long and short argument descriptions for input file path (directory containing files to be processed)
    parser.add_argument(
        "--inputpath", "-i", 
        required=True,
        help="Input directory containing files to be processed")
    
    # add long and short argument descriptions for input file pattern (file names pattern e.g. "*.pdf")
    parser.add_argument(
        "--inputpatt", "-p", 
        default="*", 
        const="*",
        nargs="?",
        help="Pattern to specify file names to be processed")

    # add long and short argument descriptions for output file path (directory to write processed files to)
    parser.add_argument(
        "--outputpath", "-o",
        required=False,
        help="Output directory for processed data files")
    
    # add long and short argument descriptions for output format (e.g. json, csv, etc.) for processed data files
    # note outputformat is a string but may be multiple comma-delimited values e.g. -f "json, csv"
    parser.add_argument(
        "--outputformat", "-f", 
        default="json", 
        help="Output format(s) for processed data files"
    )    

    # datestamp for use in directory names
    datestamp = DT.now().strftime('%Y%m%d') 

    # parse and clean command line arguments
    args = parser.parse_args()
    input_path: Path = Path(args.inputpath.strip())
    output_path: Path = Path(args.outputpath.strip() if args.outputpath else Path(input_path).joinpath(f"ie-output-{datestamp}"))
    input_patt: str = args.inputpatt.strip() if args.inputpatt else "*"
    output_formats: list = list(set(args.outputformat.strip().lower().split(","))) if args.outputformat else ["json"]
    
    # create the spaCy pipeline to use
    print("Creating configured pipeline")
    pipeline = create_configured_pipeline() 
    print("Created configured pipeline")

    # run the pipeline using cleaned input args
    print("Running information extraction")
    run_information_extraction(
        nlp = pipeline,
        input_path = input_path,
        input_patt = input_patt, 
        output_path = output_path, 
        output_formats = output_formats
    )
    print("Finished information extraction")