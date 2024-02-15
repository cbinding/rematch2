# test alt methods of loading terminology list - ensure both sides lemmatised for matching
import spacy
# from spacy.lang.en import English
from spacy.matcher import PhraseMatcher
from pprint import pprint


def main():
    terms = [
        {
            "id": "011",
            "language": "en",
            "label": "ACTIVITY",
            "pattern": "brownest",
        },
        {
            "id": "012",
            "language": "en",
            "label": "ACTIVITY",
            "pattern": "Archaeologically",
        },
        {
            "id": "123",
            "language": "en",
            "label": "PERIOD",
            "pattern": "Early Roman",
        },
        {
            "id": "124",
            "language": "en",
            "label": "PERIOD",
            "pattern": "Roman",
        },
        {
            "id": "234",
            "language": "en",
            "label": "PERIOD",
            "pattern": "Early Iron Age",
        },
        {
            "id": "345",
            "language": "en",
            "label": "PERIOD",
            "pattern": "Early Bronze Age",
        },
        {
            "id": "456",
            "language": "en",
            "label": "OBJECT",
            "pattern": "Pottery",
        },
        {
            "id": "789",
            "language": "en",
            "label": "SUFFIX",
            "pattern": "A. D.",
        },
    ]
    text = "This collection comprises site data (images, CAD and reports) from an archaeological evaluation, an abacus or an a. D. abutment comprising the excavation of thirty-three trenches, at Handley Park, near Abthorpe, Northamptonshire In May 2014, carried out by Cotswold Archaeology. The evaluation was commissioned by Pegasus Planning Group, acting on behalf of Haymaker Energy Ltd, and was carried out prior to the submission of a planning application for the construction of a solar park on the site. Evidence for Late Bronze Age / Early Iron Ages activity, comprising a pit and a ditch from which a small assemblage of pottery was recovered, was encountered on the south-east facing slope overlooking the valley of Silverstone Brook. In the same area the remains of a small Roman settlement, probably a farmstead and associated field system, were identified. The Roman features contained pottery, animal bone and fragments of Roman roof tile, the latter indicating that there may have been a building in the vicinity. The Middle/Late Saxon remains comprised a circular or oval enclosure, although no evidence was encountered for features within the enclosure. Pottery dateable to the 7th to 10th centuries, a fragment of an iron pin or bobbin and a metal fragment, possibly part of a bucket with mineralised wood fibres adhering to its surface, were recovered from the enclosure ditch. The archaeological features broadly corresponded with anomalies detected by a geophysical survey of the site, although in a number of instances there was only an approximate correlation with the geophysical survey results, possibly due to the highly variable geology. Many of the anomalies interpreted as being of possible archaeological significance were confirmed as geological in origin and several features were identified that were not detected by the geophysical survey."

    # test lemmatisation, does it work the way I think it works???
    txt2 = "the quickest brownest foxes jumped over the laziest dogs. The programming indicated that the early iron ages A. D. was archaeologically and educationally significant"
    # txt2 = "earlier iron ages"
    nlp2 = spacy.load("en_core_web_sm", exclude=['ner'])
    # the lemmatisation WON'T work if it thinks words are proper nouns, so lowercase everything...
    doc2 = nlp2(txt2.lower())
    lemmatised = ' '.join(token.lemma_ for token in doc2)
    print("lemmatised1: ", lemmatised)
    #for token in doc2:
        #print(token, token.lemma_)

    # nlp = English()
    nlp = spacy.load("en_core_web_sm", exclude=['ner'])
    # nlp.add_pipe("lemmatizer", last=True)
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    # print(nlp.pipeline)
    # patterns = [nlp.make_doc(term)
    # for term in map(lambda item: item["label"], terms)]
    # patterns = [nlp(term) for term in map(
    # lambda item: item["pattern"].lower(), terms)]

    # lemmatize all words using SAME pipeline for lookup terms/phrases and doc text
    patterns = []
    for term in map(lambda item: item["pattern"].lower(), terms):
        doc1 = nlp(term)
        # words = list(map(lambda token: token.lemma_, doc))
        # lemmatised = ' '.join(token.lemma_ for token in doc1)
        lemmatised = ' '.join([token.lemma_ for token in nlp(term)])
        # print("lemmatised: ", lemmatised)
        doc2 = nlp.make_doc(lemmatised)
       # patterns.append(nlp.make_doc(lemmatised))
        patterns.append(doc2)

    matcher.add("term_patterns", patterns)

    # print(patterns[3].text)

    doc = nlp(text.lower())
    for match_id, start, end in matcher(doc):
        print("s based on token text:", doc[start:end])


if __name__ == '__main__':
    main()
