# =============================================================================
# Package   : rematch2
# Module    : PeriodoData.py
# Version   : 0.0.1
# Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
# Contact   : ceri.binding@southwales.ac.uk
# Project   : ReMatch2
# Summary   : PeriodoData class
# Imports   : json, os, urllib
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
    CACHE_FILE_NAME = "periodo_cache.json"


    def __init__(self):
        self._data = None


    def load(self, refresh_cache=False):
        """load data from cache or from url"""
        # checking if cache file exists first
        file_name = PeriodoData.CACHE_FILE_NAME
        cache_file_exists = exists(file_name)

        if cache_file_exists == False or refresh_cache == True:
            PeriodoData._cache_from_url(PeriodoData.PERIODO_URI)
        self.data = PeriodoData._json_from_file(file_name) 


    @property
    def data(self):
        """Perio.do JSON data"""
        return self._data


    @data.setter
    def data(self, new_value):
        self._data = new_value      


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
        result = jmespath.search(pattern, self.data)
        return json.dumps(result) # to return JSON string, not python object
    
    @property
    def authorities(self):
        return self.find("keys(authorities)")       

    @property
    def authority(self, authorityID="*"):
        return self.find(f"authorities.{ authorityID.strip() }") 

    @property
    def periods(self, authorityID="*"):
        return self.find(f"authorities.{ authorityID.strip() }.periods") 

    @property
    def period(self, authorityID="*", periodID="*"):
        return self.find(f"authorities.{ authorityID.strip() }.periods.{ periodID.strip() }") 
    

# This class may be tested as a standalone script using the parameters below
#  e.g. python PeriodoData.py
if __name__ == "__main__":
    pd = PeriodoData()
    pd.load()
    #print(pd.authorities) # all authorities
    #print(pd.data) # this specific authority
    #print(pd.authority("p0qwjcd")) # this specific authority
    #print(pd.periods("p0qwjcd")) ## all periods for this authority
    #print(pd.find(f"authorities.p0qwjcd")) # free searching data
    #print(pd.period("p0qwjcd", "p0qwjcdnzt9")) # this period in this authority
    #authorityID = "p0qwjcd"    
    #print(pd.find(f"authorities.{ authorityID }.periods")) # free searching data
    print(pd.find("authorities.p0qwjcd.periods.*.{id: id, lbl: label}")) # free searching data
    