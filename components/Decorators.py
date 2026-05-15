"""
=============================================================================
Package   : any
Module    : decorators.py
Classes   : 
Project   : any
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : custom decorators:
            run_timed - decorator for reporting function execution time
Imports   : functools, datetime
Example   : 
    from decorators import run_timed
    @run_timed
    my_function()
License   : https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History
21/02/2024 CFB Initially created script
22/05/2025 CFB using time lib instead of datetime
=============================================================================
"""
import functools
import time # For measuring elapsed time

# custom decorator to output execution timing information
# based on https://realpython.com/primer-on-python-decorators/
def run_timed(f):
    @functools.wraps(f)
    def wrapper_run_timed(*args, **kwargs):
        starting = time.time()
       
        result = f(*args, **kwargs)
        
        finished = time.time()      
        duration = finished - starting 

        print(f"\"{f.__name__ }\" ran in {duration:.3f} seconds")

        return result

    return wrapper_run_timed