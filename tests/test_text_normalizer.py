import unittest
import spacy

from components import Util


class TestTextNormalizer(unittest.TestCase):       
    
    def setUp(self):
        self.nlp = Util.load_pipeline_for_language("en")
        # example - testing whitespace & punctuation issues and inconsistent spelling
        self.text = f"Archeological  work in Bełżec indi-\ncated   an Iron Age/ Romano- British  /Roman\npost -hole, in( low -lying)ground.\nThis  was  near(vandal-\nized)\n  mediæval/post-medieval(15th-17th century? )foot-\nings. Items of Mediaeval &  paleolithic(archeological)jewelry dated to the 2nd -  3rd century and pottery & vertebræ of a fœtus were  located in the New Harbor area.  Gray colored  & oxidized,aluminum artifacts were   found near the theater."
        self.nlp.add_pipe("text_normalizer", before="tagger")           
        self.doc = self.nlp(self.text)
        self.nlp.remove_pipe("text_normalizer")
        

    def tearDown(self):
        del self.nlp

    # test that spelling normalization is performed correctly
    def test_normalize_spelling(self):        
        self.assertTrue(self.doc[0].text == "Archaeological", msg=self.doc.text)
        

    # test that unicode substitution is performed correctly
    def test_normalize_unicode(self):
        self.assertTrue(self.doc[3].text == "Belzec", msg=self.doc.text)
