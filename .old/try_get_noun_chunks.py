#get noun chunks from doc and output them
import os
import spacy, json
from components.Util import read_json_file


input_directory = "./data/oasis/journals_july_2024/text_extraction-20251117" # Mark's script re-extracted text 2025-11-17
input_file_name = "text_extraction_archael547-079-116-ceolwulf.pdf.json"
input_file_path = os.path.join(input_directory, input_file_name)

json_data = read_json_file(input_file_path)
text = ""
if type(json_data) is dict:
    text = json_data.get("text", "")
elif type(json_data) is list:
    text = "\n".join([item.get("text", "") for item in json_data])

nlp = spacy.load("en_core_web_sm", disable = ['ner'])

doc = nlp(text)
chunks = doc.noun_chunks

with open("./noun_chunks_output_ceolwulf.txt", "w") as f:
    for span in chunks:
        f.write(f"{span.text}\n")