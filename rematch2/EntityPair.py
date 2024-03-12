'''
=============================================================================
Package   : 
Module    : EntityPair.py
Classes   : EntityPair
Project   : 
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : for use in identifying 'paired' entities
            e.g. "medieval furrow", "iron age barrow", "Roman villa" etc.
Imports   : Doc, Span
Example   : 
License   : https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History
08/03/2024 CFB Initially created script (split out from find_pairs.py)
=============================================================================
'''
from spacy.tokens import Doc, Span

class EntityPair:
    def __init__(self, ent1: Span = None, ent2: Span = None, rel_op: str = ""):
        self.rel_op = (rel_op or "").strip()
        self.ent1 = ent1
        self.ent2 = ent2
        self.score = self._get_score()
    
    def _get_score(self):
        score = float(0)

        match self.rel_op:
            case "-": score = 1.0   # special case, noun chunk matches
            case "<": score = 0.8   # A is the immediate dependent of B
            case ">": score = 0.8   # A is the immediate head of B
            case "<<": score = 0.6  # A is the dependent in a chain to B following dep → head paths
            case ">>": score = 0.6  # A is the head in a chain to B following head → dep paths
            case ".*": score = 0.2  # A precedes B, i.e. A.i < B.i, and both are within the same dependency tree
            case ";*": score = 0.2  # A follows B, i.e. A.i > B.i, and both are within the same dependency tree
            case _: score = 0.0
        return score

    def __str__(self):
        return "{id_1:<40} [{type_1:<}] {text_1:>20} {rel_op} {text_2:<20} [{type_2:>}] {id_2:<40} ({score})".format(
                score = self.score,
                type_1 = self.ent1.label_,
                type_2 = self.ent2.label_,
                rel_op = self.rel_op,
                id_1 = self.ent1.ent_id_,
                id_2 = self.ent2.ent_id_,                  
                text_1 = f"\"{self.ent1.text}\"",                        
                text_2 = f"\"{self.ent2.text}\""    
            )
    
    def __repr__(self):
        return self.__str__()