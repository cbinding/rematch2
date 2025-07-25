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

from .Decorators import run_timed
from .SpanPair import SpanPair
from .Util import *


class SpanPairs:

    def __init__(self, 
        doc: Doc,
        spans_key: str = DEFAULT_SPANS_KEY, 
        rel_ops: list[str] = [ "<", ">", ".", ";"], 
        left_labels: list[str] = [], 
        right_labels: list[str] = []):
  
        self.doc = doc
        self.spans_key = spans_key.strip()
        self.rel_ops = rel_ops
        self.left_labels = list(map(lambda s: s.strip().upper(), left_labels or []))
        self.right_labels = list(map(lambda s: s.strip().upper(), right_labels or []))
        self.pairs = self._get_all_pairs()


    @staticmethod
    def _filter_spans_by_labels(labels: list[str]=[], spans: list[Span]=[]) -> list[Span]:
        filtered = list(filter(lambda span: span.label_ in labels, spans))
        return filtered

    # Using noun chunks to find pairs of spans
    @run_timed
    def _get_noun_chunk_pairs(self) -> list[SpanPair]:

        pairs = []
        all_spans = self.doc.spans.get(self.spans_key, [])
        for chunk in self.doc.noun_chunks:
            
            # get all identified spans within this noun chunk        
            spans_in_chunk = list(filter(lambda span: span.start >= chunk.start and span.end <= chunk.end, all_spans))
            
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
    def _get_all_pairs(self) -> list[SpanPair]:
        dependency_pairs = self._get_dependency_pairs()
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
    from .DocSummary import DocSummary

    nlp = get_pipeline_for_language("en")
    nlp.add_pipe("fish_monument_types_ruler", last=True )
    nlp.add_pipe("periodo_ruler", last=True, config={"periodo_authority_id": "p0kh9ds"})
    rel_ops =[ "<", ">", ".", ";"]
    left_labels: list=["PERIOD", "YEARSPAN"] 
    right_labels: list=["FISH_OBJECT", "FISH_MONUMENT"]       
    text = "the medieval barrow and trench and the iron age farm is bronze age and are both interesting"
    text ="An archaeological trench evaluation was undertaken by AC archaeology during July 2023 on land at Hartnoll Farm, Tiverton, Devon (centred on NGR SS 9898 1288) . The evaluation comprised the machine excavation of 33 trenches totaling 1640m in length with each trench 1.8m wide. Trenches were positioned to target anomalies identified by a previous geophysical survey, as well as in what were thought to be blank areas. The site is located where previous investigations nearby had identified evidence for late prehistoric settlement, funerary and agricultural occupation. The main archaeological features identified during the present work were comparable to previous results and comprised two probable cremation pits representing potential evidence for an Early Bronze Age flat cemetery in the southwest part of the site, as well as part of a ring ditch of a probable ploughed - down former barrow to the southeast. Adjacent to this was a linear ditch likely to be part of a wider pattern of early field division. Elsewhere across the site mainly former ditches were present, with the majority of these of post medieval / modern date and related to agricultural field division and drainage"
    doc = nlp(text)
    summary = DocSummary(doc=doc, spans_key=DEFAULT_SPANS_KEY)
    pairs = SpanPairs(doc=doc, rel_ops=rel_ops, left_labels=left_labels, right_labels=right_labels).pairs
    print(summary.spans_to_text())
    print(summary.span_pairs_to_text(pairs))