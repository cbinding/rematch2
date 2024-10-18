#import spacy       
import spacy
from spacy.tokens import Doc, Span, SpanGroup
from spacy.language import Language


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
def is_contained(index: int, spans: SpanGroup) -> bool:
    span = spans[index]
    #return any([True for i, s in enumerate(spans) if i != index and span.label == s.label and is_within(span, s)])
    # 04/10/24 CFB remove ANY contained spans - e.g. "post" within "post-medieval"
    return any([True for i, s in enumerate(spans) if i != index and is_within(span, s)])
        

# remove spans contained by any other span
@Language.component("child_span_remover")
def child_span_remover(doc: Doc, spans_key: str="rematch") -> Doc:
    spans = doc.spans.get(spans_key, [])    
    doc.spans[spans_key] = [span for index, span in enumerate(spans) if not is_contained(index, spans)]  
    return doc


@Language.component("dummy_span_creator")
def dummy_span_creator(doc: Doc, spans_key: str="rematch") -> Doc:
    x = doc[3:4]
    y = doc[1:4]
    z = doc[4:5]
    doc.spans[spans_key] = [x, y, z]
    return doc

# testing the component
if __name__ == "__main__":
    nlp = spacy.blank("en")
    nlp.add_pipe("dummy_span_creator", last=True)
    nlp.add_pipe("child_span_remover", last=True)
    text = "the quick brown fox jumped over the lazy dog"
    doc = nlp(text)
    spans = doc.spans["rematch"]
    x = spans[0]
    y = spans[1]
    z = spans[2]    
    
    print(f"\"{doc}\"")
    print(f"\"{x}\" is within \"{x}\"? {is_within(x, x)}")   
    print(f"\"{x}\" is within \"{y}\"? {is_within(x, y)}")    
    print(f"\"{x}\" is within \"{z}\"? {is_within(x, z)}")  
    print(f"\"{x}\" is contained? {is_contained(0, spans)}")
    print(f"\"{y}\" is contained? {is_contained(1, spans)}")
    print(f"\"{z}\" is contained? {is_contained(2, spans)}")
    