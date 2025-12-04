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

import regex # using regex (not re) to allow for e.g. \p{Dash_Punctuation}
import os, json, re
from dataclasses import dataclass, asdict
from typing import Optional
from unidecode import unidecode

@dataclass(frozen=True)
class Substitution:
    find: str
    repl: str
    ignoreCase: Optional[bool] = True


def compileSub(sub: Substitution) -> Substitution:
    flags = regex.IGNORECASE | regex.MULTILINE if sub.ignoreCase else regex.MULTILINE
    return Substitution(regex.compile(pattern=sub.find, flags=flags), sub.repl, sub.ignoreCase) 


@dataclass()
class Section:
    type: str=""
    text: str=""
    start: int=-1
    end: int=-1


# substitutions to normalize texts (English)
substitutions: list[Substitution] = [
    # ligature characters
    Substitution("ﬀ", "ff"),
    Substitution("ﬁ", "fi"),
    Substitution("ﬂ", "fl"),
    Substitution("ﬃ", "ffi"),
    Substitution("ﬄ", "ffl"),
    Substitution("ﬅ", "ft"),
    Substitution("ﬆ", "st"),
    Substitution("ß", "ss"),
    Substitution("Ꜳ", "AA", False),
    Substitution("ꜳ", "aa", False),    
    Substitution("Æ", "AE", False),
    Substitution("æ", "ae", False),   
    Substitution("Œ", "OE", False),     
    Substitution("œ", "oe", False),
    # newlines and carriage returns
    Substitution(r"\n", " "),   
    Substitution(r"\r", " "),   
    # double asterisks
    Substitution(r"\*{2,}", ""),
    # any dash character to single standard hyphen
    Substitution(r"\b\s*(\p{Dash_Punctuation})\s*(?=[^\p{Number}])", " - "),
    Substitution(r"\b(\p{Dash_Punctuation})\b", " - "),
    # spacing before/after slashes
    Substitution(r"\b\s*([\\\/])\s*\b", r" \1 "),
    # spacing before/after brackets
    Substitution(r"([^\s])\s*(\p{Open_Punctuation})\s*([^\s])", r"\1 \2\3"),
    Substitution(r"([^\s])\s*(\p{Close_Punctuation})\s*([^\s])", r"\1\2 \3"),        
    # convert ampersands (&) to "and"
    Substitution(r"(\p{Letter})\s+&\s+(\p{Letter})", r"\1 and \2"),
    # removing apostrophes
    Substitution(r"(\p{Letter})'s\s(\p{Letter})", r"\1s \2"),        
    Substitution(r"(\p{Letter}s)'\s(\p{Letter})", r"\1 \2"),
    # spacing after commas
    Substitution(r"(\p{Letter}),(\p{Letter})", r"\1, \2")
]


# normalize text substituting problematic characters and by removing extra whitespace
def normalize_text(text):
    
    #subs: list[Substitution] = list(map(compileSub, substitutions))
    text = unidecode(text) # unicode substitutions to nearest ASCII equivalent
    for item in substitutions: # NOTE - if using unidecode, we maybe don't need the ligature sustitution?
        text = regex.sub(item.find, item.repl, text, flags=re.IGNORECASE if item.ignoreCase else 0)
    # finally make whitespace consistent
    return " ".join(text.split()).strip()


# read and parse a JSON file, returning the content as a dictionary
def read_json_file(file_path: str="") -> dict:
    file_content = {}
    try:
        with open(file_path, "r", encoding="utf-8-sig") as f:
            file_content = json.load(f)
    except Exception as e:
        print(f"Problem reading \"{file_path}\": {e}")
    return file_content


# get location of identified section in the LLM output within the report text
def locate_section(section_text: str="", report_text: str="") -> Section:  

    # normalize the text for better matching
    report_text = normalize_text(report_text)
    section_text = normalize_text(section_text)

    new_section: Section = None
    index = report_text.find(section_text)
    if index == -1:
        print(f"Section not found: \"{section_text[:100]}\"")  # Print truncated text        
    else:
        # create a new section for the results
        new_section = Section(
            text = section_text,
            start = index, 
            end = index + len(section_text)
        )
        print(f"Section found at position {new_section.start} to {new_section.end}: \"{(section_text[:60])}...\"")

    return new_section


def delete_sections(json_file_content: dict={}, section_type: str="") -> dict:
    json_file_content["sections"] = [s for s in json_file_content.get("sections",[]) if s.get("type", "") != section_type.lower()]  
    return json_file_content


def append_sections(json_file_content: dict={}, new_sections: list[Section]=[]) -> dict:
    
    # make them serializable
    sections = map(asdict, filter(None, new_sections))

    # add the sections to the JSON file content        
    if "sections" not in json_file_content:              
        json_file_content["sections"] = sections
    else:
        json_file_content["sections"].extend(sections) 

    return json_file_content 


if __name__ == "__main__":
    llm_files_folder = "./data/doug_llm/GeminiJSONoutput2-TitleAbs"
    json_files_folder = "./data/oasis/journals_july_2024/text_extraction-20251117"

    for entry in os.scandir(llm_files_folder):
        if not entry.is_file() or not entry.name.lower().endswith(".json"):  
            continue

        llm_file_name = entry.name
        llm_file_path = entry.path
        llm_file_content = read_json_file(entry.path)

        json_file_name = llm_file_content.get("meta",{}).get("Document", "")
        json_file_path = os.path.join(json_files_folder, json_file_name)
        json_file_content = read_json_file(json_file_path)  

        print(f"\nProcessing LLM file: {llm_file_name} with JSON file: {json_file_name}")
                
        # normalize the report text for better matching
        report_text = normalize_text(json_file_content.get("text", ""))

        # write the normalised text to the JSON file content (for reference)
        json_file_content["text_normalized"] = report_text

        # get the title and abstract (if they exist) from the LLM output file content
        llm_title = normalize_text(llm_file_content.get("meta",{}).get("Title", ""))
        llm_abstract = normalize_text(llm_file_content.get("meta",{}).get("Abstract", ""))
        
        # find the title in the report text
        title_section: Section = locate_section(section_text = llm_title, report_text = report_text)
        if(title_section): title_section.type = "title"

        # find the abstract in the report text
        abstract_section: Section = locate_section(section_text = llm_abstract, report_text = report_text)
        if(abstract_section): abstract_section.type = "abstract"

        # delete existing title or abstract sections (if they exist)
        json_file_content = delete_sections(json_file_content, "llm_significance")
        json_file_content = delete_sections(json_file_content, "title")
        json_file_content = delete_sections(json_file_content, "abstract")

        # add the sections to the JSON file content
        new_sections = list(filter(None, [title_section, abstract_section]))
        json_file_content = append_sections(json_file_content, new_sections)
            
        # write the updated JSON file content back to the file
        with open(json_file_path, "w", encoding="utf-8") as f:
            json.dump(json_file_content, f, ensure_ascii=False, indent=4)
        #break # remove this break to process all files

    print("Processing complete.")