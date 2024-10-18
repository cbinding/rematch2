import spacy
from rematch2.YearSpanRuler import *
from rematch2.VocabularyRuler import *
from spacy.tokens import Span, Token
#from spacy.matcher import Matcher
#from spacy.tokens import SpanGroup
from Util import *
from spacy import displacy

# determine whether a token is within a previously labelled span
def is_token_within_labelled_span(tok: Token, label: str="DATEPREFIX", spans_key: str="rematch"):
    # list any previously identified spans with this label in the document
    spans = list(filter(lambda span: span.label_ == label, tok.doc.spans[spans_key]))
    # is this token inside any of them?
    return any(span.start <= tok.i and span.end > tok.i for span in spans)   

def is_dateprefix(tok):
    return is_token_within_labelled_span(tok, "DATEPREFIX")

def is_datesuffix(tok):
    return is_token_within_labelled_span(tok, "DATESUFFIX")

def is_object(tok):
    return is_token_within_labelled_span(tok, "FISH_OBJECT")
    
Token.set_extension(name="is_dateprefix", getter=is_dateprefix, force=True)
Token.set_extension(name="is_datesuffix", getter=is_datesuffix, force=True)
Token.set_extension(name="is_object", getter=is_object, force=True)

nlp = get_pipeline_for_language("en")

#nlp.add_pipe("yearspan_ruler", last=True)
nlp.add_pipe("aat_activities_ruler", last=True)
nlp.add_pipe("fish_archobjects_ruler", last=True)
nlp.add_pipe("aat_materials_ruler", last=True)

text = "During the burial ground survey, evidence of a late Roman fort was located near the earlier Neolithic flint knapping site. Fragments of a roofing nail were found."

doc = nlp(text.lower())

options = {
    "spans_key": "rematch",
    "colors": {
        "DATEPREFIX": "lightgray",
        "FISH_OBJECT": "plum", 
        "PERIOD": "yellow",
        "FISH_ACTIVITY": "lightpink",
        "FISH_MATERIAL": "antiquewhite"
    }
}
print([(span.text, span.label_) for span in doc.spans["rematch"]])
displacy.serve(doc, style="span", options=options, auto_select_port=True)