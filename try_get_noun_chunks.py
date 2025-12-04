#get noun chunks from doc and output them
import os
import spacy, json

# read and parse a JSON file, returning the content as a dictionary
def read_json_file(file_path: str="") -> dict:
    file_content = {}
    try:
        with open(file_path, "r", encoding="utf-8-sig") as f:
            file_content = json.load(f)
    except Exception as e:
        print(f"Problem reading \"{file_path}\": {e}")
    return file_content


input_directory = "./data/oasis/journals_july_2024/text_extraction-20251117" # Mark's script re-extracted text 2025-11-17
input_file_name = "text_extraction_archael547-079-116-ceolwulf.pdf.json"
input_file_path = os.path.join(input_directory, input_file_name)

json_data = read_json_file(input_file_path)
text = json_data.get("text", "")

nlp = spacy.load("en_core_web_sm", disable = ['ner'])

doc = nlp(text)
chunks = doc.noun_chunks

with open("./noun_chunks_output_ceolwulf.txt", "w") as f:
    for filter(span in chunks:
        span.
        f.write(f"{span.text}\n")