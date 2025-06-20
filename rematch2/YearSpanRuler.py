"""
=============================================================================
Package :   rematch2
Module  :   YearSpanRuler.py
Version :   20231027
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy custom pipeline component (specialized SpanRuler)
            Language-sensitive component to identify and tag ordinal centuries
            in free text. Span label will be "YEARSPAN"
Imports :   spacy, Language, Doc, Token, SpanRuler
Example :   nlp.add_pipe("yearspan_ruler", last=True)           
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History :   
03/08/2022 CFB Initially created script
27/10/2023 CFB type hints added for function signatures
28/03/2024 CFB base on SpanRuler instead of EntityRuler
=============================================================================
"""
import spacy
from spacy.language import Language
from spacy.pipeline import SpanRuler
from spacy.tokens import Doc, Token
#from spacy.lang.cs import Czech #doesn't exist yet..
from spacy.lang.de import German
from spacy.lang.en import English
from spacy.lang.es import Spanish
from spacy.lang.fr import French
from spacy.lang.it import Italian
from spacy.lang.nl import Dutch
from spacy.lang.nb import Norwegian
from spacy.lang.sv import Swedish
from spacy.lang.pl import Polish # experimental substitute for Czech as it doesn't exist yet..

if __package__ is None or __package__ == '':
    # uses current directory visibility
    from spacypatterns import *
    from CustomSpanRuler import CustomSpanRuler
    from OrdinalRuler import create_ordinal_ruler
    from DatePrefixRuler import create_dateprefix_ruler
    from DateSuffixRuler import create_datesuffix_ruler
    from DateSeparatorRuler import create_dateseparator_ruler
    from MonthNameRuler import create_monthname_ruler
    from SeasonNameRuler import create_seasonname_ruler
    from Util import *
    from DocSummary import DocSummary
else:
    # uses current package visibility
    from .spacypatterns import *
    from .CustomSpanRuler import CustomSpanRuler
    from .OrdinalRuler import create_ordinal_ruler
    from .DatePrefixRuler import create_dateprefix_ruler
    from .DateSuffixRuler import create_datesuffix_ruler
    from .DateSeparatorRuler import create_dateseparator_ruler
    from .MonthNameRuler import create_monthname_ruler
    from .SeasonNameRuler import create_seasonname_ruler
    from .Util import *
    from .DocSummary import DocSummary


# YearSpanRuler is a specialized CustomSpanRuler
class YearSpanRuler(CustomSpanRuler):

    def __init__(self, nlp: Language, name: str="yearspan_ruler", patterns: list=[]) -> None:
        # add token extensions for YearSpan patterns to work
        if not Token.has_extension("is_dateprefix"):
            Token.set_extension(name="is_dateprefix", getter=is_dateprefix)

        if not Token.has_extension("is_datesuffix"):
            Token.set_extension(name="is_datesuffix", getter=is_datesuffix)

        if not Token.has_extension("is_dateseparator"):
            Token.set_extension(name="is_dateseparator", getter=is_dateseparator)

        if not Token.has_extension("is_ordinal"):
            Token.set_extension(name="is_ordinal", getter=is_ordinal)

        if not Token.has_extension("is_monthname"):
            Token.set_extension(name="is_monthname", getter=is_monthname)

        if not Token.has_extension("is_seasonname"):
            Token.set_extension(name="is_seasonname", getter=is_seasonname)
        
        if not Token.has_extension("labels"):
            Token.set_extension(name="labels", getter=get_labels_for_token)

        normalized_patterns = normalize_patterns(
            nlp=nlp, 
            patterns=patterns,
            default_label="YEARSPAN",
            lemmatize=False,
            min_term_length=2
        )

        for name in [
            "ordinal_ruler",            
            "dateprefix_ruler",
            "datesuffix_ruler",
            "dateseparator_ruler",
            "monthname_ruler",
            "seasonname_ruler"
        ]:
            if not name in nlp.pipe_names:
                nlp.add_pipe(name, last=True)

        CustomSpanRuler.__init__(
            self,
            nlp=nlp,        
            name=name,
            spans_key="rematch",
            phrase_matcher_attr="LOWER",
            validate=False,
            overwrite=False
        )

        # add patterns to this pipeline component
        self.add_patterns(normalized_patterns)


    def __call__(self, doc: Doc) -> Doc:

        doc = CustomSpanRuler.__call__(self, doc)

        # filter for 'atomic' labelled spans only used to determine yearspans
        #filtered = [span for span in all_spans if span.label_ not in [
        #    "ORDINAL", "DATEPREFIX", "DATESUFFIX", "DATESEPARATOR", "MONTHNAME", "SEASONNAME"]]
        #doc.spans["rematch"] = filtered
        def not_excluded(span):
            return span.label_ not in [
                "ORDINAL", 
                "DATEPREFIX", 
                "DATESUFFIX", 
                "DATESEPARATOR", 
                "MONTHNAME", 
                "SEASONNAME"
            ]
        # apply the filter
        doc.spans["rematch"] = list(filter(not_excluded, doc.spans.get("rematch", [])))
        
        # filter out 'sub-spans' encompassed by others
        def not_enclosed(span):
            return not any(
                item.orth_ != span.orth_
                and item.label_ == "YEARSPAN" # restricted as other types may be present!
                and item.start <= span.start 
                and item.end >= span.end 
                for item in doc.spans.get("rematch", [])
            )
        # apply the filter
        doc.spans["rematch"] = list(filter(not_enclosed, doc.spans.get("rematch", [])))

        return doc


@Language.factory("yearspan_ruler", default_config={"patterns": []})
def create_yearspan_ruler(nlp: Language, name: str = "yearspan_ruler", patterns: list=[]) -> YearSpanRuler:
    return YearSpanRuler(nlp, name, patterns)


@German.factory("yearspan_ruler")
def create_yearspan_ruler_de(nlp: Language, name: str = "yearspan_ruler") -> YearSpanRuler:
    return create_yearspan_ruler(nlp, name, patterns_de_YEARSPAN)


@English.factory("yearspan_ruler")
def create_yearspan_ruler_en(nlp: Language, name: str = "yearspan_ruler") -> YearSpanRuler:
    return create_yearspan_ruler(nlp, name, patterns_en_YEARSPAN)


@Spanish.factory("yearspan_ruler")
def create_yearspan_ruler_es(nlp: Language, name: str = "yearspan_ruler") -> YearSpanRuler:
    return create_yearspan_ruler(nlp, name, patterns_es_YEARSPAN)


@French.factory("yearspan_ruler")
def create_yearspan_ruler_fr(nlp: Language, name: str = "yearspan_ruler") -> YearSpanRuler:
    return create_yearspan_ruler(nlp, name, patterns_fr_YEARSPAN)


@Italian.factory("yearspan_ruler")
def create_yearspan_ruler_it(nlp: Language, name: str = "yearspan_ruler") -> YearSpanRuler:
    return create_yearspan_ruler(nlp, name, patterns_it_YEARSPAN)


@Dutch.factory("yearspan_ruler")
def create_yearspan_ruler_nl(nlp: Language, name: str = "yearspan_ruler") -> YearSpanRuler:
    return create_yearspan_ruler(nlp, name, patterns_nl_YEARSPAN)


@Norwegian.factory("yearspan_ruler")
def create_yearspan_ruler_no(nlp: Language, name: str = "yearspan_ruler") -> YearSpanRuler:
    return create_yearspan_ruler(nlp, name, patterns_no_YEARSPAN)


@Swedish.factory("yearspan_ruler")
def create_yearspan_ruler_sv(nlp: Language, name: str = "yearspan_ruler") -> YearSpanRuler:
    return create_yearspan_ruler(nlp, name, patterns_sv_YEARSPAN)

# Polish as temp experimental substitute until Czech is available
@Polish.factory("yearspan_ruler")
def create_yearspan_ruler_cs(nlp: Language, name: str = "yearspan_ruler") -> YearSpanRuler:
    return create_yearspan_ruler(nlp, name, patterns_cs_YEARSPAN)

    
# test the YearSpanRuler class
if __name__ == "__main__":

    tests = [
        {"lang": "de", "text": "Das Artefakt wurde von 1650 bis 1800 n. Chr. datiert und war korrodiert"},
        {"lang": "en", "text": "The artefact was dated from 1650 to 1800 AD and was corroded. possibly from start of March 1715 AD"},
        {"lang": "es", "text": "El artefacto estaba fechado entre 1650 y 1800 d. C. y estaba corroído."},
        {"lang": "fr", "text": "L'artefact était daté de 1650 à 1800 après JC et a été corrodé"},
        {"lang": "it", "text": "Il manufatto fu datato dal 1650 al 1800 d.C. e fu corroso"},
        {"lang": "nl", "text": "Het artefact dateerde van 1650 tot 1800 na Christus en was gecorrodeerd"},
        {"lang": "no", "text": "Gjenstanden ble datert fra 1650 til 1800 e.Kr. og var korrodert"},
        {"lang": "sv", "text": "Artefakten daterades från 1650 till 1800 e.Kr. och var korroderad"},
        {"lang": "cs", "text": "Objekt zámku v Chanovicích (okr. Klatovy) se nalézá spolu s pozdně románským kostelem sv. Kříže na severozápadním okraji obce. Byl postaven na nevýrazné ostrožně, jejíž páteř vytvářejí výchozy žulové skály. Ze tří stran sídlo obklopuje zpustlý park s rybníkem v jeho dolní části. Na severovýchodní straně pak k zámku přiléhá areál hospodářského dvora. Nejstarším dokladem existence chanovického sídla je pozdně románský kostel Povýšení sv. Kříže. Jako vlastnický kostel se patrně vázal na zde již existující feudální sídlo. Předpokládá se, že leželo v místech pozdějšího poplužního dvora, dnes dochovaného v klasicistní přestavbě. V průběhu 13. stol. bylo sídlo přeneseno na skalnatou ostrožnu, do míst dnešního zámku. V písemných pramenech se Chanovice objevují ve 2. polovině 14. století. Z této doby pochází též nejstarší dochovaná gotická část sídla. K výrazné přestavbě objektu došlo v prvních desetiletích 16. století za Chanovských z Dlouhé Vsi, kdy stavba nabyla dnešní půdorysné podoby. Areál byl ohrazen novou, značně silnou obvodovou zdí, respektující v některých úsecích starší konstrukce. Roku 1670 byla Chanovicím odpuštěna část berní povinnosti, což snad naznačuje, že obec v této době postihla jakási živelná pohroma. Do podoby sídla výrazně zasáhla barokní přestavba, ke které došlo někdy okolo poloviny 18. století za majitele Ferdinanda Jáchyma Rumerskirchena. Dílčí zásahy do stavby nastaly patrně také po ničivém požáru roku 1781, při kterém vyhořel kostel, fara, škola a zámek spolu s hospodářskými budovami přilehlého dvora. Na přelomu 18. a 19. stol. zámek rychle střídal majitele a pustnul. Písemné prameny uvádí, že roku 1811 objekt, v té době ve velmi špatném stavu, koupil plzeňský podnikatel František Becher. Ten nechal sejmout jedno patro, zámek opravil a pokryl těžkou krytinou. Úpravám se nevyhnul ani chanovický hospodářský dvůr. Částečně ho nechal přestavět na konci 19. stol. nový majitel Eduard Rytíř z Doubků. Poslední známá úprava hospodářského dvora byla projekčně připravována v roce 1901. (Anderle – Ebel 1996)"}
    ]
    for test in tests:
        lang = test.get("lang", "")
        text = test.get("text", "")

        # print header
        print(f"-------------\nlanguage = {lang}")
        # load language-specific pre-built pipeline
        nlp = get_pipeline_for_language(lang)
        # add custom component at the end of the pipeline
        nlp.add_pipe("yearspan_ruler", last=True)
        # run text through the pipeline
        doc = nlp(text)
        
        #print("Tokens:\n" + DocSummary(doc).tokens("text"))
        print("Spans:\n" + DocSummary(doc).spans("text"))

