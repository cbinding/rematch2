'''
=============================================================================
Package   : 
Module    : SpanPair.py
Classes   : SpanPair
Project   : 
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : for use in identifying 'paired' spans
            e.g. "medieval furrow", "iron age barrow", "Roman villa" etc.
Imports   : Span
Example   : 
License   : https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History
08/03/2024 CFB Initially created script (split out from find_pairs.py)
=============================================================================
'''
from spacy.tokens import Span


class SpanPair:
    
    def __init__(self, span1: Span, span2: Span, rel_op: str = ""):
        self.rel_op = (rel_op or "").strip()
        self.span1 = span1
        self.span2 = span2
        self.score = self._get_score()
    

    def _get_score(self):
        score = float(0)

        match self.rel_op:
            case "-": score = 1.0   # special case, for noun chunk matches
            case "<": score = 0.8   # A is the immediate dependent of B
            case ">": score = 0.8   # A is the immediate head of B
            case "<<": score = 0.6  # A is the dependent in a chain to B following dep → head paths
            case ">>": score = 0.6  # A is the head in a chain to B following head → dep paths
            case ".": score = 0.4  # A immediately precedes B, i.e. A.i == B.i -1, and both are within the same dependency tree
            case ";": score = 0.4  # A immediately follows B, i.e. A.i == B.i + 1, and both are within the same dependency tree
            case ".*": score = 0.2  # A precedes B, i.e. A.i < B.i, and both are within the same dependency tree
            case ";*": score = 0.2  # A follows B, i.e. A.i > B.i, and both are within the same dependency tree
            case _: score = 0.0
        return score


    def __str__(self):
        return "{id_1:<40} [{label_1:<}] {text_1:>20} {rel_op} {text_2:<20} [{label_2:>}] {id_2:<40} ({score})".format(
                score = self.score,
                label_1 = self.span1.label_,
                label_2 = self.span2.label_,
                rel_op = self.rel_op,
                id_1 = self.span1.id_,
                id_2 = self.span2.id_,                  
                text_1 = f"\"{self.span1.text}\"",                        
                text_2 = f"\"{self.span2.text}\""    
            )
    
    
    def __repr__(self):
        return self.__str__()