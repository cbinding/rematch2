'''
=============================================================================
Package   : rematch2
Module    : SpanPairs.py
Classes   : SpanPairs
Project   : 
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : for use in identifying 'paired' spans
            e.g. "Medieval furrow", "Iron Age barrow", "Roman villa" etc.
Imports   : itertools, Doc, Span, Token, DependencyMatcher, SpanPair
Example   : 
License   : https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History
08/03/2024 CFB Initially created script (split out from find_pairs.py)
=============================================================================
'''
import itertools        # for product
from spacy.tokens import Doc, Span, Token
from spacy.matcher import DependencyMatcher

from rematch2 import DocSummary
from .Decorators import run_timed
from .SpanPair import SpanPair
from .Util import *


class SpanPairs:

    def __init__(self, 
        doc: Doc,
        spans_key: str = DEFAULT_SPANS_KEY, 
        rel_ops: list[str] = [ "<", ">", "<<", ">>", ".", ".*", ";", ";*"], 
        left_labels: list[str] = [], 
        right_labels: list[str] = []):
  
        self.doc = doc
        self.spans_key = spans_key.strip()
        self.rel_ops = rel_ops
        self.left_labels = list(map(lambda s: s.strip().upper(), left_labels or []))
        self.right_labels = list(map(lambda s: s.strip().upper(), right_labels or []))
        self.pairs = self._get_pairs()


    @staticmethod
    def _filter_spans_by_labels(labels: list[str]=[], spans: list[Span]=[]) -> list[Span]:
        return list(filter(lambda span: any(span.label_ in s for s in labels), spans))

    # Using noun chunks to find pairs of spans
    @run_timed
    def _get_noun_chunk_pairs(self) -> list[SpanPair]:
        
        pairs = []
        all_spans = self.doc.spans.get(self.spans_key, [])
            
        for chunk in self.doc.noun_chunks:  
            # get all identified spans within this noun chunk        
            spans_in_chunk = filter(lambda span: span.start >= chunk.start and span.end <= chunk.end, all_spans)
            
            # get all LEFT spans within this noun chunk
            left_spans = self._filter_spans_by_labels(self.left_labels, spans_in_chunk)
            
            # get all RIGHT spans within this noun chunk
            right_spans = self._filter_spans_by_labels(self.right_labels, spans_in_chunk)
            
            # Use cartesian product to give all left/right pair combinations
            for span1, span2 in itertools.product(left_spans, right_spans):
                # ensure they are not the same span before adding  
                if span1.orth_ != span2.orth_:             
                    pair = SpanPair(span1=span1, span2=span2, rel_op="-")
                    pairs.append(pair)
                
        return pairs


    # Using dependency matcher. Find dependency pairs
    # https://spacy.io/usage/rule-based-matching#dependencymatcher  
    # Allowing * as wildcard for dealing with negation span pairs 
    @run_timed
    def _get_dependency_pairs(self) -> list[SpanPair]:
        pairs = []
        all_spans = self.doc.spans.get(self.spans_key, [])
        left_spans = self._filter_spans_by_labels(self.left_labels, all_spans)
        right_spans = self._filter_spans_by_labels(self.right_labels, all_spans) 

        if not Token.has_extension("labels"):
            Token.set_extension(name="labels", getter=get_labels_for_token)
        
        matcher = DependencyMatcher(self.doc.vocab)        
        
        for rel_op in self.rel_ops:
            pattern = [
                {
                    "RIGHT_ID": "left",
                    "RIGHT_ATTRS": {"_": {"labels": {"INTERSECTS": self.left_labels}}}
                },
                {
                    "LEFT_ID": "left",
                    "REL_OP": rel_op, 
                    "RIGHT_ID": "right",
                    "RIGHT_ATTRS": {"_": {"labels": {"INTERSECTS": self.right_labels}}}
                }
           ]
            matcher.add(f"pair_{rel_op}", [pattern])
        
        matches = matcher(self.doc)

        # matches is a list of tuples (match_id, token_ids)
        # where match_id is a string like "pair_>" and token_ids is a list
        # of token IDs that match the pattern.
        # e.g. [(match_id, [token_id1, token_id2, ...]), ...]
        for match_id, token_ids in matches:
            match_label = self.doc.vocab.strings[match_id]  # e.g., "pair_>"
            rel_op = match_label.split("_", 1)[1]           # get the REL_OP part
    
            # get all LEFT side spans token_ids match
            left_side = filter(lambda span: any(span.start <= token_id and span.end > token_id for token_id in token_ids), left_spans)
            
            # get all RIGHT side spans token_ids match
            right_side = filter(lambda span: any(span.start <= token_id and span.end > token_id for token_id in token_ids), right_spans)

            # using cartesian product to give all LEFT - RIGHT pair combinations
            for span1, span2 in itertools.product(left_side, right_side):
                # ensure they are not the same span before adding
                if span1.orth_ != span2.orth_:
                    pair = SpanPair(span1=span1, span2=span2, rel_op=rel_op)
                    pairs.append(pair)
                
        # return list of result items
        return pairs

    @run_timed
    def _get_dependency_pairs2(self) -> list[SpanPair]:
        pairs = []
        all_spans = self.doc.spans.get(self.spans_key, [])
        left_spans = self._filter_spans_by_labels(self.left_labels, all_spans)
        right_spans = self._filter_spans_by_labels(self.right_labels, all_spans) 

        if not Token.has_extension("labels"):
            Token.set_extension(name="labels", getter=get_labels_for_token)
        
        matcher = DependencyMatcher(self.doc.vocab)

        for rel_op in self.rel_ops:
            pattern = [
                {
                    "RIGHT_ID": "left",
                    "RIGHT_ATTRS": {"_": {"labels": {"INTERSECTS": self.left_labels}}}
                },
                {
                    "LEFT_ID": "left",
                    "REL_OP": rel_op, 
                    "RIGHT_ID": "right",
                    "RIGHT_ATTRS": {"_": {"labels": {"INTERSECTS": self.right_labels}}}
                }
            ]
            matcher.add(f"pair_{rel_op}", [pattern])

        matches = matcher(self.doc)

        # Build token-to-span index for fast lookup
        from collections import defaultdict
        left_token_to_spans = defaultdict(list)
        for span in left_spans:
            for i in range(span.start, span.end):
                left_token_to_spans[i].append(span)
        right_token_to_spans = defaultdict(list)
        for span in right_spans:
            for i in range(span.start, span.end):
                right_token_to_spans[i].append(span)

        for match_id, token_ids in matches:
            match_label = self.doc.vocab.strings[match_id]
            rel_op = match_label.split("_", 1)[1]
            left_candidates = set()
            right_candidates = set()
            for tid in token_ids:
                left_candidates.update(left_token_to_spans.get(tid, []))
                right_candidates.update(right_token_to_spans.get(tid, []))
            for span1, span2 in itertools.product(left_candidates, right_candidates):
                if span1.orth_ != span2.orth_:
                    pair = SpanPair(span1=span1, span2=span2, rel_op=rel_op)
                    pairs.append(pair)
        return pairs
    

    @run_timed
    def _get_pairs(self) -> list[SpanPair]:
        dependency_pairs = self._get_dependency_pairs2()
        noun_chunk_pairs = self._get_noun_chunk_pairs()
        
        def get_span_id(span):
            # get a suitable identifier
            id = ""
            if span.id_:
                id = span.id_
            elif span.ent_id_:
                id = span.ent_id_
            elif span.lemma_:
                id = span.lemma_
            elif span.text:
                id = span.text
            else:
                id = "other"
            return id

        best_scoring_pairs = {}
        for pair in noun_chunk_pairs + dependency_pairs:            
            # if they have the same label don't include them as a pair
            if pair.span1.label == pair.span2.label:
                continue
            
            # get identifier for each span
            id1 = get_span_id(pair.span1)
            id2 = get_span_id(pair.span2)

            # if they have the same id don't include them as a pair
            if id1 == id2:
                continue

            # add the pair, overriding any pair having same id but lower score            
            id = f"{id1}|{id2}"
            if (id not in best_scoring_pairs or pair.score > best_scoring_pairs[id].score):
                best_scoring_pairs[id] = pair
        
        # finally, sort best_scoring_pairs by ascending score and return them
        best_pairs = list(best_scoring_pairs.values())
        return sorted(best_pairs, key=lambda x: x.score, reverse=True)


    def __str__(self):
        result = ""
        for pair in self.pairs:
            result += f"{str(pair)}\n"
            
        return result


    def __repr__(self):
        return self.__str__()
    
# testing the component: python -m rematch2.SpanPairs
if __name__ == "__main__":
    nlp = get_pipeline_for_language("en")
    nlp.add_pipe("fish_monument_types_ruler", last=True )
    nlp.add_pipe("periodo_ruler", last=True, config={"periodo_authority_id": "p0kh9ds"})
    rel_ops =[ "<", ">", "<<", ">>", ".", ";"]
    left_labels: list=["PERIOD", "YEARSPAN"] 
    right_labels: list=["FISH_OBJECT", "FISH_MONUMENT"]       
    text = "the medieval barrow and trench and the iron age farm is bronze age and are both interesting"
    doc = nlp(text)
    summary = DocSummary(doc=doc, spans_key=DEFAULT_SPANS_KEY)
    pairs = SpanPairs(doc=doc, rel_ops=rel_ops, left_labels=left_labels, right_labels=right_labels).pairs
    print(summary.spans_to_text())
    print(summary.spanpairs_to_text(pairs))