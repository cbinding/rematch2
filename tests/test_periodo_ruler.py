import unittest
import spacy

from rematch2 import Util, PeriodoRuler

class TestPeriodoRuler(unittest.TestCase):       
    def setUp(self):
        self.nlp = Util.get_pipeline_for_language("en")

    def tearDown(self):
        del self.nlp

    def test_periodo_ruler(self):
        found = False
        txt = "There was evidence of Early Bronze Age and Iron Age activity, plus a Medieval settlement"
        periodo_authority_id = "p0kh9ds"
        self.nlp.add_pipe("periodo_ruler", last=True, config={
                 "periodo_authority_id": periodo_authority_id})
        doc = self.nlp(txt)
        self.nlp.remove_pipe("periodo_ruler")
        
        spans = doc.spans.get(Util.DEFAULT_SPANS_KEY, [])
       
        # should identify "Early Bronze Age"
        for span in spans:
            if span.id_ == "http://n2t.net/ark:/99152/p0kh9dshs59" and \
                span.label_ == "PERIOD" and \
                span.start == 4 and span.end == 7:
                found = True
                break

        self.assertTrue(found, msg=doc.spans)