#from .PatternRuler import PatternRuler
from .BaseAnnotator import BaseAnnotator
from .TemporalAnnotator import TemporalAnnotator
from .VocabularyAnnotator import VocabularyAnnotator

__version__ = "0.1.0"
#from . import components, patterns
# For relative imports to work in Python 3.6
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
