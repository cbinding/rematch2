"""
=============================================================================
Package   : rematch2
Module    : SpanRemover.py
Classes   : Stop_listSpanRemover, child_span_remover
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Project   : 
Summary   : Remove particular spans from output
Imports   : 
Example   : nlp.add_pipe("stop_list_span_remover", last=True, config={"stop_list": ["12345"]})            
License   : https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History
07/01/2024 CFB Initially created script
=============================================================================
"""

#import spacy       
import spacy
from spacy.tokens import Doc, Span, SpanGroup
from spacy.language import Language


# A equals B (position-wise)
def span_equals(spanA: Span, spanB: Span)-> bool:
    return spanA.start_char == spanB.start_char and spanA.end_char == spanB.end_char


# A starts B?
def span_starts(spanA: Span, spanB: Span)-> bool:
    return spanA.start_char == spanB.start_char and spanA.end_char < spanB.end_char


# A finishes B?
def span_finishes(spanA: Span, spanB: Span)-> bool:
    return spanA.start_char > spanB.start_char and spanA.end_char == spanB.end_char


# A within B?
def span_within(spanA: Span, spanB: Span)-> bool:
    return spanA.start_char > spanB.start_char and spanA.end_char < spanB.end_char


# A starts|finishes|within B?
def is_within(spanA: Span, spanB: Span)-> bool:
    return span_starts(spanA, spanB) or span_finishes(spanA, spanB) or span_within(spanA, spanB)
    

# is span 'contained' by any other span in the list and not equal start & end
def is_contained(index: int, spans: SpanGroup|list[Span]) -> bool:
    span = spans[index]
    #return any([True for i, s in enumerate(spans) if i != index and span.label == s.label and is_within(span, s)])
    # 04/10/24 CFB remove ANY contained spans - e.g. "post" within "post-medieval"
    return any([True for i, s in enumerate(spans) if i != index and is_within(span, s)])
    

# remove matched spans "contained" by any other matched spans
# e.g. "post" within "post-medieval"
@Language.component("child_span_remover")
def child_span_remover(doc: Doc, spans_key: str="rematch") -> Doc:
    spans = doc.spans.get(spans_key, [])    
    doc.spans[spans_key] = [span for index, span in enumerate(spans) if not is_contained(index, spans)]  
    return doc


# remove matched spans where the ID is in a stop list of IDs not to be matched
# e.g. "coin" matched on both "coin" and "coin (forgery)" - ID of "coin (forgery)" can be on the stop list
# TODO: not yet tested..
class Stop_listSpanRemover:
    def __init__(self, spans_key: str="rematch", stop_list: list=[]):
        self.spans_key = spans_key
        self.stop_list = stop_list        

    def __call__(self, doc: Doc) -> Doc:
        spans = doc.spans.get(self.spans_key, [])  

        def in_stop_list(span):
            if span.id_ in self.stop_list: 
                return True
            elif span.text.lower().strip() in (s.lower().strip() for s in self.stop_list): 
                return True
            else:
                return False
        
        doc.spans[self.spans_key] = [span for index, span in enumerate(spans) if not in_stop_list(span)] 
        return doc


@Language.factory(name="stop_list_span_remover", default_config={"spans_key": "rematch", "stop_list": []})
def stop_list_span_remover(nlp: Language, name: str="periodo_ruler", spans_key: str="rematch", stop_list: list=[]):
    return Stop_listSpanRemover(spans_key=spans_key, stop_list=stop_list)


# for the testing below
@Language.component("dummy_span_creator")
def dummy_span_creator(doc: Doc, spans_key: str="rematch") -> Doc:
    x = doc[3:4] # "fox"
    y = doc[1:4] # "quick brown fox"
    z = doc[4:5] # "jumps"
    a = doc[10:11]
    doc.spans[spans_key] = [x, y, z, a]    
    return doc

# testing the component
if __name__ == "__main__":
    nlp = spacy.blank("en")
    nlp.add_pipe("dummy_span_creator", last=True)
    #nlp.add_pipe("child_span_remover", last=True)
    nlp.add_pipe("stop_list_span_remover", last=True, config={"stop_list": ["eric"]})
    text = "the quick brown fox jumps over the lazy dog called Eric"
    doc = nlp(text)
    spans = doc.spans["rematch"]       
    x = spans[0]
    y = spans[1]
    z = spans[2]    
    
    print(f"\"{doc}\"")
    print(spans)
    print(f"\"{x}\" is within \"{x}\"? {is_within(x, x)}")   
    print(f"\"{x}\" is within \"{y}\"? {is_within(x, y)}")    
    print(f"\"{x}\" is within \"{z}\"? {is_within(x, z)}")  
    print(f"\"{x}\" is contained? {is_contained(0, spans)}")
    print(f"\"{y}\" is contained? {is_contained(1, spans)}")
    print(f"\"{z}\" is contained? {is_contained(2, spans)}")
    