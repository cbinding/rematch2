from spacy.tokens import Doc
from spacy.pipeline import SpanRuler
import functools
import time


def run_timed(f):
    @functools.wraps(f)
    def wrapper_run_timed(self, *args, **kwargs):
        starting = time.time()
       
        result = f(self, *args, **kwargs)
        
        finished = time.time()      
        duration = finished - starting 

        print(f"\"{self.__class__.__name__}.{f.__name__ }\" ran in {duration:.3f} seconds")
        
        return result
    return wrapper_run_timed


class CustomSpanRuler(SpanRuler):
    
    @run_timed
    def __call__(self, doc: Doc) -> Doc:
        print(f"{self.name}")
        return SpanRuler.__call__(self, doc)      

