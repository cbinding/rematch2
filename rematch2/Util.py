import spacy
import json
from spacy.language import Language
from spacy.tokens import Doc


# get suitable spaCy NLP pipeline for given ISO639-1 (2-char) language code
def get_pipeline_for_language(language: str="") -> Language:
    pipe_name = ""
    match language.strip().lower():
        case "cs":
            pipe_name = "pl_core_news_sm"   # Polish (experiment for now, as there is no Czech SpaCy)
        case "de":
            pipe_name = "de_core_news_sm"   # German
        case "en":
             pipe_name = "en_core_web_sm"   # English
        case "es":
            pipe_name = "es_core_news_sm"   # Spanish
        case "fr":
            pipe_name = "fr_core_news_sm"   # French
        case "it":
            pipe_name = "it_core_news_sm"   # Italian
        case "nl":
            pipe_name = "nl_core_news_sm"   # Dutch
        case "no":
            pipe_name = "nb_core_news_sm"   # Norwegian Bokmal
        case "sv":
            pipe_name = "sv_core_news_sm"   # Swedish
        case _:
            pipe_name = ""

    # create the pipeline
    if pipe_name != "":
        nlp = spacy.load(pipe_name, disable=['ner'])
    else:
        nlp = spacy.blank("xx")
    return nlp


# normalize string whitespace
def normalize_whitespace(s: str = ""): 
    return ' '.join(s.strip().split()) 


# normalize input patterns with Language pipeline
# as used for custom rulers, for consistency
# patterns: [{id, label, pattern}, {id, label, pattern},...]    
def normalize_patterns(
    nlp: Language, 
    patterns: list=[],
    default_label: str="UNKNOWN",
    lemmatize: bool=True,
    min_lemmatize_length: int=4,
    min_term_length: int=3,
    pos: list=[]
    ) -> list:
    normalized_patterns = []

    for item in patterns:
        # clean values before using
        clean_id = normalize_whitespace(item.get("id", ""))
        clean_label = normalize_whitespace(item.get("label", default_label))
        pattern = item.get("pattern", "")

        # is there even a pattern present? 
        # (at this point it may be a list or a str)
        if len(pattern) > 0:

            # if already a token pattern  [{}, {}, ...]
            if isinstance(pattern, list):

                # just add to normalized_patterns
                normalized_patterns.append({
                    "id": clean_id,
                    "label": clean_label,
                    "pattern":  pattern
                })

            # if phrase pattern (plain string term/phrase)   
            elif isinstance(pattern, str):
                    
                # normalize whitespace (inconsistent whitespace can frustrate matching)
                clean_phrase = normalize_whitespace(pattern)
                    
                # if too small don't include it at all
                if len(clean_phrase) < min_term_length:
                    continue

                # first tokenize the phrase
                doc = nlp(clean_phrase)
                phrase_length = len(doc)
                    
                # build a new token pattern for this phrase
                new_pattern = []                    
                # for each term (token) in the phrase
                #for n, tok in enumerate(doc, 0):
                for tok in doc:
                    element = {}

                    # lemmatize term if required (providing term is long enough)
                    # e.g. "skirting boards":
                    # { "LEMMA": "skirt" }, { "LEMMA": "board" } or
                    # { "LOWER": "skirt" }, { "LOWER": "board" }
                    # IMPORTANT: lemmatization may not work if text is
                    # capitalised, as spaCy regards it as a proper Noun
                    if (lemmatize == True and len(tok.text) >= min_lemmatize_length):
                        element["LEMMA"] = tok.lemma_.lower()
                    else:
                        element["LOWER"] = tok.text.lower()  
                    
                    # add pos tags check if any passed in
                    # note POS (was) only applied to LAST term if multi-word phrase
                    # e.g. { "LEMMA": "board", "POS": { "IN": ["NOUN", "PROPN"] }}
                    # 06/03/2024 - POS now only applied to single words, but not phrases
                    #if (len(pos) > 0 and n == phrase_length):
                    if (len(pos) > 0 and phrase_length == 1):
                        element["POS"] = {"IN": pos}

                    new_pattern.append(element)
                    
                # add newly built pattern to normalized_patterns
                # print(new_pattern)
                normalized_patterns.append({
                    "id": clean_id,
                    "label": clean_label,
                    "pattern":  new_pattern
                })

    # finally, return the normalized list        
    return normalized_patterns


# load list of patterns from specified JSON file
def _patterns_from_json_file(file_path: str) -> list:
    patterns = []

    with open(file_path, "r") as f:
        patterns = json.load(f)

    return patterns


def doc_toks_to_text(doc: Doc)-> str:
    result = "tokens:\n"
    for tok in doc:
        result += "{index:<4} {span:^12} {pos:<10} {text:<40}\n".format(
            index = tok.i,
            span = f"({tok.idx + 1} -> {tok.idx + len(tok.text)})",
            pos = tok.pos_,
            text = f"\"{tok.text}\""
        )
    return result


def doc_ents_to_text(doc: Doc)-> str:
    result = "entities:\n"
    for ent in doc.ents:
        result += "{index:4} {span:^12} {type:<10} {id} {text:<40}\n".format(
            index="",                
            span = f"({ent.start_char + 1} -> {ent.end_char})",
            type = ent.label_,
            text = f"\"{ent.text}\"",
            id = ent.ent_id_
        )
    return result
    

    def entities_to_html_list(doc: Doc)-> str:result = ""
    result = "<ul>"
    for ent in doc.ents:
            result += f"<li>({ent.start_char} &#8594; {ent.end_char - 1}) \"{ent.text}\" [{ent.label_}]</li>"
    result += "</ul>"