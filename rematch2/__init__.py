#from .ReSpeller import ReSpeller
from .BaseAnnotator import BaseAnnotator
from .DatePrefixRuler import create_dateprefix_ruler
from .DateSeparatorRuler import create_dateseparator_ruler
from .DateSuffixRuler import create_datesuffix_ruler
from .DayNameRuler import create_dayname_ruler
from .MonthNameRuler import create_monthname_ruler
from .PeriodoRuler import create_periodo_ruler
from .OrdinalRuler import create_ordinal_ruler
from .PeriodoData import PeriodoData
from .SeasonNameRuler import create_seasonname_ruler
from .TemporalAnnotator import TemporalAnnotator
from .VocabularyAnnotator import VocabularyAnnotator
from .VocabularyEnum import VocabularyEnum
from .VocabularyRuler import *
from .SpanPair import SpanPair
from .SpanPairs import SpanPairs
from .DocSummary import DocSummary
from .StringCleaning import *
from .Util import *
#from .LogFile import LogFile # not currently used
from .YearSpanRuler import create_yearspan_ruler

__version__ = "0.2.0"

# For relative imports to work in Python 3.6
import os
import sys
# sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)))
