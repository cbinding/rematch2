"""
=============================================================================
Package :   rematch2
Module  :   GeoNamesRuler.py
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy custom pipeline component (specialized SpanRuler) to 
            identify place names (from GeoNames) in free text. 
            Span label will be "PLACE"
Imports :   os, sys, spacy, Language, SpanRuler, Doc, Language
Example :   
        nlp = spacy.load(pipe_name, disable=['ner'])
        nlp.add_pipe("geonames_ruler", last=True, config={"country_codes": ["GB"]}) 
        doc = nlp(test_text)

License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History :   
15/10/2024 CFB Initially created script
=============================================================================
"""
from pathlib import Path
import requests
import zipfile
import os
import sys
import spacy            # NLP library
import pandas as pd
from html import escape
#from spacy.pipeline import SpanRuler
from spacy.tokens import Doc
from spacy.language import Language
from pprint import pprint

from .Util import *
from .BaseRuler import BaseRuler
from .DocSummary import DocSummary


def download_file(remote_url: str, local_name: str, chunk_size: int=128, overwrite: bool=False):  
     # if local directory does not exist create it
    directory = Path(local_name).parent
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

     # if local file not already cached (or overwrite is requested), get it
    if overwrite==True or not os.path.exists(local_name):
        # download the remote file 
        response = requests.get(remote_url, timeout=30, stream=True)
        # write to the local file
        with open(local_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                f.write(chunk)


def get_geonames_admin1_data(country_codes: list=[]) -> list:
    # get (and cache) GeoNames 'admin1CodesASCII.txt' data file
    REMOTE_URL = "https://download.geonames.org/export/dump/admin1CodesASCII.txt"
    LOCAL_PATH = (Path(__file__).parent / "vocabularies").resolve()
    LOCAL_NAME = os.path.join(LOCAL_PATH, Path(REMOTE_URL).name )     
    download_file(REMOTE_URL, LOCAL_NAME, overwrite=False)

    # fields names in the input tab-delimited data file
    field_names = [
        "admin_code",
        "name" ,
        "ascii_name",
        "geoname_id"
    ]

    # read and parse extracted CSV data file to pandas DataFrame
    df = pd.read_csv(
        LOCAL_NAME, 
        delimiter="\t", 
        encoding="utf-8", 
        engine="python", 
        skip_blank_lines=True, 
        header=None,
        names=field_names
    )

    # filter records for specified country code(s) only
    myfilter = lambda x: x.partition(".")[0].upper() in country_codes
    filtered = df[df["admin_code"].apply(myfilter)] 
    
    # return data as an array of dict items   
    return filtered.to_dict(orient="records")


def get_geonames_admin2_data(country_codes: list=[]) -> list:
    # get (and cache) GeoNames 'admin2Codes.txt' data 
    REMOTE_URL = "https://download.geonames.org/export/dump/admin2Codes.txt"
    LOCAL_PATH = (Path(__file__).parent / "vocabularies").resolve()
    LOCAL_NAME = os.path.join(LOCAL_PATH, Path(REMOTE_URL).name )    
    
    download_file(REMOTE_URL, LOCAL_NAME, overwrite=False)

    # fields names in the input tab-delimited data file
    field_names = [
        "admin_code",
        "name" ,
        "ascii_name",
        "geoname_id"
    ]

    # read and parse extracted CSV data file to pandas DataFrame
    df = pd.read_csv(
        LOCAL_NAME, 
        delimiter="\t", 
        encoding="utf-8", 
        engine="python", 
        skip_blank_lines=True, 
        header=None,
        names=field_names
    )

    # filter records for specified country code(s) only
    myfilter = lambda x: x.partition(".")[0].upper() in country_codes
    filtered = df[df["admin_code"].apply(myfilter)] 
    
    # return data as an array of dict items   
    return filtered.to_dict(orient="records")



def get_geonames_city_data(country_codes: list=[]) -> list:
    # get (and cache) GeoNames 'cities500.zip' data file 
    REMOTE_URL = "https://download.geonames.org/export/dump/cities500.zip"
    LOCAL_PATH = (Path(__file__).parent / "vocabularies").resolve()
    LOCAL_NAME = os.path.join(LOCAL_PATH, Path(REMOTE_URL).name)
    download_file(REMOTE_URL, LOCAL_NAME, overwrite=False)
   
    # extract zipped data file contents to cache path
    #with zipfile.ZipFile(LOCAL_NAME, 'r') as zf:
        #zf.extractall(LOCAL_PATH)    

    # anticipated fields names in the input delimited data
    field_names = [
        "geoname_id",
        "name" ,
        "ascii_name",
        "alternate_names",
        "latitude",
        "longitude",
        "feature_class",
        "feature_code",
        "country_code",
        "cc2",
        "admin1_code",
        "admin2_code",
        "admin3_code",
        "admin4_code",
        "population",
        "elevation",
        "dem",
        "timezone",
        "modification_date"
    ]

    # read and parse extracted CSV data file to pandas DataFrame
    df = pd.read_csv(
        LOCAL_NAME, 
        delimiter="\t", 
        encoding="utf-8", 
        engine="python", 
        skip_blank_lines=True, 
        header=None,
        names=field_names
    )

    # filter down to records for specified country codes
    filtered = df[df["country_code"].isin(country_codes)] 

    # return data as a list of dict items   
    return filtered.to_dict(orient="records")


@Language.factory(name="geonames_ruler", default_config={"country_codes": ["GB"]})
def create_geonames_ruler(nlp: Language, name: str="geonames_ruler", country_codes=["GB"]) -> BaseRuler:

    # get records for selected GeoNames country codes
    geonames_admin1 = get_geonames_admin1_data(country_codes) 
    geonames_admin2 = get_geonames_admin2_data(country_codes) 
    geonames_cities = get_geonames_city_data(country_codes) 
    
    geonames_data = (geonames_admin1 or []) + (geonames_admin2 or []) + (geonames_cities or [])
    
    # convert all geonames records to required 'patterns' format 
    patterns = list(map(lambda item: {
        "id": f"http://sws.geonames.org/{escape(str(item.get('geoname_id', '')))}/",
        "label": "PLACE",
        "pattern": str(item.get("name", ""))
    }, geonames_data))    

    ruler = BaseRuler(
        nlp=nlp,        
        name=name,
        spans_key="rematch",
        #phrase_matcher_attr="LOWER",
        validate=False,
        overwrite=False
    ) 

    normalized_patterns = BaseRuler.normalize_patterns(
        nlp=nlp, 
        patterns=patterns,
        default_label="PLACE",
        lemmatize=False,
        pos=["PROPN"]
    ) 
      
    ruler.add_patterns(normalized_patterns)
    return ruler 
  

# test the PeriodoRuler class
if __name__ == "__main__":

    # import json
    # from ..test_examples import test_examples
    # test_file_name = "test_examples.py"
    # tests = []
    # with open(test_file_name, "r") as f:  # what if file doesn't exist?
    # tests = json.load(f)
    

    # example test
    test_text = """This collection comprises Roman site data(reports, images, spreadsheets, GIS data and site records) from two phases of archaeological evaluation undertaken by Oxford Archaeology in June 2018 (SAWR18) and February 2021 (SAWR21) at West Road, Sawbridgeworth, Hertfordshire. SAWR18 In June 2018, Oxford Archaeology were commissioned by Taylor Wimpey to undertake an archaeological evaluation on the site of a proposed housing development to the north of West Road, Sawbridgeworth(TL 47842 15448). A programme of 19 trenches was undertaken to ground truth the results of a geophysical survey and to assess the archaeological potential of the site. The evaluation confirmed the presence of archaeological remains in areas identified on the geophysics. Parts of a NW-SE‐aligned trackway were found in Trenches 1 and 2. Field boundaries identified by geophysics(also present on the 1839 tithe map) were found in Trenches 5 and 7, towards the south of the site, and in Trenches 12 and 16, in the centre of the site. Geophysical anomalies identified in the northern part of the site were investigated and identified as geological. The archaeology is consistent with the geophysical survey results and it is likely that much of it has been truncated by modern agricultural activity. SAWR21 Oxford Archaeology carried out an archaeological evaluation on the site of proposed residential development north of West Road, Sawbridgeworth, Hertfordshire, in February 2021. The fieldwork was commissioned by Taylor Wimpey as a condition of planning permission. Preceding geophysical survey of the c 5.7ha development site was undertaken in 2016 and identified a concentration of linear and curvilinear anomalies in the north-east corner of the site and two areas of several broadly NW-SE aligned anomalies in the southern half of the site. Subsequent trial trench evaluation, comprising the investigation of 19 trenches, was undertaken by Oxford Archaeology in 2018, targeted upon the geophysical survey results. The evaluation revealed a small number of ditches in the centre and south of the site, correlating with the geophysical anomalies. Although generally undated, the ditches were suggestive of a trackway and associated enclosure/field boundaries. Other ditches encountered on site correlated with post-medieval field boundaries depicted on 19th century mapping. Given the results of the 2018 evaluation, in conjunction with those of the 2018 investigations at nearby Chalk's Farm, which uncovered the remains of Late Bronze Age-early Iron Age and early Roman settlement and agricultural activity, it was deemed necessary to undertake a further phase of evaluation at the site. Four additional trenches were excavated in the southern half of the site to further investigate the previously revealed ditches. The continuations of the trackway ditches were revealed in the centre of the site, with remnants of a metalled surface also identified. Adjacent ditches may demonstrate the maintenance and modification of the trackway or perhaps associated enclosure/field boundaries. Artefactual dating evidence recovered from these ditches was limited and of mixed date, comprising small pottery sherds of late Bronze Age- Early Iron Age date and fragments of Roman ceramic building material. It is probable that these remains provide evidence of outlying agricultural activity associated with the later prehistoric and early Roman settlement evidence at Chalk's Farm. A further undated ditch and a parallel early Roman ditch were revealed in the south of the site, suggestive of additional land divisions, probably agricultural features. A post-medieval field boundary ditch and modern land drains are demonstrative of agricultural use of the landscape during these periods."""
    nlp = get_pipeline_for_language("en")    
    nlp.add_pipe("geonames_ruler", last=True, config={"country_codes": ["GB"]})

    doc = nlp(test_text)
    summary = DocSummary(doc)
    #print("\nTokens:\n" + summary.tokens("text"))
    print("\nSpans:\n" + summary.spans("text"))    