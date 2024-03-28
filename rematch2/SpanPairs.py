'''
=============================================================================
Package   : 
Module    : SpanPairs.py
Classes   : SpanPairs
Project   : 
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : for use in identifying 'paired' spans
            e.g. "medieval furrow", "iron age barrow", "Roman villa" etc.
Imports   : itertools, Doc, Span, DependencyMatcher
Example   : 
License   : https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History
08/03/2024 CFB Initially created script (split out from find_pairs.py)
=============================================================================
'''
import itertools        # for product
import pandas as pd     # for output to HTML table
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
        rel_ops: list = [ "<", ">", "<<", ">>", ".*", ";", ";*" ], 
        left_types: list = [], 
        right_types: list = []):
  
        self.doc = doc
        self.rel_ops = rel_ops
        self.left_types = list(map(lambda s: s.strip().upper(), left_types or []))
        self.right_types = list(map(lambda s: s.strip().upper(), right_types or []))
        self.pairs = self._get_pairs()


    @staticmethod
    def _filter_spans_by_types(types=[], ents=[]):
        return filter(lambda span: any(span.label_ in t for t in types), ents)      
        

    def _get_noun_chunk_pairs(self) -> list[SpanPair]:
        #matched = dict()
        pairs = []
        for chunk in self.doc.noun_chunks:            

            # get all LEFT spans in the noun chunk
            left_spans = self._filter_spans_by_types(self.left_types, chunk.ents)
            #if self.left_type == "*":   
                #left_ents = filter(lambda ent: ent.label_ != self.left_type, chunk.ents)            
            #else:
                #left_ents = filter(lambda ent: ent.label_ == self.left_type, chunk.ents)

            # get all RIGHT spans in the noun chunk
            right_spans = self._filter_spans_by_types(self.right_types, chunk.ents)
            #if self.right_type == "*":   
                #right_ents = filter(lambda ent: ent.label_ != self.right_type, chunk.ents)            
            #else:
                #right_ents = filter(lambda ent: ent.label_ == self.right_type, chunk.ents)

            # Use cartesian product to give all pair combinations
            for span1, span2 in itertools.product(left_spans, right_spans):
                # using dict to eliminate duplicates with lower scores
                # ensure they are not the same entity before adding  
                if span1.start != span2.start:             
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
        # so label can be seen in pattern below...
        if not Token.has_extension("label"):
            def get_label(token): return token.ent_type_
            Token.set_extension(name="label", getter=get_label)

            def get_labels(token): 
                outer_spans = filter(lambda span: span.start <= token.i and span.end >= token.i, token.doc.spans["custom"])
                return list(set(map(lambda span: span.label, outer_spans)))
            Token.set_extension(name="labels", getter=get_labels)


        pattern = [
            {
                "RIGHT_ID": "left",
                #"RIGHT_ATTRS": {"_": {"label": {"IN": self.left_types}}}
                "RIGHT_ATTRS": {"_": {"labels": {"INTERSECTS": self.left_types}}}
            },
            {
                "LEFT_ID": "left",
                "REL_OP": rel_op,
                "RIGHT_ID": "right",            
                #"RIGHT_ATTRS": {"_": {"label": {"IN": self.right_types}}}
                "RIGHT_ATTRS": {"_": {"labels": {"INTERSECTS": self.right_types}}}
            }
        ]
        matcher = DependencyMatcher(self.doc.vocab)
        #matcher.add(f"{self.left_type}_{self.right_type}", [pattern])
        matcher.add("pair", [pattern])
        matches = matcher(self.doc)

        #matched = dict()
        pairs = []
        for match_id, token_ids in matches:
            # get all LEFT side entities token_ids match
            left_spans = self._filter_spans_by_types(self.left_types, self.doc.spans["custom"])
            left_spans = filter(lambda span: any(span.start <= token_id and span.end > token_id for token_id in token_ids), left_spans)
            
            # get all RIGHT side entities token_ids match
            right_spans = self._filter_spans_by_types(self.right_types, self.doc.spans["custom"])
            right_spans = filter(lambda span: any(span.start <= token_id and span.end > token_id for token_id in token_ids), right_spans)

            '''
            if self.left_type == "*":
                left_ents = filter(lambda ent: ent.label_ != self.left_type and any(
                    ent.start <= id and ent.end > id for id in token_ids), self.doc.ents)
            else:
                left_ents = filter(lambda ent: ent.label_ == self.left_type and any(
                    ent.start <= id and ent.end > id for id in token_ids), self.doc.ents)
            # get all RIGHT side entities token_ids match (allowing * wildcard entity type)
            if self.right_type == "*":
                right_ents = filter(lambda ent: ent.label_ != self.right_type and any(
                    ent.start <= id and ent.end > id for id in token_ids), self.doc.ents)
            else:
                right_ents = filter(lambda ent: ent.label_ == self.right_type and any(
                    ent.start <= id and ent.end > id for id in token_ids), self.doc.ents)
                    '''
            # using cartesian product to give all LEFT - RIGHT pair combinations
            for span1, span2 in itertools.product(left_spans, right_spans):
                # ensure they are not the same entity before adding  
                if span1.start != span2.start:    
                    pair = SpanPair(span1=span1, span2=span2, rel_op=rel_op)
                    pairs.append(pair)
                #id = f"{pair.ent1.id}|{pair.ent2.id}" 
                # using dict to eliminate duplicates with lower scores
                #if (id not in matched or pair.score > matched[id].score):
                    #matched[id] = pair                 
            
        # return list of result items
        #return list(matched.values())
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
            # if they are the same type of entity don't include them as a pair
            if pair.span1.label == pair.span2.label:
                continue

            # if they are actually the same entity don't include them as a pair
            id1 = get_span_id(pair.span1)
            id2 = get_span_id(pair.span2)
            if id1 == id2:
                continue
            
            # add the pair, eliminating any duplicate pairs having lower scores
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


    #TODO - set up stylers/formatters
    def to_html_table(self) -> str:
        data = [{
            "ent1_id": pair.ent1.id_,
            "ent1_type": pair.ent1.label_,
            "ent1_text": pair.ent1.text,
            "rel_op": pair.rel_op,
            "ent2_id": pair.ent2.id_,
            "ent2_type": pair.ent2.label_,
            "ent2_text": pair.ent2.text,
            "score": pair.score
        } for pair in self.pairs]

        pd.set_option('display.max_colwidth', None)
        df = pd.DataFrame(data)
        return df.to_html(border=0)
        
    