# this will be the main script for bulk processing of the OASIS journal reports
import mimetypes, json
from pathlib import Path
from typing import Literal
import argparse
import srsly # for JSONL serialization/deserialization
from spacy.language import Language
from datetime import datetime as DT # for timestamps
from slugify import slugify # for valid filenames from identifiers
from weasyprint import HTML
from components import DocSummary, SpanScorer

from ATRIUM_T4_1_2_IE_pipeline import create_configured_pipeline
# imported like this because there is a hyphen in the name
from atrium_text_extraction import pdf_to_json # Sheffield script

# run configured information extraction pipeline on specified set of input documents
def run_IE(
    nlp: Language,          # pre-configured spaCy pipeline to do the IE
    input_path: Path,       # directory containing input files 
    output_path: Path,      # directory to write output files (will be created if it doesn't exist)    
    input_patt: str="*",    # file name pattern to restrict to particular input files (e.g. "*.pdf")
    output_format: Literal["pdf", "txt", "csv", "json"]="json" # format to write output
    ): 
    print(f"Running {__file__}")
    # if output folder structure does not already exist, build it
    if not Path.exists(output_path): Path.mkdir(output_path)
    
    # processing each file in the specified input path
    print(f"Processing files in input path '{input_path}'")
    file_names = input_path.rglob(input_patt) # file names filtered by pattern 
    #file_names = Path().rglob(input_path) # get_file_names_for_path(input_directory)
    for entry in file_names:        
        
        if not entry.is_file(): continue
           
        input_file_name: str = entry.name
        #input_file_path = entry.absolute. entry..path
        input_file_type, encoding = mimetypes.guess_type(input_file_name)
        input_file_ext: str = entry.stem.lower()
        input_file_content: dict = {}
        
        print(f"Processing file '{input_file_name}'...")

        # get the file content based on file type (e.g. PDF, JSON, TXT, etc.)
        # note: think mimetypes.guess_type only uses file extension anyway,
        # may be more accurate to use python-magic?        
        if input_file_type == "application/json" or input_file_ext == "json": 
            print(f"Reading JSON file '{input_file_name}'...")      
            with entry.open() as f:    
                input_file_content = json.load(f)
        elif input_file_type == "application/jsonl" or input_file_ext == "jsonl": 
            # different case - need to cater for multiple records...
            print(f"Reading JSONL file '{input_file_name}'...")  
            data: list = list(srsly.read_jsonl(input_file_name))            
            input_file_content = data[0] # very temp...
        elif input_file_type == "text/plain" or input_file_ext == "txt":     
            print(f"Reading TXT file '{input_file_name}'...")  
            with entry.open() as f:          
            #with open(input_file_path, 'r') as f:
                input_file_content = {"text": f.read()}
        elif input_file_type == "application/pdf" or input_file_ext == "pdf": 
            print(f"Reading PDF file '{input_file_name}'...") 
            input_file_content = pdf_to_json.convert(entry)            
            #input_file_content = {"text": ""}
        else:
            print(f"Unsupported file type, skipping {input_file_name}")
            continue
        
        # get any existing metadata from the input file       
        old_metadata: dict = input_file_content.get("meta", {})      
        # set up new metadata to include in the output
        new_metadata: dict = {
            "identifier": input_file_name,
            "title": "vocabulary-based IE results",
            "description": f"vocabulary-based information extraction results for file '{input_file_name}'",
            "creator": __file__, # "ATRIUM_T4_1_2_IE_OASIS_journal_reports.py",
            "created": DT.now().isoformat(),
            "pipeline": nlp.pipe_names,
            "input_file_name": input_file_name
        }
        # merge with existing metadata in input_file_content 
        the_metadata: dict = {**old_metadata, **new_metadata}
        input_file_content["meta"] = the_metadata
      
        # run the IE pipeline on the 'text' property of the input 
        print(f"Running IE pipeline on file '{input_file_name}'...")
        ts_nlp = DT.now()         
        doc = nlp(input_file_content.get("text",""))
        print(f"finished IE pipeline in {DT.now() - ts_nlp}")

        # add calculated scores to spans
        print(f"Adding calculated scores for file '{input_file_name}'...")
        ts_add = DT.now() 
        sections = list(input_file_content.get("sections", []))
        scorer = SpanScorer(nlp, sections=sections)
        doc = scorer(doc)
        print(f"finished adding calculated scores in {DT.now() - ts_add}")
        
        print(f"Summarizing results for file '{input_file_name}'...")
        ts_sum = DT.now()         
        summary = DocSummary(doc, metadata=the_metadata)
        print(f"finished summarizing results in {DT.now() - ts_sum}")

        # write results to output file
        output_file_name =  Path(output_path).joinpath(f"ie-output-{slugify(entry.name)}.{output_format}")
        print(f"Creating report '{output_file_name}'...")  
        ts_out = DT.now()        
        
        match output_format:
            case "json": 
                report = summary.report_to_json() 
                # include sections in output for score diagnostics
                report["sections"] = input_file_content.get("sections", [])  
                    
                with open(output_file_name, "w") as file:
                    # converting to JSON string first for pretty printing
                    json_string = json.dumps(report, indent=4, default=str)
                    file.write(json_string)
            case "txt":
                with open(output_file_name, "w") as file:
                    file.write(summary.report_to_text())
            case "csv":
                with open(output_file_name, "w") as file:
                    file.write(summary.spans_to_csv())
            case "pdf":
                report = summary.report_to_html()
                HTML(None, string=report, encoding="utf-8").write_pdf(target=output_file_name)    
            case _:
                print(f"Output format '{output_format}' not currently handled")      

        print(f"finished creating report in {DT.now() - ts_out}")

    print(f"Finished running {__file__}")


# Input parameters for running from terminal/command line. Example:
# python ./ATRIUM_T4_1_2_IE_OASIS_journal_reports.py -i './data/oasis/journals_july_2024' -p '*.pdf' -f "json"
# python ./ATRIUM_T4_1_2_IE_OASIS_journal_reports.py -i './data/oasis/journals_july_2024' -p '120_215*.pdf' -f "json"
if __name__ == "__main__":
    
    # initiate the input arguments parser
    parser = argparse.ArgumentParser(
        prog=__file__, description="ATRIUM T4_1_2 IE for OASIS journal reports")

    # add long and short argument descriptions for input file path (directory containing files to be processed)
    parser.add_argument(
        "--inputpath", "-i", 
        required=True,
        help="Input directory containing files to be processed")
    
    # add long and short argument descriptions for input file pattern (file names pattern)
    parser.add_argument(
        "--inputpatt", "-p", 
        default="*", 
        help="Pattern to specify file names to be processed")

    # add long and short argument descriptions for output file path (directory to write processed files to)
    parser.add_argument(
        "--outputpath", "-o", 
        required=False,
        help="Output directory for processed data files")
    
    # add long and short argument descriptions for output format (e.g. json, csv, etc.) for processed data files
    parser.add_argument(
        "--outputformat", "-f", 
        default="json", 
        const="json",
        nargs="?",
        choices=("txt" "csv", "json", "pdf"),
        help="Output format for processed data files"
    )    

    # datestamp for use in directory names
    datestamp = DT.now().strftime('%Y%m%d') 

    # parse and clean command line arguments
    args = parser.parse_args()
    input_path = Path(args.inputpath.strip())
    output_path = Path(args.outputpath.strip() if args.outputpath else Path(input_path).joinpath(f"ie-output-{datestamp}"))
    input_patt = args.inputpatt.strip() if args.inputpatt else "*"
    output_format = args.outputformat.strip().lower() if args.outputformat else "json"
    
    # create the spaCy pipeline to use
    print("Creating configured IE pipeline")
    pipeline = create_configured_pipeline() 
    print("Finished creating configured IE pipeline")

    # run the pipeline using cleaned input args
    print("Running IE pipeline")
    run_IE(
        nlp = pipeline,
        input_path = input_path,
        input_patt = input_patt, 
        output_path = output_path, 
        output_format = output_format
    )
    print("Finished running IE pipeline")