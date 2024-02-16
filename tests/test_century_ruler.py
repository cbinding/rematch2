import unittest
import spacy
from rematch2 import CenturyRuler


class TestCenturyRuler(unittest.TestCase):

    def test_CenturyRulerDE(self):
        txt = "Das Artefakt stammt aus dem 7. bis 6. Jahrhundert v. Chr., Kann aber älter sein"
        nlp = spacy.load("de_core_news_sm", disable=['ner'])
        nlp.add_pipe("century_ruler", last=True)
        doc = nlp(txt)
        found = next((ent for ent in doc.ents if ent.label_ == "CENTURY" and ent.text == "7. bis 6. Jahrhundert v. Chr."), False)
        self.assertTrue(found)

    def test_CenturyRulerEN(self):
        txt = "The artefact dates from the 7th to 6th century BC but may be older"
        nlp = spacy.load("en_core_web_sm", disable=['ner'])
        nlp.add_pipe("century_ruler", last=True)
        doc = nlp(txt)
        found = next((ent for ent in doc.ents if ent.label_ == "CENTURY" and ent.text == "7th to 6th century BC"), False)
        self.assertTrue(found)
        