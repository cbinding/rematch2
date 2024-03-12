'''
=============================================================================
Package   : 
Module    : EntityPairs.py
Classes   : EntityPairs
Project   : 
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : for use in identifying 'paired' entities
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
from spacy.tokens import Doc, Span
from spacy.matcher import DependencyMatcher

if __package__ is None or __package__ == '':
    # uses current directory visibility
    from EntityPair import EntityPair
else:
    # uses current package visibility
    from .EntityPair import EntityPair


class EntityPairs:

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
    def _filter_ents_by_types(ent_types=[], ents=[]):
        return filter(lambda ent: any(ent.label_ in x for x in ent_types), ents)      
        

    def _get_noun_chunk_pairs(self) -> list[EntityPair]:
        #matched = dict()
        pairs = []
        for chunk in self.doc.noun_chunks:            

            # get all LEFT entities in the noun chunk
            left_ents = self._filter_ents_by_types(self.left_types, chunk.ents)
            #if self.left_type == "*":   
                #left_ents = filter(lambda ent: ent.label_ != self.left_type, chunk.ents)            
            #else:
                #left_ents = filter(lambda ent: ent.label_ == self.left_type, chunk.ents)

            # get all RIGHT entities in the noun chunk
            right_ents = self._filter_ents_by_types(self.right_types, chunk.ents)
            #if self.right_type == "*":   
                #right_ents = filter(lambda ent: ent.label_ != self.right_type, chunk.ents)            
            #else:
                #right_ents = filter(lambda ent: ent.label_ == self.right_type, chunk.ents)

            # Use cartesian product to give all pair combinations
            for ent1, ent2 in itertools.product(left_ents, right_ents):
                # using dict to eliminate duplicates with lower scores
                # ensure they are not the same entity before adding  
                if ent1.start != ent2.start:             
                    pair = EntityPair(ent1=ent1, ent2=ent2, rel_op="-")
                    pairs.append(pair)
                #id = f"{pair.ent1.id}|{pair.ent2.id}" 
                # using dict to eliminate duplicates with lower scores
                #if (id not in matched or pair.score > matched[id].score):
                    #matched[id] = pair 

        # return as array of tuple
        #return list(matched.values())
        return pairs


    def _get_dependency_pairs(self) -> list[EntityPair]:
        results = []
        for rel_op in self.rel_ops:
            results += self._get_dependency_pairs_by_rel_op(rel_op)
        return results


    # Using dependency matcher. Find dependency pairs
    # https://spacy.io/usage/rule-based-matching#dependencymatcher  
    # ALlowing * as wildcard for dealing with negation entity pairs      
    def _get_dependency_pairs_by_rel_op(self, rel_op: str = "") -> list[EntityPair]:
             
        pattern = [
            {
                "RIGHT_ID": "left",
                "RIGHT_ATTRS": {"ENT_TYPE": {"IN": self.left_types}} 
            },
            {
                "LEFT_ID": "left",
                "REL_OP": rel_op,
                "RIGHT_ID": "right",            
                "RIGHT_ATTRS": {"ENT_TYPE": {"IN": self.right_types}} 
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
            left_ents = self._filter_ents_by_types(self.left_types, self.doc.ents)
            left_ents = filter(lambda ent: any(ent.start <= token_id and ent.end > token_id for token_id in token_ids), left_ents)
            
            # get all RIGHT side entities token_ids match
            right_ents = self._filter_ents_by_types(self.right_types, self.doc.ents)
            right_ents = filter(lambda ent: any(ent.start <= token_id and ent.end > token_id for token_id in token_ids), right_ents)

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
            for ent1, ent2 in itertools.product(left_ents, right_ents):
                # ensure they are not the same entity before adding  
                if ent1.start != ent2.start:    
                    pair = EntityPair(ent1=ent1, ent2=ent2, rel_op=rel_op)
                    pairs.append(pair)
                #id = f"{pair.ent1.id}|{pair.ent2.id}" 
                # using dict to eliminate duplicates with lower scores
                #if (id not in matched or pair.score > matched[id].score):
                    #matched[id] = pair                 
            
        # return list of result items
        #return list(matched.values())
        return pairs


    def _get_pairs(self) -> list[EntityPair]:
        dependency_pairs = self._get_dependency_pairs()
        noun_chunk_pairs = self._get_noun_chunk_pairs()
        
        best_scoring_pairs = {}
        for pair in noun_chunk_pairs + dependency_pairs:
            # if they are the same type of entity don't include them as a pair
            if pair.ent1.label == pair.ent2.label:
                continue

            # if they are actually the same entity don't include them as a pair
            id1 = pair.ent1.ent_id_ if pair.ent1.ent_id_ != "" else pair.ent1.lemma_
            id2 = pair.ent2.ent_id_ if pair.ent2.ent_id_ != "" else pair.ent2.lemma_
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
        
    