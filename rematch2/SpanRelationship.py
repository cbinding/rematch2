from spacy.tokens import Span
from enum import Enum


class SpanRelationship(Enum):
    BEFORE = "before" 
    AFTER = "after"
    MEETS = "meets"
    MET_BY = "met_by"
    OVERLAPS = "overlaps"
    OVERLAPPED_BY = "overlapped_by"
    STARTS = "starts"
    STARTED_BY = "started_by"
    FINISHES = "finishes"
    FINISHED_BY = "finished_by"
    WITHIN = "within"
    CONTAINS = "contains"
    EQUALS = "equals"
    

def get_span_relationship(spanA: Span, spanB: Span)-> SpanRelationship:
    if span_before(spanA, spanB): 
        rel = SpanRelationship.BEFORE
    elif span_after(spanA, spanB): 
        rel = SpanRelationship.AFTER
    elif span_meets(spanA, spanB):
        rel = SpanRelationship.MEETS
    elif span_met_by(spanA, spanB): 
        rel = SpanRelationship.MET_BY
    elif span_overlaps(spanA, spanB): 
        rel = SpanRelationship.OVERLAPS
    elif span_overlapped_by(spanA, spanB): 
        rel = SpanRelationship.OVERLAPPED_BY
    elif span_starts(spanA, spanB): 
        rel = SpanRelationship.STARTS
    elif span_started_by(spanA, spanB): 
        rel = SpanRelationship.STARTED_BY
    elif span_finishes(spanA, spanB):
        rel = SpanRelationship.FINISHES
    elif span_finished_by(spanA, spanB):
        rel = SpanRelationship.FINISHED_BY
    elif span_within(spanA, spanB): 
        rel =SpanRelationship.WITHIN
    elif span_contains(spanA, spanB): 
        rel = SpanRelationship.CONTAINS
    elif span_equals(spanA, spanB): 
        rel = SpanRelationship.EQUALS
    return rel


# A occurs before B (by character position)
def span_before(spanA: Span, spanB: Span)-> bool:
    return spanA.end_char + 1 < spanB.start_char 

# A occurs after B 
def span_after(spanA: Span, spanB: Span)-> bool:
    return span_before(spanB, spanA)

# A meets B
def span_meets(spanA: Span, spanB: Span)-> bool:
    return spanA.end_char + 1 == spanB.start_char 

# B meets A
def span_met_by(spanA: Span, spanB: Span)-> bool:
    return span_meets(spanB, spanA)

# A overlaps B?
def span_overlaps(spanA: Span, spanB: Span)-> bool:
    return spanA.start_char < spanB.start_char and spanA.end_char > spanB.start_char and spanA.end_char < spanB.end_char

# A overlapped by B?
def span_overlapped_by(spanA: Span, spanB: Span)-> bool:
    return span_overlaps(spanB, spanA)

# A starts B?
def span_starts(spanA: Span, spanB: Span)-> bool:
    return spanA.start_char == spanB.start_char and spanA.end_char < spanB.end_char

# A started by B?
def span_started_by(spanA: Span, spanB: Span)-> bool:
    return span_starts(spanB, spanA)

# A within B?
def span_within(spanA: Span, spanB: Span)-> bool:
    return spanA.start_char > spanB.start_char and spanA.end_char < spanB.end_char

# A contains B?
def span_contains(spanA: Span, spanB: Span)-> bool:
    return span_within(spanB, spanA)

# A finishes B?
def span_finishes(spanA: Span, spanB: Span)-> bool:
    return spanA.start_char > spanB.start_char and spanA.end_char == spanB.end_char

# A finished by B?
def span_finished_by(spanA: Span, spanB: Span)-> bool:
    return span_finishes(spanB, spanA)

# A equals B? 
def span_equals(spanA: Span, spanB: Span)-> bool:
    return spanA.start_char == spanB.start_char and spanA.end_char == spanB.end_char
