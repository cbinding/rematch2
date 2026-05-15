import spacy
import pandas as pd
from components import YearSpanRuler, ChildSpanRemover, PeriodoRuler

# use a predefined pipeline, disabling the default NER component
nlp = spacy.load("en_core_web_sm", disable=["ner"])
# add required pipeline component(s) to the end of the pipeline
nlp.add_pipe("yearspan_ruler", last=True)
nlp.add_pipe("periodo_ruler", last=True, config={"periodo_authority_id": "p0kh9ds"})
nlp.add_pipe("child_span_remover", last=True)

test_text = """Although generally undated, the ditches were suggestive of a trackway and associated enclosure/field boundaries. Other ditches encountered on site correlated with post-medieval field boundaries depicted on 19th century mapping. Given the results of the 2018 evaluation, in conjunction with those of the 2018 investigations at nearby Chalk's Farm, which uncovered the remains of Late Bronze Age-early Iron Age and early Roman settlement and agricultural activity, it was deemed necessary to undertake a further phase of evaluation at the site."""
# process some example text using the modified pipeline
doc = nlp(test_text)
# display the spans located in the text (they will be under the key 'rematch')
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
start  end    label                                    id            text
   163  176   PERIOD http://n2t.net/ark:/99152/p0kh9dsctsj   post-medieval
   206  218 YEARSPAN                                          19th century
   378  393   PERIOD http://n2t.net/ark:/99152/p0kh9dsqkbq Late Bronze Age
   394  408   PERIOD http://n2t.net/ark:/99152/p0kh9dszskn  early Iron Age
   413  424   PERIOD http://n2t.net/ark:/99152/p0kh9ds7wqn     early Roman
  """