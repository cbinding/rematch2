from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Metadata:
    filename: str
    pipeline: Optional[list[str]] = None


@dataclass(frozen=True)
class Token:
    start: int
    end: int
    text: str
    lemma: Optional[str] = None
    pos: Optional[str] = None


@dataclass(frozen=True)
class Section:
    type: str
    text: str
    start: int
    end: int   


@dataclass(frozen=True)
class Span:
    start: int
    end: int
    text: str
    label: Optional[str] = None
    token_start: Optional[int] = None
    token_end: Optional[int] = None


@dataclass(frozen=True)
class SpanPair:
    span1_id: str
    span1_label: str
    span1_text: str
    span2_id: str
    span2_label: str
    span2_text: str
    rel_op: str
    score: Optional[float] = None
    score_explain: Optional[str] = None


@dataclass(frozen=True)
class Report:
    meta: Metadata
    text: str
    text_normalized: Optional[str] = None
    sections: Optional[list[Section]] = None
    spans: Optional[list[Span]] = None
    tokens: Optional[list[Token]] = None  
    span_pairs: Optional[list[SpanPair]] = None  



