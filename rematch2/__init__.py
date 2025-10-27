__version__ = "0.2.0"

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
from .GeoNamesRuler import create_geonames_ruler
from .SpanRemover import child_span_remover, stop_list_span_remover
from .NegationRuler import NegationRuler
from .SpanPair import SpanPair
from .SpanPairs import SpanPairs
from .DocSummary import DocSummary
from .Decorators import run_timed
from .TextNormalizer import TextNormalizer
from .Util import *
from .YearSpanRuler import create_yearspan_ruler


# The following was previously a workaround for relative imports in Python 3.6
# instead now use e.g. 'python -m rematch2.TextNormalizer' from package root
# to run modules directly for testing purposes.
# import os
# import sys
# sys.path.append(os.path.dirname(os.path.realpath(__file__)))
# sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)))
