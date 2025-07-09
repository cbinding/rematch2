import spacy
import json
import re
import functools
import time # For measuring elapsed time
from spacy.language import Language
from spacy.tokens import Token

DEFAULT_SPANS_KEY = "rematch" # default key for storing spans in Doc.spans

# get suitable spaCy NLP pipeline for given ISO639-1 (2-char) language code
def get_pipeline_for_language(language: str="") -> Language:
    pipe_name = ""
    match language.strip().lower()[:2]:
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

# determine whether a token is within a previously labelled span
def is_token_within_labelled_span(tok: Token, label: str="DATEPREFIX", spans_key: str=DEFAULT_SPANS_KEY) -> bool:
    # list any previously identified spans with this label in the document
    
    spans = list(filter(lambda span: span.label_ == label, tok.doc.spans.get(spans_key, [])))
    # is this token inside any of them?
    return any(span.start <= tok.i and span.end > tok.i for span in spans) 


# get list of labels for any spans this token is within
def get_labels_for_token(tok: Token, spans_key: str=DEFAULT_SPANS_KEY) -> list: 
    outer_spans = filter(lambda span: span.start <= tok.i and span.end >= tok.i, tok.doc.spans.get(spans_key,[]))
    return list(set(map(lambda span: span.label, outer_spans)))


def is_dateprefix(tok: Token) -> bool: return is_token_within_labelled_span(tok, "DATEPREFIX")        
def is_datesuffix(tok: Token) -> bool: return is_token_within_labelled_span(tok, "DATESUFFIX")
def is_dateseparator(tok: Token) -> bool: return is_token_within_labelled_span(tok, "DATESEPARATOR")
def is_ordinal(tok: Token) -> bool: return is_token_within_labelled_span(tok, "ORDINAL")
def is_monthname(tok: Token) -> bool: return is_token_within_labelled_span(tok, "MONTHNAME")
def is_seasonname(tok: Token) -> bool: return is_token_within_labelled_span(tok, "SEASONNAME")
