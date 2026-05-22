# this will be the main script for bulk processing of the OASIS journal reports
import mimetypes, json
from pathlib import Path
import argparse
import pandas as pd
from datetime import datetime as DT # for timestamps
from ATRIUM_T4_1_2_IE_pipeline import create_configured_pipeline


# run the configured pipeline and output results to files
if __name__ == "__main__":
    
    # initiate the input arguments parser
    parser = argparse.ArgumentParser(
        prog=__file__, description="ATRIUM T4_1_2 IE for OASIS journal reports")

    # add long and short argument descriptions for input file path (directory containing files to be processed)
    parser.add_argument("--inputpath", "-i", required=False, default="./data/oasis/journals_july_2024/*.pdf",
        help="Input directory containing files to be processed")
    
    # add long and short argument descriptions for output file path (directory to write processed files to)
    parser.add_argument("--outputpath", "-o", required=False,
        help="Output directory for processed data files")
    
    # add long and short argument descriptions for output format (e.g. json, csv, etc.) for processed data files
    parser.add_argument("--outputformat", "-f", required=False, default="json",
        help="Output format for processed data files")

    # parse command line arguments
    args = parser.parse_args()

    # timestamp for use in directory names
    timestamp = DT.now().strftime('%Y%m%d')   

    # clean required arguments
    input_path = args.inputpath.strip() if args.inputpath else "./"
    output_path = Path(args.outputpath.strip() if args.outputpath else Path(input_path).joinpath(f"ie-output-{timestamp}"))
    output_format = args.outputformat.strip() if args.outputformat else "json"
    
    # create output folder structure if it does not already exist 
    #output_path = Path(output_directory)   
    if not Path.exists(output_path):
        Path.mkdir(output_path)
    
    # create a pre-configured information extraction pipeline
    print("Creating configured pipeline...")
    nlp = create_configured_pipeline() 
    print(f"Pipeline created with components: {nlp.pipe_names}")

    # process each eligible file in the input directory
    print(f"Processing files in input path '{input_path}'")
    file_names = Path().rglob(input_path) # get_file_names_for_path(input_directory)
    for entry in file_names: #os.scandir(input_directory):
        
        if not entry.is_file():
            continue
           
        input_file_name: str = entry.name
        #input_file_path = entry.absolute. entry..path
        input_file_type, encoding = mimetypes.guess_type(input_file_name)
        input_file_ext: str = entry.stem.lower()
        input_file_content = {}
        
        print(f"Processing file '{input_file_name}'...")

        # get the file content based on file type (e.g. PDF, JSON, TXT, etc.)
        # note: think mimetypes.guess_type only uses file extension anyway,
        # may be more accurate to use python-magic?        
        if input_file_type == "application/json" or input_file_ext == "json": 
            print(f"Reading JSON file '{input_file_name}'...")      
            with entry.open() as f:    
            #with open(input_file_path, 'r') as f:
                input_file_content = json.load(f)
        elif input_file_type == "text/plain" or input_file_ext == "txt":     
            print(f"Reading TXT file '{input_file_name}'...")  
            with entry.open() as f:          
            #with open(input_file_path, 'r') as f:
                input_file_content = {"text": f.read()}
        elif input_file_type == "application/pdf" or input_file_ext == "pdf": 
            print(f"Reading PDF file '{input_file_name}'...") 
            input_file_content = {"text": ""}
        else:
            print(f"Unsupported file type, skipping {input_file_name}")
            continue
        
        # set up metadata to include in output reports
        metadata = {
            "identifier": input_file_name,
            "title": "vocabulary-based IE results",
            "description": f"vocabulary-based information extraction results for file {input_file_name}",
            "creator": "ATRIUM_T4_1_2_IE_OASIS_journal_reports.py",
            "created": DT.now().isoformat(),
            "pipeline": nlp.pipe_names,
            "input_file_name": input_file_name
        }
        #  TODO merge with any existing metadata in input file content (if present) and update created timestamp
        #input_file_content["meta"] = metadata

        print(f"Running pipeline on file '{input_file_name}'...")
        #doc = nlp(input_file_content.get("text", ""))
        print(f"Done")

        