import unittest
import spacy

from rematch2 import Util, VocabularyRuler

class TestAatActivitiesRuler(unittest.TestCase):       
    def setUp(self):
        self.nlp = Util.get_pipeline_for_language("en")

    def tearDown(self):
        del self.nlp


    def test_AatActivitiesRuler(self):
        found = False
        txt = "Contextualisation and spatial analysis of radiocarbon data reveals finer - scale patterning than is usually possible with summed - probability approaches"
        #nlp = Util.get_pipeline_for_language("en")
        self.nlp.add_pipe("aat_activities_ruler", last=True)
        doc = self.nlp(txt)
        self.nlp.remove_pipe("aat_activities_ruler")
        
        spans = doc.spans.get(Util.DEFAULT_SPANS_KEY, [])
       
        # should identify "spatial analysis"
        for span in spans:
            if span.id_ == "http://vocab.getty.edu/aat/300223990" and \
                span.label_ == "AAT_ACTIVITY" and \
                span.start == 2 and span.end == 4:
                found = True
                break

        self.assertTrue(found, msg=doc.spans)
        