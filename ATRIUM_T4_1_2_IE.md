# ATRIUM T4.1.2 Information Extraction
Script to perform Information Extraction on archaeological reports.

### installation
Required Python 3.12 or later.

Clone the repository, install associated dependencies and download the appropriate spaCy language model:
```bash
git clone https://github.com/cbinding/rematch2.git
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Usage
Run the main script on a number of data files:
```sh
$ python ./ATRIUM_T4_1_2_IE.py [-i] [-p] [-o] [-f]

e.g. $ python ./ATRIUM_T4_1_2_IE.py -i './path/to/files' -p '*.pdf' -f "json,csv"
```

**options:**

```-i, --inputpath```  
Path of folder containing input files to be processed

```-p, --inputpatt```  
Pattern to specify a subset of file names to be processed (e.g. "*.pdf"). The script will take as input PDF, TXT or JSON files. If not specified the default value is "*" (i.e. all files in the input folder)

```-o, --outputpath```  
Path of folder to hold resultant processed data files. If the specified folder does not already exist it will be created. If not specified, a date-stamped folder will be created within the input folder instead (e.g. ie-output-yyyymmdd) ansd the result files will be saved there

```-f, --outputformat```  
Output format(s) for processed data files ("pdf", "txt", "csv" or "json"). The script can produce PDF, plain text, CSV or JSON output files). If multiple output formats are required then use a comma delimited string here (e.g. -f "json,csv")

## Outputs
The CSV output will be a table of identified spans representing subject terms and indicating their locations within the text, e.g.

| start | end   | token_start | token_end | label         | id                                                           | text                         | sec_score | sections         | sig_proximity | score | score_explain   | context                                              |
|-------|-------|-------------|-----------|---------------|--------------------------------------------------------------|------------------------------|-----------|------------------|---------------|-------|-----------------|------------------------------------------------------|
| 0     | 15    | 0           | 2         | PERIOD        | http://n2t.net/ark:/99152/p0kh9ds9nsj                        | ROMANO - BRITISH             | 0.1       | page, body       | 0.0           | 0.1   | (0.10) + (0.00) | ROMANO - BRITISH AISLED HOUSES By J.                 |
| 17    | 29    | 3           | 4         | FISH_MONUMENT | http://purl.org/heritagedata/schemes/eh_tmt2/concepts/91023  | AISLED HOUSES                | 0.1       | page, body       | 0.0           | 0.1   | (0.10) + (0.00) | ROMANO - BRITISH AISLED HOUSES By J. T. SMITH        |
| 80    | 87    | 16          | 16        | FISH_MONUMENT | http://purl.org/heritagedata/schemes/eh_tmt2/concepts/70336  | building                     | 0.1       | page, body       | 0.0           | 0.1   | (0.10) + (0.00) | with the type of building usually known as basilican |
| 417   | 425   | 80          | 80        | FISH_MONUMENT | http://purl.org/heritagedata/schemes/eh_tmt2/concepts/70336  | buildings                    | 0.1       | page, body       | 0.0           | 0.1   | (0.10) + (0.00) | name is that the buildings under discussion did not  |
| 505   | 513   | 93          | 93        | FISH_MONUMENT | http://purl.org/heritagedata/schemes/eh_tmt2/concepts/70420  | structure                    | 0.1       | page, body       | 0.0           | 0.1   | (0.10) + (0.00) | definition of a basilican structure, which, in       |
| 616   | 624   | 117         | 117       | FISH_MONUMENT | http://purl.org/heritagedata/schemes/eh_tmt2/concepts/70336  | Buildings                    | 0.1       | page, body       | 0.0           | 0.1   | (0.10) + (0.00) | flanked by aisles. Buildings of this kind were       |
| 659   | 663   | 125         | 125       | PERIOD        | http://n2t.net/ark:/99152/p0kh9ds9nsj                        | Roman                        | 0.1       | page, body       | 0.0           | 0.1   | (0.10) + (0.00) | were not unknown in Roman Britain but may well       |
| 802   | 814   | 152         | 153       | FISH_MONUMENT | http://purl.org/heritagedata/schemes/eh_tmt2/concepts/91023  | aisled houses                | 0.1       | page, body       | 0.0           | 0.1   | (0.10) + (0.00) | the term to all aisled houses with a nave and        |
| 1030  | 1039  | 193         | 193       | FISH_MONUMENT | http://purl.org/heritagedata/schemes/eh_tmt2/concepts/70420  | structures                   | 0.1       | page, body       | 0.0           | 0.1   | (0.10) + (0.00) | important class of aisled structures, nor even of    |
| 1060  | 1068  | 199         | 199       | FISH_MONUMENT | http://purl.org/heritagedata/schemes/eh_tmt2/concepts/70336  | buildings                    | 0.1       | page, body       | 0.0           | 0.1   | (0.10) + (0.00) | nor even of those buildings in which a clerestorey   |


The CSV output columns are:
* `start` - start character position of the identified span
* `end` - end character position of the identified span
* `token_start` - start token position for the identified span
* `token_end` - end token position for the identified span
* `label` - the 'type' of entity identified (e.g. PERIOD, OBJECT, MONUMENT etc.)
* `id` - identifier associated with the entity (as specified in the matching patterns)
* `text` - text of the entity, as it appears in the input text
* `sec_score` - maximum section score for the located entity. Each section has an associated score specified
* `sections` - section(s) the entity is located within e.g. 'page', 'abstract', 'body', 'end_matter' (may be multiple e.g. 'page,body')
* `sig_proximity` - score assigned where the entity is in close proximity to a 'significance' indicator
* `score` - overall calculated score for the located entity (sec_score + sig_proximity)
* `score_explain` - breakdown explanation of the overall calculated score 
* `context` - wider textual context for the located entity text 

The JSON, TXT and PDF format outputs are more detailed, containing the following sections:
* `metadata` - metadata about the information extraction process performed
* `text` - the input text these output results are based on
* `tokens` - tokenisation of the text (input text broken down to a list of individual words/punctuation marks with associated character locations)
* `label_counts` - aggregated summary of counts for each unique label identified
* `spans` - a list of all individual spans located (containing fields as in the CSV output described above)
* `span_scores`- aggregated summary of scores for each unique entity identified
* `span_pairs` - pairs of entities located (e.g. "12th Century" - "Vessels", "Medieval" - "pottery", "Roman" - "settlement")
* `sections` - a supplied list of section locations (for use in scoring)
