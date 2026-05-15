import spacy
from spacy.language import Language
import pandas as pd
import json

DEFAULT_SPANS_KEY = "rematch" # default key for storing spans in Doc.spans

# get suitable spaCy NLP pipeline for given ISO639-1 (2-char) language code
def load_pipeline_for_language(language: str="") -> Language:
    # load appropriate language-specific pipeline
    package_name: str = ""
    match language.strip().lower()[:2]:
        case "cs":
            package_name = "pl_core_news_sm"   # Polish (temp, experimental as there is no Czech SpaCy pipeline available)
        case "de":
            package_name = "de_core_news_sm"   # German
        case "en":
             package_name = "en_core_web_sm"   # English
        case "es":
            package_name = "es_core_news_sm"   # Spanish
        case "fr":
            package_name = "fr_core_news_sm"   # French
        case "it":
            package_name = "it_core_news_sm"   # Italian
        case "nl":
            package_name = "nl_core_news_sm"   # Dutch
        case "no":
            package_name = "nb_core_news_sm"   # Norwegian Bokmal
        case "sv":
            package_name = "sv_core_news_sm"   # Swedish
        case _:
            raise ValueError(f"Unsupported language code \"{language}\"")

    return spacy.load(package_name, disable=['ner'])
    

def read_csv_file(file_path: str, delimiter: str=",") -> list[dict]:
    # parse and extract records from CSV file; 
    # returns list[dict] for subsequent processing

    # read the CSV file to a DataFrame
    df = pd.read_csv(file_path, skip_blank_lines=True, delimiter=delimiter)
    # set any NaN values to blank string
    df.fillna("", inplace=True)
    # return data as a list[dict] structure
    return df.to_dict(orient="records") 


def read_json_file(file_path: str) -> list|dict:
    # read data from JSON file (supplementary lists and stopword lists)
    data = []
    try:
        with open(file_path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Problem reading \"{file_path}\": {e}")
    return data
