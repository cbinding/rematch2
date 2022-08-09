import json
from TemporalRecognizer import TemporalRecognizer

testdata_file_name = "test-examples.json"
testData = None 
with open(testdata_file_name, "r") as f:  # what if file doesn't exist?            
    testData = json.load(f)   

if __name__ == "__main__":    
    out_format = "tsv"
    for testItem in testData:
        print(f"-------------\nlanguage = {testItem['language']}")
        tr = TemporalRecognizer(testItem["language"], testItem["periodo_id"])
        entities = tr.get_entities(testItem["value"], out_format)
        #formatted = TemporalRecognizer.format_entities(testItem["value"], entities, out_format)
        print(entities)             