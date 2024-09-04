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
Imports   : itertools, Doc, Span, Token, DependencyMatcher
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

if __package__ is None or __package__ == '':
    # uses current directory visibility
    from SpanPair import SpanPair
else:
    # uses current package visibility
    from .SpanPair import SpanPair


class SpanPairs:

    def __init__(self, 
        doc: Doc,
        spans_key: str = "custom", 
        rel_ops: list = [ "<", ">", "<<", ">>", ".", ";", ".*", ";*" ], 
        left_labels: list = [], 
        right_labels: list = []):
  
        self.doc = doc
        self.spans_key = spans_key.strip()
        self.rel_ops = rel_ops
        self.left_labels = list(map(lambda s: s.strip().upper(), left_labels or []))
        self.right_labels = list(map(lambda s: s.strip().upper(), right_labels or []))
        self.pairs = self._get_pairs()


    @staticmethod
    def _filter_spans_by_labels(labels=[], spans=[]):
        return filter(lambda span: any(span.label_ in s for s in labels), spans)      
        

    def _get_noun_chunk_pairs(self) -> list[SpanPair]:
        #matched = dict()
        pairs = []
        all_spans = self.doc.spans.get(self.spans_key, [])
            
        for chunk in self.doc.noun_chunks:  
            # get all spans within the noun chunk        
            spans_in_chunk = filter(lambda span: span.start >= chunk.start and span.end <= chunk.end, all_spans)
            
            # get all LEFT spans within the noun chunk
            left_spans = self._filter_spans_by_labels(self.left_labels, spans_in_chunk)
            
            # get all RIGHT spans within the noun chunk
            right_spans = self._filter_spans_by_labels(self.right_labels, spans_in_chunk)
            
            # Use cartesian product to give all pair combinations
            for span1, span2 in itertools.product(left_spans, right_spans):
                # ensure they are not the same span before adding  
                if span1.orth_ != span2.orth_:             
                    pair = SpanPair(span1=span1, span2=span2, rel_op="-")
                    pairs.append(pair)
                #id = f"{pair.ent1.id}|{pair.ent2.id}" 
                # using dict to eliminate duplicates with lower scores
                #if (id not in matched or pair.score > matched[id].score):
                    #matched[id] = pair 

        # return as array of tuple
        #return list(matched.values())
        return pairs


    def _get_dependency_pairs(self) -> list[SpanPair]:
        results = []
        for rel_op in self.rel_ops:
            results += self._get_dependency_pairs_by_rel_op(rel_op)
        return results


    # Using dependency matcher. Find dependency pairs
    # https://spacy.io/usage/rule-based-matching#dependencymatcher  
    # Allowing * as wildcard for dealing with negation span pairs      
    def _get_dependency_pairs_by_rel_op(self, rel_op: str = "") -> list[SpanPair]:
        
        if not Token.has_extension("labels"):
            Token.set_extension(name="labels", getter=get_labels_for_token)

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
        matcher = DependencyMatcher(self.doc.vocab)
        matcher.add("pair", [pattern])
        matches = matcher(self.doc)

        #matched = dict()
        pairs = []
        all_spans = self.doc.spans.get(self.spans_key, [])

        for match_id, token_ids in matches:
            # get all LEFT side spans token_ids match
            left_spans = self._filter_spans_by_labels(self.left_labels, all_spans)
            left_spans = filter(lambda span: any(span.start <= token_id and span.end > token_id for token_id in token_ids), left_spans)
            
            # get all RIGHT side spans token_ids match
            right_spans = self._filter_spans_by_labels(self.right_labels, all_spans)
            right_spans = filter(lambda span: any(span.start <= token_id and span.end > token_id for token_id in token_ids), right_spans)

            # using cartesian product to give all LEFT - RIGHT pair combinations
            for span1, span2 in itertools.product(left_spans, right_spans):
                # ensure they are not the same span before adding  
                if span1.orth_ != span2.orth_:    
                    pair = SpanPair(span1=span1, span2=span2, rel_op=rel_op)
                    pairs.append(pair)
                
        # return list of result items
        return pairs


    def _get_pairs(self) -> list[SpanPair]:
        dependency_pairs = self._get_dependency_pairs()
        noun_chunk_pairs = self._get_noun_chunk_pairs()
        
        def get_span_id(span):
            # get a suitable identifier
            id=""
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
            
            # add the pair, eliminating any duplicate pairs having lower scores
            id1 = get_span_id(pair.span1)
            id2 = get_span_id(pair.span2)
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
    