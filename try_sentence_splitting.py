# test sentence splitting approaches
import spacy # for sentence splitter
from spacy.lang.en import English 


input_file_name = "./data/journals_july_2024/078_047_054.pdf.txt"
with open(input_file_name) as input_file:
    input_text = input_file.read()

nlp = spacy.load("en_core_web_sm", disable=["ner"])
#nlp.add_pipe("sentencizer")
with nlp.select_pipes(enable=['tok2vec', "parser", "sentencizer"]):
    doc = nlp(input_text)

sentences = [sent.text.strip() for sent in doc.sents]

for sent in sentences:
    print(sent[0:60])
    print("***********************")
