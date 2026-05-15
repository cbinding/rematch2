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


# custom decorator to call function once, return same result on subsequent calls
# (for use with e.g. expensive setup functions that only need to be run once)
def run_once(f):

    result = []

    @functools.wraps(f)
    def wrapper_run_once(*args, **kwargs):
        if not result:
            result.append(f(*args, **kwargs))
        return result[0]

    return wrapper_run_once

if __name__ == "__main__":
    @run_timed
    def test_function():
        print("Running timed function...")
        time.sleep(1) # Simulate a function that takes 1 second to run
        return ("Timed function complete")
    test_function()


    @run_once
    def expensive_setup():
        print("Running expensive setup...")
        time.sleep(2) # Simulate an expensive setup that takes 2 seconds
        return "Setup complete"

    print(expensive_setup()) 