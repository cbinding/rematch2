"""
=============================================================================
Package   : rematch2.components
Module    : TokenPatterns.py
Version   : 0.0.1
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Project   : ARIADNEplus
Summary   : TokenPatterns class
Imports   : json, os, fnmatch
Example   : tp = TokenPatterns();
            patterns = tp.get(language, ['MONTHNAME', 'SEASONNAME']);             
License   : https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History
0.0.1 05/07/2022 CFB Initially created script
=============================================================================
"""
import json
import os
import fnmatch
#from os.path import exists
#from urllib.request import urlopen


class TokenPatterns:
    """loads spaCy token patterns from external JSON files"""

    def __init__(self):
        self._patterns = []
       # default data sources
        PATTERNS_PATH = "../src/patterns"

        # load all pre-defined token patterns from specified directory
        self._patterns = TokenPatterns.__load_json_from_directory(
            PATTERNS_PATH)
        #self._patterns = [pattern for pattern in patterns if (pattern.get("language") or "").lower() == self._language]

    @staticmethod
    def __load_json_from_directory(directory_name):
        """Construct array of token patterns from all JSON files in the specified directory"""
        file_names = os.listdir(directory_name)
        patterns = []

        for file_name in fnmatch.filter(file_names, "*.json"):
            file_name_with_path = os.path.join(directory_name, file_name)
            patterns.extend(
                TokenPatterns.__load_json_from_file(file_name_with_path))
        return patterns

    @staticmethod
    def __load_json_from_file(file_name_with_path):
        """Load data from one specified (JSON) file"""
        json_data = []
        with open(file_name_with_path, 'r', encoding='utf8') as f:
            json_data = json.load(f)
        return json_data

    def get(self, language=None, entities=[]):
        return [p for p in self._patterns if (p.get("language") or "").lower() == language and (p.get("label") or "").upper() in entities]

    def count(self, language=None, entities=[]):
        matches = self.get(language, entities)
        return len(matches)


# test code for this class
if __name__ == "__main__":
    language = "de"
    entities = ["MONTHNAME", "DATESUFFIX", "MONUMENT"]
    tp = TokenPatterns()

    count = tp.count(language, entities)
    print(count)

    patterns = tp.get(language, entities)
    print(patterns)
