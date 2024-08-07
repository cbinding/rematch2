import spacy
import json
import re
from spacy.language import Language
from spacy.tokens import Token

if __package__ is None or __package__ == '':
    # uses current directory visibility
    from StringCleaning import normalize
else:
    # uses current package visibility
    from .StringCleaning import normalize

# get suitable spaCy NLP pipeline for given ISO639-1 (2-char) language code
def get_pipeline_for_language(language: str="") -> Language:
    pipe_name = ""
    match language.strip().lower():
        case "cs":
            pipe_name = "pl_core_news_sm"   # Polish (temp, experimental as there is no Czech SpaCy pipeline available)
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
        nlp = spacy.blank("xx-blank-xx")
    return nlp


# load list of patterns from specified JSON file
def _get_patterns_from_json_file(file_path: str) -> list:
    patterns = []

    with open(file_path, "r") as f:
        patterns = json.load(f)

    return patterns


# determine whether a token is within a previously labelled span
def is_token_within_labelled_span(tok: Token, label: str="DATEPREFIX", spans_key: str="custom") -> bool:
    # list any previously identified spans with this label in the document
    spans = list(filter(lambda span: span.label_ == label, tok.doc.spans.get(spans_key, [])))
    # is this token inside any of them?
    return any(span.start <= tok.i and span.end > tok.i for span in spans) 


# get list of labels for any spans this token is within
def get_labels_for_token(tok: Token, spans_key: str="custom") -> list: 
    outer_spans = filter(lambda span: span.start <= tok.i and span.end >= tok.i, tok.doc.spans.get(spans_key,[]))
    return list(set(map(lambda span: span.label, outer_spans)))


def is_dateprefix(tok: Token) -> bool: return is_token_within_labelled_span(tok, "DATEPREFIX")        
def is_datesuffix(tok: Token) -> bool: return is_token_within_labelled_span(tok, "DATESUFFIX")
def is_dateseparator(tok: Token) -> bool: return is_token_within_labelled_span(tok, "DATESEPARATOR")
def is_ordinal(tok: Token) -> bool: return is_token_within_labelled_span(tok, "ORDINAL")
def is_monthname(tok: Token) -> bool: return is_token_within_labelled_span(tok, "MONTHNAME")
def is_seasonname(tok: Token) -> bool: return is_token_within_labelled_span(tok, "SEASONNAME")


# normalize input patterns with Language pipeline
# used for custom rulers, for consistency
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
        clean_id = item.get("id", "").strip()
        clean_label = item.get("label", default_label).strip()
        pattern = item.get("pattern", "")

        # is a pattern present? (may be either a list or a string)
        if len(pattern) > 0:

            # if already a pre-structured token pattern [{}, {}, ...]
            if isinstance(pattern, list):

                # just add to normalized_patterns as it is
                normalized_patterns.append({
                    "id": clean_id,
                    "label": clean_label,
                    "pattern":  pattern
                })

            # if a string term or phrase
            elif isinstance(pattern, str):
                    
                # get normalized clean phrase, lower case
                clean_phrase = normalize(pattern).lower()
                
                # if too small don't include it at all
                if len(clean_phrase) < min_term_length:
                    continue

                # first tokenize the phrase
                doc = nlp(clean_phrase)
                phrase_length = len(doc)
                    
                # build a new token pattern for this phrase
                new_pattern = []                    
                # for each term (token) in the phrase
                # for n, tok in enumerate(doc, 0):
                for tok in doc:
                    element = {}

                    # lemmatize term if required (and if term long enough). Using both lemma AND original term,
                    # as lemmatization won't work if text is capitalised (spaCy may regard it as a proper Noun),
                    # and there doesn't seem to be a way to specify a rule to match on the lowercase of the lemma
                    # e.g. "skirting boards" - so pattern built is either:
                    # { "LEMMA": { "IN" { [ "SKIRT", "skirt", "Skirt", "SKIRTING", "skirting", "Skirting" ] },
                    # { "LEMMA": { "IN" { [ "BOARD", "board", "Board", "BOARDS", "boards", "Boards" ] } 
                    # or:
                    # { "LOWER": "skirting" }, { "LOWER": "boards" }                    
                    lemma = tok.lemma_.strip()
                    text = tok.text.strip()
                    
                    if (lemmatize == True and len(text) >= min_lemmatize_length):
                        # lemmatization of full text may be different to lemmatisation of vocabulary term, 
                        # so using set to list unique case variants of either original term text OR lemma 
                        variants = {
                            lemma.upper(), 
                            lemma.lower(), 
                            lemma.title(), 
                            text.upper(), 
                            text.lower(), 
                            text.title()
                        }                        
                        
                        element["LEMMA"] = { "IN": list(variants) }   
                    else:
                        # just match the term, ignore case
                        element["LOWER"] = text.lower()                       
                    
                    # add pos tags restriction if any passed in
                    # note 06/03/2024 - POS (was) only applied to LAST term if multi-word phrase
                    # e.g. { "LEMMA": "board", "POS": { "IN": ["NOUN", "PROPN"] }}
                    # POS now applied ONLY to single terms, NOT to multi-word phrases
                    if (len(pos) > 0 and phrase_length == 1):
                        element["POS"] = { "IN": pos }

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
    