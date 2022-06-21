# =============================================================================
# Package   : rematch2
# Module    : PeriodoData.py
# Version   : 0.0.1
# Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
# Contact   : ceri.binding@southwales.ac.uk
# Project   : ReMatch2
# Summary   : PeriodoData class
# Imports   : json, os, urllib, jmespath
# Example   : pd = PeriodoData();
#             pd.load();
#             auths = pd.get_authorities();
# License   : https://creativecommons.org/licenses/by/4.0/ [CC-BY]
# =============================================================================
# History
# 0.0.1 17/06/2022 CFB Initially created script
# =============================================================================
import json
import jmespath
from os.path import exists
from urllib.request import urlopen

class PeriodoData:
    """gets and manipulates Perio.do data"""

    # default data sources
    PERIODO_URI = "https://n2t.net/ark:/99152/p0dataset.json"
    CACHE_FILE_NAME = "periodo-cache.json"


    def __init__(self, refresh_cache=False):
        self.jsondata = None
        self.load(refresh_cache)


    def load(self, refresh_cache=False):
        """load data from cache or from url"""
        # checking if cache file exists first
        file_name = PeriodoData.CACHE_FILE_NAME
        cache_file_exists = exists(file_name)

        if cache_file_exists == False or refresh_cache == True:
            PeriodoData._cache_from_url(PeriodoData.PERIODO_URI)
        self.jsondata = PeriodoData._json_from_file(file_name) 


    @property
    def jsondata(self):
        """Perio.do JSON data"""
        return self._jsondata


    @jsondata.setter
    def jsondata(self, new_value):
        self._jsondata = new_value      


    @staticmethod
    def _json_from_url(url):
        """download JSON data from URL"""     
        data = json.loads(urlopen(url).read().decode("utf-8"))           
        return data

        
    @staticmethod
    def _json_from_file(file_name):
        """load JSON data from file"""  
        data = None 
        with open(file_name, "r") as f:  # what if file doesn't exist?            
            data = json.load(f) 
        return data  


    @staticmethod
    def _json_to_file(data, file_name):
        """write JSON data to file"""  
        with open(file_name, "w") as f:
            json.dump(data, f, indent=3) 
        

    @staticmethod
    def _cache_from_url(url=None, file_name=None):
        """refresh locally cached JSON file"""
        if url == None:
            url = PeriodoData.PERIODO_URI
        if file_name == None:
            file_name = PeriodoData.CACHE_FILE_NAME

        data = PeriodoData._json_from_url(url)        
        PeriodoData._json_to_file(data, file_name) 
        return file_name     

    
    # this is really versatile once we have the JSON data loaded...
    # pip3 install jmespath
    # see https://jmespath.org/tutorial.html

    def find(self, pattern):
        """find data by pattern, return JSON"""
        result = jmespath.search(pattern, self.jsondata)
        #return json.dumps(result) # to return JSON string, not python object
        return result 
    
    # specialised properties based on .find
    # returns list of authority as [{id, label}]
    def get_authority_list(self, sorted=True):
        #return self.find("keys(authorities)") 
        lst = self.find("authorities.* | [?source.title != null].{id: id, label: @.source.title}")
        if(sorted):
            lst.sort(key=lambda item: item["label"].lower())
        return lst
    
    # returns list of period as [{id, label}]
    def get_period_list(self, authorityID="*"):
        return self.find(f"authorities.{ authorityID }.periods.*.{{id: id, label: label}}") 

    # convert periods list into spaCy patterns
    @staticmethod
    def _period_to_pattern(period_string):
        words = period_string.split()
        pattern = list(map(lambda word:  {"LOWER": word }, words)) 


    @staticmethod
    def _periods_to_patterns(data, file_name):
        patterns = list(map(lambda item: { 
            "id": item["id"],            
            "label": "TEMPORAL", 
            "language": "en", 
            "pattern": list(map(lambda word:  { "LOWER": word.lower() }, item["label"].split()))           
        }, data)) 

        with open(file_name, "w") as f:
            json.dump(patterns, f, indent=3) 
 

# This class may be tested as a standalone script using the parameters below
#  e.g. python PeriodoData.py
if __name__ == "__main__":
    pd = PeriodoData(False)
    #pd.load()
    #print(pd.authorities) # all authorities
    #print(pd.data) # this specific authority
    #print(pd.authority("p0qwjcd")) # this specific authority
    #print(pd.periods("p0qwjcd")) ## all periods for this authority
    #print(pd.find(f"authorities.p0qwjcd")) # free searching data
    #print(pd.period("p0qwjcd", "p0qwjcdnzt9")) # this period in this authority
    #authorityID = "p0qwjcd"    
    #print(pd.find(f"authorities.{ authorityID }.periods")) # free searching data
    #print(pd.find("authorities.p0qwjcd.periods.*.{id: id, lbl: label}")) # free searching data
    #print(pd.find("authorities.* | source[].title"))
    #print(pd.find("authorities.*.id
    # print(pd.find("authorities.*.{key: id, lbl: @.source.title}"))
    #print(pd.find("authorities.* | [?source.title != null].{key: id, lbl: @.source.title}"))
    lst1 = pd.get_authority_list()
    lst2 = pd.get_period_list("p0kh9ds") # HeritageData 

    #lst = pd.get_period_list("p0h9ttq")
    print(lst1)
    print(lst2)
    PeriodoData._periods_to_patterns(lst2, "en-periodo-data.json")
    #print(pd.find("authorities.*.[@.source.title, id]"))