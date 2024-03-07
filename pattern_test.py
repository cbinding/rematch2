import spacy
from rematch2.Util import *


text = "This collection comprises images, CAD, spreadsheets and a report from an Archaeological Evaluation of Land off Ellen Aldous Avenue, Hadleigh. This work was undertaken by Archaeology South-East between January to February 2021. A preceding geophysical survey detected a range of anomalies of possible or probable archaeological origin, mainly concentrated in the western part of the site, indicating the potential presence of a series of ditched enclosures. A total of fifty-five evaluation trenches were investigated across the northern 8.8ha of the overall 18.4ha site. Archaeological features were recorded in thirty-nine trenches and comprised ditches, pits and possible postholes. A close correspondence between the archaeological evaluation and geophysical survey results was evident, though smaller features such as pits and postholes had generally not been detected as geophysical anomalies. Remains of Early Iron Age ditched enclosures, a possible trackway and a few pits were found in two distinct concentrations in the west and east of the evaluated area. Remains of Roman ditched field / enclosure systems were recorded across the west half of the evaluated area. A further Roman ditch was found in the east. The significant quantity and range of artefacts and plant remains recovered from these Roman period features(especially from a few ditches in the west) suggests that they relate to a rural settlement, such as a farmstead, located in the near vicinity. A number of ditches defining former field boundaries, along with quarries and other pits, relate to the agricultural use of this landscape in the late post-medieval and early modern periods. The boundary ditches are shown on historic mapping from the earlier 19th century onwards."

nlp = get_pipeline_for_language("en")
ruler = nlp.add_pipe("entity_ruler")
patterns = [
      
    {   
        'id': 'http://purl.org/heritagedata/schemes/eh_tmt2/concepts/70361', 
        'label': 'OBJECT', 
        'pattern': [
            {'LEMMA': 'ditch'}, 
            {'LEMMA': 'enclosure'}
        ]
    }
]
ruler.add_patterns(patterns)

doc = nlp(text)
for ent in doc.ents:
    print(ent.start_char, ent.end_char, ent.ent_id_, ent.text, ent.label_)
