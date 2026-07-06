import pandas as pd  # for DataFrame
import json
from html import escape # to esscape values for HTML display

# default initial values for sliders (used for reset button and as fallback if sliders are not set)
DEFAULT_SCORES: dict[str, float] = {
    "title": 40.0,              # score for terms apprearing in the title section
    "abstract": 2.0,            # score for terms apprearing in the abstract section
    "body": 0.1,                # score for terms apprearing in the body section
    "sig_proximity": 2.0,       # score for terms with significance proximity to the target term
    "mrs": 0.0,                 # Minimum Relevance Score
    "mrc": 1.0                  # Minimum Relevance Count
}


def get_input_data(filepath_or_buffer) -> list[dict]:    
    df = pd.read_csv(filepath_or_buffer, delimiter=",", encoding="utf-8", skip_blank_lines=True)
    # set any NaN values to blank string
    df.fillna("", inplace=True)
    # returning data as list[dict]
    return df.to_dict(orient='records')


# get maximum section score from a list of sections
# (e.g. concept may be within "abstract", "page" AND "body" sections)
def get_max_section_score(sections: list[str], slider_t, slider_a, slider_b) -> float:

    def get_section_score(section: str="") -> float:
        score_by_section: dict[str, float] = {
            "title": float(slider_t.value),
            "abstract": float(slider_a.value),
            "body": float(slider_b.value),
            "end_matter": 0.0
        }
        return score_by_section.get(section.strip().lower(), 0.0)

    return max([get_section_score(sec) for sec in sections], default=0.0)


# create HTML anchor for displaying id that looks like URL
def make_html_link(id, lbl):
    label = escape(lbl)
    if str(id).startswith("http"):
        return f"<a target='_blank' rel='noopener noreferrer' href='{str(id)}'>{label}</a>"
    else:
        return label


# calculate aggregated scores per concept id
def aggregate_results_by_concept(data: list[dict], slider_t, slider_a, slider_b, slider_s) -> pd.DataFrame:
    sum_by_id = {}

    for row in data:
        # create list from csv delimited string of sections
        sections = list(row.get('sections', '').split(','))
        # if item is located in the end matter don't use it
        if('end_matter' in sections):
            continue

        # for concept_id use 'id' field, or text field if not present
        concept_id: str = str(row.get('id', '')).strip().lower()
        if(concept_id == ''):
            concept_id = str(row.get('text', '')).strip().lower()

        # do we have a record for this concept?
        if concept_id not in sum_by_id.keys():
            # create new record for this concept
            sum_by_id[concept_id] = {
                'id': concept_id,
                'text': [],
                'label': row.get('label', ''),
                'sec_score': 0.0,
                'sig_score': 0.0,
                'score': 0.0,
                'count': 0
            }
        new_section_score: float = get_max_section_score(sections, slider_t, slider_a, slider_b)
        new_sig_proximity: float = round(slider_s.value, 2) if row.get('sig_proximity', 0) > 0 else 0.0
        new_concept_text: str = row.get('text', '')
        if new_concept_text != "" and new_concept_text not in sum_by_id[concept_id]['text']:
            sum_by_id[concept_id]['text'].append(new_concept_text)
        # aggregate scores for this concept
        sum_by_id[concept_id]['sec_score'] += new_section_score
        sum_by_id[concept_id]['sig_score'] += new_sig_proximity
        sum_by_id[concept_id]['score'] += new_section_score + new_sig_proximity
        sum_by_id[concept_id]['count'] += 1

    # return as a DataFrame, adding combined columns for display purposes
    df = pd.DataFrame(list(sum_by_id.values()))
    df["span"] = df.apply(lambda x: make_html_link(x['id'], ", ".join(x['text'])), axis=1)
    df["score_explain"] = df.apply(lambda x: f"({round(x['sec_score'], 2)} + {round(x['sig_score'], 2)})", axis=1)
    return df
