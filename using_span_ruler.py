import spacy
from rematch2 import DayNameRuler2
from spacy.tokens import Span, Token
#from spacy.matcher import Matcher
#from spacy.tokens import SpanGroup
from Util import *
from spacy import displacy

# determine whether a token is within a previously labelled span
def is_token_within_labelled_span(tok: Token, label: str="DATEPREFIX", spans_key: str="custom"):
    # list any previously identified spans with this label in the document
    spans = list(filter(lambda span: span.label_ == label, tok.doc.spans[spans_key]))
    # is this token inside any of them?
    return any(span.start <= tok.i and span.end >= tok.i for span in spans)   

def is_dateprefix(tok):
    return is_token_within_labelled_span(tok, "DATEPREFIX")

def is_datesuffix(tok):
    return is_token_within_labelled_span(tok, "DATESUFFIX")

def is_object(tok):
    return is_token_within_labelled_span(tok, "OBJECT")
    
Token.set_extension(name="is_dateprefix", getter=is_dateprefix, force=True)
Token.set_extension(name="is_datesuffix", getter=is_datesuffix, force=True)
Token.set_extension(name="is_object", getter=is_object, force=True)

nlp = get_pipeline_for_language("en")

#config = {"spans_key": "custom", "annotate_ents": False, "overwrite": True}
#ruler = nlp.add_pipe("span_ruler", config=config)
#ruler = nlp.add_pipe("dayname_ruler2", config=config)
'''
config = {
   "spans_key": "custom",
   "validate": False,
   "overwrite": False
}

dateprefix_ruler = nlp.add_pipe("span_ruler", name="dateprefix_ruler", config=config, last=True)
dateprefix_ruler.add_patterns([
    {"label": "DATEPREFIX", "pattern": [{"LOWER": {"REGEX": "earl(ier|y)"}}]},
    {"label": "DATEPREFIX", "pattern": [{"LOWER": "lower"}]},
    {"label": "DATEPREFIX", "pattern": [{"LOWER": {"REGEX": "^mid(dle)?$"}}]},
    {"label": "DATEPREFIX", "pattern": [{"LOWER": {"REGEX": "^later?$"}}]},
    {"label": "DATEPREFIX", "pattern": [{"LOWER": "upper"}]} 
])

object_ruler = nlp.add_pipe("span_ruler", name="object_ruler", config=config, last=True)
object_ruler.add_patterns([
    {"label": "OBJECT", "pattern": [{"LOWER": "flint"}]},
    {"label": "OBJECT", "pattern": [{"LOWER": "roofing"}, {"LOWER": "nail"}]}, 
    {"label": "OBJECT", "pattern": [{"LOWER": "nail"}]}, 
    {"label": "OBJECT", "pattern": [{"LOWER": "roman"}, {"LOWER": "fort"}]},
    {"label": "OBJECT", "pattern": [{"LOWER": "fort"}]}, 
    {"label": "OBJECT", "pattern": [{"LOWER": "burial"}]},
    {"label": "OBJECT", "pattern": [{"LOWER": "burial"}, {"LOWER": "ground"}]},
    {"label": "OBJECT", "pattern": [{"LOWER": "flint"}, {"LOWER": "knapping"}, {"LOWER": "site"}]},
    {"label": "OBJECT", "pattern": [{"LOWER": "site"}]}
])

activity_ruler = nlp.add_pipe("span_ruler", name="activity_ruler", config=config, last=True)
activity_ruler.add_patterns([
    {"label": "ACTIVITY", "pattern": [{"LOWER": "survey"}]},
    {"label": "ACTIVITY", "pattern": [{"LOWER": "roofing"}]}, 
    {"label": "ACTIVITY", "pattern": [{"LOWER": "knapping"}]},
    {"label": "ACTIVITY", "pattern": [{"LOWER": "burial"}]},
    {"label": "ACTIVITY", "pattern": [{"LOWER": "flint"}, {"LOWER": "knapping"}]},
    {"label": "ACTIVITY", "pattern": [{"LOWER": "ground"}, {"LOWER": "survey"}]},
    {"label": "ACTIVITY", "pattern": [{"LOWER": "burial"}, {"LOWER": "ground"}, {"LOWER": "survey"}]}
])

period_ruler = nlp.add_pipe("span_ruler", name="period_ruler", config=config, last=True)
period_ruler.add_patterns([
    {"label": "PERIOD", "pattern": [{"OP": "*", "_": {"is_dateprefix": True}}, {"LOWER": "roman"}]}, 
    {"label": "PERIOD", "pattern": [{"OP": "*", "_": {"is_dateprefix": True}}, {"LOWER": "neolithic"}]}
])

material_ruler = nlp.add_pipe("span_ruler", name="material_ruler", config=config, last=True)
material_ruler.add_patterns([
    {"label": "MATERIAL", "pattern": [{"LOWER": "flint"}]}
])
'''
nlp.add_pipe("fish_archobjects_ruler", last=True)

text = "During the burial ground survey, evidence of a late Roman fort was located near the earlier Neolithic flint knapping site. Fragments of a roofing nail were found."

doc = nlp(text.lower())

options = {
    "spans_key": "custom",
    "colors": {
        "DATEPREFIX": "lightgray",
        "OBJECT": "plum", 
        "PERIOD": "yellow",
        "ACTIVITY": "lightpink",
        "MATERIAL": "antiquewhite"
    }
}
print([(span.text, span.label_) for span in doc.spans["custom"]])
displacy.serve(doc, style="span", options=options, auto_select_port=True)