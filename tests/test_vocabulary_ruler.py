import unittest
import spacy

from rematch2 import Util, VocabularyRuler

class TestVocabularyRuler(unittest.TestCase):       
    def setUp(self):
        self.nlp = Util.get_pipeline_for_language("en")

    def tearDown(self):
        del self.nlp


    def test_aat_activities_ruler(self):
        found = False
        txt = "Contextualisation and spatial analysis reveals finer - scale patterning than is usually possible with summed - probability approaches"
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
        
    
    def test_fish_archsciences_ruler(self):
        found = False
        txt = "Further analysis of the radiocarbon dating results was undertaken."
        self.nlp.add_pipe("fish_archsciences_ruler", last=True)
        doc = self.nlp(txt)
        self.nlp.remove_pipe("fish_archsciences_ruler")
        #for tok in doc: print(f"{tok.text} {tok.pos_}")
        spans = doc.spans.get(Util.DEFAULT_SPANS_KEY, [])

        # should identify "radiocarbon dating"
        for span in spans:
            if span.id_ == "http://purl.org/heritagedata/schemes/560/concepts/142188" and \
                span.label_ == "FISH_ARCHSCIENCE" and \
                span.start == 4 and span.end == 6:
                found = True
                break

        self.assertTrue(found, msg=spans)