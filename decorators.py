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
=============================================================================
"""
import functools
from datetime import datetime as DT # For measuring elapsed time

# custom decorator to output execution timing information
# see https://realpython.com/primer-on-python-decorators/
def run_timed(func):
    @functools.wraps(func)
    def wrapper_run_timed(*args, **kwargs):
        dt_start = DT.now()
        print(f"\"{func.__name__}\" started: {dt_start.strftime('%Y-%m-%dT%H:%M:%S')}")
        
        result = func(*args, **kwargs)
        
        dt_end = DT.now()
        print(f"\"{func.__name__}\" finished: {dt_start.strftime('%Y-%m-%dT%H:%M:%S')}")
        
        duration = dt_end - dt_start
        print(f"\"{func.__name__}\" duration: {duration}")
        
        return result

    return wrapper_run_timed