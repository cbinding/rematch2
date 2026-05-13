# build configured pipeline for ATRIUM T4_1_2
import spacy
from spacy.language import Language

# from tides_dataclasses import Report, Section

# load appropriate language-specific pipeline
def load_pipeline_for_language(language: str="en") -> Language:   
    lang: str = language.strip().lower()[:2] 
    package_name: str = ""
    match lang:
        case "en":
            package_name = "en_core_web_sm"
        case "fr":
            package_name = "fr_core_news_sm"
        case "de":
            package_name = "de_core_news_sm"  
        case "es":
            package_name = "es_core_news_sm"
        case _:
            raise ValueError(f"Unsupported language code \"{language}\"")
    
    return spacy.load(package_name, disable = ['ner'])
    

# get periodo authority ID to use based on language code 
def get_periodo_id_for_language(language: str="en") -> str:
    lang = language.strip().lower()[:2]        
    periodo_id: str = ""

    match lang:
        case "en":
            periodo_id = "p0kh9ds" # 'Historic England Archaeological and Cultural Periods' authority
        case "fr":
            periodo_id = "fr_core_news_sm" # 'PACTOLS chronology periods used in DOLIA data' authority
        case "de":
            periodo_id = "de_core_news_sm"  # using ARIADNE authority (no DAI authority??)
        case "es":
            periodo_id = "es_core_news_sm" # using 'SIA+ Chrono-Cultural Categories' authority
        case _:
            raise ValueError(f"Unsupported language code \"{language}\"")
    
    return periodo_id

# get pre-configured information extraction pipeline
def get_configured_pipeline(language: str="en") -> Language:

    nlp: Language = load_pipeline_for_language(language) 
    periodo_id: str = get_periodo_id_for_language(language)
    
    nlp.add_pipe("normalize_text", before="parser")
    nlp.add_pipe("yearspan_ruler", last=True)  
    nlp.add_pipe("periodo_ruler", last=True, config={ "periodo_authority_id": periodo_id }) 
    nlp.add_pipe("child_span_remover", last=True) 
           
    return nlp


# test pipeline creation for each language
if __name__ == "__main__":
    print("Testing ATRIUM IE pipeline creation for multiple languages")

    for language in["en", "fr", "de", "es", "unknown"]:
        print(f"Building pipeline for language \"{language}\"...")
        try:
            nlp = get_configured_pipeline(language)
            print(f"Pipeline for language \"{language}\" built: {nlp.pipe_names}")               
        except ValueError as e:
            print(f"Error building pipeline for language \"{language}\": {e}")
            continue
       
    print("Finished.")
