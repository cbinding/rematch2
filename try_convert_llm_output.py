# =============================================================================
# Project   : ATRIUM
# Package   : rematch2
# Module    : try_convert_llm_output.py
# Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
# Contact   : ceri.binding@southwales.ac.uk
# Summary   : Convert 'significant' sections from LLM output into JSON format
#             for further processing
# Imports   : os, json, re, dataclass, Optional
# Example   : python try_convert_llm_output.py
# License   : http://creativecommons.org/publicdomain/zero/1.0/ [CC0]
# =============================================================================
# History
# 18/11/2025 CFB Initially created script
# =============================================================================

import os, json, re
from dataclasses import dataclass
from typing import Optional

DEFAULT_SECTION_TYPE: str = "llm_significance"

@dataclass(frozen=True)
class Substitution:
    find: str
    repl: str
    ignoreCase: Optional[bool] = True


# text substitutions to normalize ligatures (English)
substitute_ligatures_en: list[Substitution] = [
    Substitution("ﬀ", "ff"),
    Substitution("ﬁ", "fi"),
    Substitution("ﬂ", "fl"),
    Substitution("ﬃ", "ffi"),
    Substitution("ﬄ", "ffl"),
    Substitution("ﬅ", "ft"),
    Substitution("ﬆ", "st"),
    Substitution("ß", "s"),
    Substitution("Ꜳ", "AA", False),
    Substitution("ꜳ", "aa", False),    
    Substitution("Æ", "AE", False),
    Substitution("æ", "ae", False),   
    Substitution("Œ", "OE", False),     
    Substitution("œ", "oe", False)    
]


# normalize text by removing extra whitespace and substituting ligatures
def normalize_text(text):
    text = " ".join(text.strip().replace("\n", " ").replace("\r", " ").split())
    for item in substitute_ligatures_en:
        text = re.sub(item.find, item.repl, text, flags=re.IGNORECASE if item.ignoreCase else 0)
    return text


# read and parse a JSON file, returning the content as a dictionary
def read_json_file(file_path: str="") -> dict:
    file_content = {}
    with open(file_path, "r", encoding="utf-8") as f:
        file_content = json.load(f)
    return file_content


# get locations of identified sections in the LLM output within the report text
def get_llm_sections(llm_file_content: dict={}, report_text: str="", section_type: str=DEFAULT_SECTION_TYPE) -> list:  

    # normalize the report text for better matching
    report_text = normalize_text(report_text)
    
    new_sections = []
    llm_sections = llm_file_content.get("sections", [])
    for section in llm_sections:
        # normalize the section text for better matching
        llm_section_text = normalize_text(section.get("Sentence", ""))
        # locate the section text in the report text
        index = report_text.find(llm_section_text)
        if index == -1:
            print(f"Section not found: \"{llm_section_text[:100]}...\"")  # Print truncated text
            continue # section not found, don't include in results
        else:
            # create a new section for the results
            new_sections.append({
                "type": section_type, 
                "text": llm_section_text,
                "start": index, 
                "end":  index + len(llm_section_text),
                "comment": section.get("Rationale", "")
            })
            print(f"Section found at position {new_sections[-1]['start']} to {new_sections[-1]['end']}: \"{(llm_section_text[:60])}...\"")

    return new_sections


def add_llm_sections(json_file_content: dict={}, llm_sections: list=[], section_type: str=DEFAULT_SECTION_TYPE) -> dict:
        
    # add the sections to the JSON file content        
    if "sections" not in json_file_content:              
        json_file_content["sections"] = llm_sections
    else:
        # remove any existing sections of the specified type and replace with the new ones
        json_file_content["sections"] = [s for s in json_file_content["sections"] if s.get("type") != section_type]  
        json_file_content["sections"].extend(llm_sections) 

    return json_file_content 


if __name__ == "__main__":
    llm_files_folder = "./data/doug_llm/"
    json_files_folder = "./data/oasis/journals_july_2024/text_extraction-20251117"

    # for bulk processing
    file_names = [
        { "json_file": "text_extraction_archael547-079-116-ceolwulf.pdf.json", "llm_file": "gemini-ceolwulf-prompt14.json" },
        #{ "json_file": "text_extraction_2022_96_013-068_Huxley.pdf.json", "llm_file": "gemini-huxley-prompt13.json" },
    ]

    for item in file_names:
        llm_file_name = item.get("llm_file", "")
        json_file_name = item.get("json_file", "")

        print(f"Processing LLM file: {llm_file_name} with JSON file: {json_file_name}")
        
        # read and parse the llm output file content 
        llm_file_path = os.path.join(llm_files_folder, llm_file_name)
        llm_file_content = read_json_file(llm_file_path)

        # read and parse the json data file content
        json_file_path = os.path.join(json_files_folder, json_file_name)
        json_file_content = read_json_file(json_file_path)
        
        # normalize the report text for better matching
        report_text = normalize_text(json_file_content.get("text", ""))

        # write the normalised text to the JSON file content (for reference)
        json_file_content["text_normalized"] = report_text

        # get the sections (with positions) from the LLM output file content
        section_type: str = DEFAULT_SECTION_TYPE
        llm_sections: list = get_llm_sections(llm_file_content, report_text, section_type)
        if llm_sections:
            # add the sections to the JSON file content
            json_file_content = add_llm_sections(json_file_content, llm_sections, section_type)
            
        # write the updated JSON file content back to the file
        with open(json_file_path, "w", encoding="utf-8") as f:
            json.dump(json_file_content, f, ensure_ascii=False, indent=4)

    print("Processing complete.")