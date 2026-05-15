import spacy
from spacy.language import Language
import pandas as pd
import json

DEFAULT_SPANS_KEY = "rematch" # default key for storing spans in Doc.spans

# get suitable spaCy NLP pipeline for given ISO639-1 (2-char) language code
def load_pipeline_for_language(language: str="") -> Language:
    # load appropriate language-specific pipeline based on ISO639-1 (2-char) language code
    packages = {
        "cs": "pl_core_news_sm",   # Polish (temp, experimental as there is no Czech SpaCy pipeline available)
        "de": "de_core_news_sm",    # German
        "en": "en_core_web_sm",     # English
        "es": "es_core_news_sm",    # Spanish
        "fr": "fr_core_news_sm",    # French
        "it": "it_core_news_sm",    # Italian
        "nl": "nl_core_news_sm",    # Dutch
        "no": "nb_core_news_sm",    # Norwegian Bokmal
        "sv": "sv_core_news_sm"     # Swedish
    }

    package_name: str|None = packages.get(language.strip().lower()[:2], None)
    if package_name is None:
        raise ValueError(f"Unsupported language code \"{language}\"")

    # load the spaCy pipeline for the specified language, disabling the default NER component    
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
