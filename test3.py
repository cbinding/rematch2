import spacy
import pandas as pd
from components import GeoNamesRuler

nlp = spacy.load("en_core_web_sm", disable=["ner"])

# example text
test_text = """This collection comprises Roman site data(reports, images, spreadsheets, GIS data and site records) from two phases of archaeological evaluation undertaken by Oxford Archaeology in June 2018 (SAWR18) and February 2021 (SAWR21) at West Road, Sawbridgeworth, Hertfordshire. SAWR18 In June 2018, Oxford Archaeology were commissioned by Taylor Wimpey to undertake an archaeological evaluation on the site of a proposed housing development to the north of West Road, Sawbridgeworth (TL 47842 15448)."""
nlp.add_pipe("geonames_ruler", last=True, config={"country_codes": ["GB"]})

doc = nlp(test_text)
spans = doc.spans.get("rematch", [])

# create DataFrame with required columns
df = pd.DataFrame([{
  "start": span.start_char,
  "end": span.end_char,
  "label": span.label_,
  "id": span.id_,
  "text": span.text
  } for span in spans])

# output results
print(df.to_string(index=False))  

"""results:
start end label                               id           text
159   165 PLACE http://sws.geonames.org/2640729/         Oxford
241   255 PLACE http://sws.geonames.org/2638481/ Sawbridgeworth
257   270 PLACE http://sws.geonames.org/2647043/  Hertfordshire
293   299 PLACE http://sws.geonames.org/2640729/         Oxford
462   476 PLACE http://sws.geonames.org/2638481/ Sawbridgeworth
"""