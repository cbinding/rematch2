__version__ = "0.2.0"

#from ..old.BaseAnnotator import BaseAnnotator
from .DatePrefixRuler import create_dateprefix_ruler
from .DateSeparatorRuler import create_dateseparator_ruler
from .DateSuffixRuler import create_datesuffix_ruler
from .DayNameRuler import create_dayname_ruler
from .MonthNameRuler import create_monthname_ruler
from .PeriodoRuler import create_periodo_ruler
from .OrdinalRuler import create_ordinal_ruler
from .PeriodoData import PeriodoData
from .SeasonNameRuler import create_seasonname_ruler
#from ..old.TemporalAnnotator import TemporalAnnotator
from .VocabularyRuler import create_vocabulary_ruler
from .GeoNamesRuler import create_geonames_ruler
from .SpanScorer import create_span_scorer
from .ChildSpanRemover import child_span_remover
from .NegationRuler import NegationRuler
from .SpanPair import SpanPair
from .SpanPairs import SpanPairs
from .SpanScorer import SpanScorer
from .DocSummary import DocSummary
from .Decorators import run_timed
from .TextNormalizer import TextNormalizer, create_text_normalizer, create_text_normalizer_en
from .Util import *
from .YearSpanRuler import create_yearspan_ruler


# The following was previously a workaround for relative imports in Python 3.6
# instead now use e.g. 'python -m components.TextNormalizer' from package root
# to run modules directly for testing purposes.
# import os
# import sys
# sys.path.append(os.path.dirname(os.path.realpath(__file__)))
# sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)))
