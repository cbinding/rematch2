import spacy
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


# get list of labels for any spans this token is within
def get_labels_for_token(tok: Token, spans_key: str=DEFAULT_SPANS_KEY) -> list: 
    outer_spans = filter(lambda span: span.start <= tok.i and span.end >= tok.i, tok.doc.spans.get(spans_key,[]))
    return list(set(map(lambda span: span.label, outer_spans)))

