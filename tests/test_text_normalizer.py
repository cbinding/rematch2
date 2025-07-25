import unittest
import spacy

from rematch2 import Util, TextNormalizer


class TestTextNormalizer(unittest.TestCase):       
    
    def setUp(self):
        self.nlp = Util.get_pipeline_for_language("en")
        # example - testing whitespace & punctuation issues and inconsistent spelling
        self.text = f"Archeological  work indi-\ncated   an Iron Age/ Romano- British  /Roman\npost -hole, in( low -lying)ground.\nThis  was  near(vandal-\nized)\n  mediæval/post-medieval(15th-17th century? )foot-\nings. Items of Mediaeval &  paleolithic(archeological)jewelry dated to the 2nd -  3rd century and pottery & vertebræ of a fœtus were  located in the New Harbor area.  Gray colored  & oxidized,aluminum artifacts were   found near the theater."


    def tearDown(self):
        del self.nlp


    def test_text_normalizer(self):        
        #self.nlp.add_pipe("normalize_text", before="tagger", config={"normalize_spelling": False})     
        self.nlp.add_pipe("normalize_text", before="tagger")           
        doc = self.nlp(self.text)
        self.nlp.remove_pipe("normalize_text")

        self.assertTrue(doc[0].text == "Archaeological", msg=doc.text)