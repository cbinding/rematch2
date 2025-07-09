import unittest
import spacy
import logging

from rematch2 import Util, YearSpanRuler
# Set log level
loglevel = logging.DEBUG
logging.basicConfig(level=loglevel)
log = logging.getLogger("LOG")


class TestYearSpanRuler(unittest.TestCase):

    def test_YearSpanRulerDE(self):
        txt = "Das Artefakt stammt aus dem 7. bis 6. Jahrhundert v. Chr., Kann aber älter sein"
        nlp = Util.get_pipeline_for_language("de")
        nlp.add_pipe("yearspan_ruler", last=True)
        doc = nlp(txt)
        spans = doc.spans.get(Util.DEFAULT_SPANS_KEY, [])
        found = next((span for span in spans if span.label_ == "YEARSPAN" and span.text == "7. bis 6. Jahrhundert v. Chr."), False)
        self.assertTrue(found, msg=doc.ents)
        

    def test_YearSpanRulerEN(self):
        txt = "The artefact dates from the 7th to 6th century BC but may be older"
        nlp = Util.get_pipeline_for_language("en")
        nlp.add_pipe("yearspan_ruler", last=True)
        doc = nlp(txt)
        spans = doc.spans.get(Util.DEFAULT_SPANS_KEY, [])
        found = next((ent for ent in doc.ents if ent.label_ == "YEARSPAN" and ent.text == "7th to 6th century BC"), False)
        self.assertTrue(found)


    def test_YearSpanRulerES(self):
        txt = "el artefacto data del siglo VII al VI a. C. pero puede ser más antiguo"
        nlp = Util.get_pipeline_for_language("es")
        nlp.add_pipe("yearspan_ruler", last=True)
        doc = nlp(txt)
        for ent in doc.ents:
            print(ent.text)
        found = next((ent for ent in doc.ents if ent.label_ == "YEARSPAN" and ent.start_char == 22), False)
        self.assertTrue(found)