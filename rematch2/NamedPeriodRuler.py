"""
=============================================================================
Package :   rematch2.components
Module  :   NamedPeriodRuler.py
Version :   20220803
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   ARIADNEplus
Summary :   spaCy custom pipeline component (specialized EntityRuler) to 
            identify named periods (from Perio.do) in free text. 
            Entity type added will be "NAMEDPERIOD"
Imports :   os, sys, spacy, Language, EntityRuler, Doc
Example :   nlp.add_pipe("namedperiod_ruler", last=True)           
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
History :   03/08/2022 CFB Initially created script
=============================================================================
"""
import os
import sys
import spacy            # NLP library

from spacy.pipeline import EntityRuler
from spacy.tokens import Doc
from spacy.language import Language

if __package__ is None or __package__ == '':
    # uses current directory visibility
    from PeriodoData import PeriodoData
else:
    # uses current package visibility
    from .PeriodoData import PeriodoData

@Language.factory(name="namedperiod_ruler", default_config={"periodo_authority_id": None})
def create_namedperiod_ruler(nlp, name, periodo_authority_id: str):
    ruler = NamedPeriodRuler(nlp, name, periodo_authority_id)
    return ruler

# NamedPeriodRuler is a specialized EntityRuler
class NamedPeriodRuler(EntityRuler):

    def __init__(self, nlp: Language, name: str, periodo_authority_id=None) -> None:
        EntityRuler.__init__(
            self,
            nlp=nlp,
            name=name,
            phrase_matcher_attr="LOWER",
            validate=True,
            overwrite_ents=True,
            ent_id_sep="||"
        )
        # add terms from selected Perio.do authority as patterns
        pd = PeriodoData()  # new instance, don't refresh cached data
        periodo_periods = pd.get_period_list(
            periodo_authority_id)  # periods for authority id
        periodo_patterns = NamedPeriodRuler._periods_to_patterns(
            periodo_periods, nlp)  # convert to spaCy pattern format
        self.add_patterns(periodo_patterns)

    def __call__(self, doc: Doc) -> Doc:
        EntityRuler.__call__(self, doc)
        return doc

    # lemmatize each word in phrase for better chance of free-text match
    # using SAME nlp pipeline for patterns and terms being compared,
    # rather than separate independent tokenisation..
    @staticmethod
    def _period_to_pattern(period, nlp):
        # normalise whitespace and force lowercase
        # (lemmatization won't work if capitalised)
        clean = ' '.join(period.strip().lower().split())
        doc = nlp(clean)

        # lemmatize the words in the period
        pat = [{"LEMMA": tok.lemma_} for tok in doc]
        return pat

    # Convert Periodo period records to list of spaCy patterns
    # input: [{id, language, label}, {id, language, label}]
    # output: [{id, language, label, pattern}, {id, language, label, pattern}]
    @staticmethod
    def _periods_to_patterns(data, nlp):
        patterns = list(map(lambda item: {
            "id": item.get("uri", ""),
            "language": item.get("language", ""),
            "label": "NAMEDPERIOD",
            "pattern": NamedPeriodRuler._period_to_pattern(item.get("label", ""), nlp)
            # "pattern": list(map(lambda word: {"LOWER": word.lower()}, item.get("label", "").split()))
        }, data or []))
        return patterns


# test the NamedPeriodRuler class
if __name__ == "__main__":

    # import json
    # from ..test_examples import test_examples
    # test_file_name = "test_examples.py"
    # tests = []
    # with open(test_file_name, "r") as f:  # what if file doesn't exist?
    # tests = json.load(f)

    pipeline = "fr_core_news_sm"
    periodo_authority_id = "p02chr4"
    test_text = '''Quelques éléments lithiques Würm IV dispersés sont des indicateurs de la période néolithique d'environ fin 11000 - début 10000 av JC. 
    Un ensemble de fosses, circonscrit sur une surface de 35 m2, a livré du mobilier céramique du premier âge du Fer (Hallstatt C) et quelques éléments lithiques. 
    Un bâtiment sur poteaux se situe à une distance de 100 m vers l’ouest. 
    Pour la période de La Tène finale et gallo-romaine, l’ensemble des vestiges fossoyés et bâtis sont concentrés sur une parcelle à la croisée de deux chemins actuels présents sur le cadastre de 1807. 
    L’élément structurant majeur est le fossé F6 qui traverse perpendiculairement la parcelle, large de 3 m pour une profondeur de 1,80 m sous la terre arable. 
    Seul un angle de fossé, de nature différente et de plus petite taille, semble participer à cette même organisation du paysage. 
    Un bâtiment de plan rectangulaire, 13 x 9 m, sur fondations de schiste dont deux angles ont été découverts, est orienté de façon identique au fossé F6. 
    Il est très bien fondé sur une profondeur de 0,70 m avec de gros blocs de schiste. 
    Si quelques rares tessons du Haut-Empire ont été trouvés dans la fondation du bâtiment, le mobilier céramique du colmatage de la zone humide située à 10 m au sud-ouest, est compris entre le milieu du Ier siècle et le début du IIe siècle de notre ère. 
    Situé à 45 m plus au sud et parallèle au bâtiment, un fossé rectiligne de 3 m de large pour 1,80 m de profondeur sous la terre arable, scinde l’espace en deux. 
    Son creusement en V à été comblé en deux temps. 
    La première phase est une sédimentation naturelle qui a piégé quelques tessons protohistoriques et des scories ferreuses dont un culot de forge. 
    Le colmatage supérieur est composé de matériaux issus de la démolition avec de très nombreuses tuiles, des blocs de schiste brut ainsi que quelques tessons de céramique gallo-romaine. 
    De nombreux trous de poteaux et fosses se situent entre ces deux structures majeures. 
    Un angle de fossé dessinant l’amorce d’un enclos se développe au sud. Du mobilier La Tène finale a également été trouvé dans une fosse située dans cette espace. Un réseau fossoyé se développe à l’est, très érodé du côté nord. 
    Des fragments de céramique possiblement haut Moyen Âge ont été trouvés dans son comblement.'''

    test_text2 = '''Auteur : Sylvie Bocquet (Inrap) Numéro d’OA : 22 12 825 Responsable de l’opération : Sylvie Bocquet (Inrap) Nature de l’opération : OPD, du 20 novembre au 15 décembre 2017 YEAR Couverture géographique : Auvergne-Rhône-Alpes > Isère (38) > Gillonnay Code INSEE de la commune : 38 180 Mots-clés du thésaurus : France, Auvergne–Rhône-Alpes, Isère dép., silex, céramique, habitat rural à vocation agricole, structures de combustion, déchets de forge Chronologie PERIOD : Néolithique final PERIOD ou âge du Bronze ancien PERIOD à époque contemporaine PERIOD Peuples et cités : Keywords : Titre : Gillonnay Sous-titre : Les Olagnières, Gagnage La fouille urgente réalisée en novembre-décembre 2017 YEAR au lieu-dit Gagnage est intervenue en amont de l’extension des activités d’une gravière. Elle a été déclenchée suite à un signalement de vestiges. La parcelle fouillée se situe au sud-ouest de la commune, dans la plaine de la Bièvre. Le secteur est délimité au sud-est par la RD 119 ou « Axe de Bièvre » et à l’ouest par le chemin de Gillonnay à Bressieux, qui sert de limite entre les communes de La Côte-Saint-André et de Gillonnay. Les trois zones de fouille prescrites par le service régional de l’Archéologie couvrent 3 678 m². Cinq grandes périodes de mise en place et d’occupation du site ont été retenues. Elles s’échelonnent, après la stabilisation du paysage de la plaine à la fin de la DATEPREFIX période glaciaire PERIOD , entre le Néolithique final PERIOD ou l’ âge du Bronze ancien PERIOD et la période contemporaine PERIOD . L’état de conservation des vestiges apparaît médiocre. La platitude des terrains et la quasi-absence d’accumulation sédimentaire durant l’occupation ont, en effet, engendré des phénomènes de palimpseste, amplifiés par les activités agricoles qui ont accéléré l’érosion des vestiges. À la base de la séquence sédimentaire du site, un cailloutis alluvial gris renvoie à une forme non altérée de la terrasse fluvio-glaciaire FGyb. Il témoignerait de nappes caillouteuses, différenciées par un réseau de chenaux hétérométriques. Ceux-ci seraient en lien avec la mise en place d’un système fluvial en tresses s’écoulant vers l’ouest et la vallée du Rhône au Würm PERIOD récent. Au-dessus, se développe un sol fersiallitique, témoin de l’altération de la terrasse au post- glaciaire. Il est incisé par des paléochenaux dont les tracés ne se sont pas pérennisés. Ils indiquent un paysage instable, en lien avec la morphologie en cours de stabilisation du ruisseau du Rival (D’ap. K. Raynaud). Ces paléochenaux sont colmatés à partir du DATEPREFIX Néolithique final PERIOD ou de l’ âge du Bronze ancien PERIOD , d’après la présence d’un éclat en silex turonien PERIOD (étude S. Saintot) (Période 1). Durant la Protohistoire PERIOD , le paysage se stabilise avec un Rival dont le cours se cale au sud ; il s’écoule aujourd’hui à 620 m du site fouillé. À Gagnage, des tessons de céramique dispersés attestent une fréquentation au plus tard à La Tène finale PERIOD et au Ier s. CENTURYSPAN av. J.-C. DATESUFFIX (Période 2). Ces données ténues s’inscrivent toutefois dans un canevas de diverses occupations protohistoriques connues en plaine de la Bièvre, notamment sur les communes de La Côte-Saint-André, au Rival et aux Olagnières 13 I. Données administratives, techniques et scientifiques Inrap - Gillonnay (38), Les Olagnières, Gagnage (diagnostics sous la direction de S. CENTURYSPAN Bleu, Inrap, et fouilles sous la direction de S. CENTURYSPAN Bocquet, Inrap, et de C. Péquignot, Oxford Archéologie Méditerranée) et de Brézins, au Grand Plan (diagnostic sous la direction de F. Isnard, Inrap, et fouille sous la direction d’E. Courboin-Grésillaud, Eveha). Une occupation de la fin de la DATEPREFIX période antique PERIOD ou de l’ Antiquité tardive PERIOD est ensuite représentée par une structure de combustion, datée du milieu du DATEPREFIX IIIe - IVe s. CENTURYSPAN d’après une analyse radiocarbone sur charbons de bois (Période 3). Elle a servi de dépotoir pour différents rejets de l’artisanat du fer (étude S. Bigot). Ces derniers témoignent d’une activité de forge, dont la localisation est inconnue. Malgré quelques données acquises sur le site voisin de la Zac du Rival /Olagnières – Tranche 3, les modalités de l’occupation de la plaine restent très mal connues entre le IIIe s. et le Ve s. CENTURYSPAN La fosse de Gagnage constitue donc un jalon précieux. Elle fournit en outre des données paléoenvironnementales. En plus d’un approvisionnement en bois de chêne à feuillage caduc, pour l’activité de forge ou de combustion de la fosse, la proximité de cultures de printemps /été et d’automne / hiver apparaît dans les taxons de plantes sauvages adventives associés (étude M. Cabanis). D’autres mobiliers, en réemploi, évoquent la période antique PERIOD au sens large (tegulae, peson, clou), mais la collecte reste maigre et totalement dépourvue de mobilier céramique. Des trous de poteau, une fosse et des empierrements relèvent également de la période antique PERIOD ou du haut Moyen Âge PERIOD , sans précision possible. Les installations médiévales datent des VIe-VIIe s. CENTURYSPAN , d’après le mobilier céramique (Période 4). Elles regroupent une structure de combustion iden'''

    nlp = spacy.load(pipeline, disable=['ner'])
    # nlp.max_length = 2000000

    nlp.add_pipe("namedperiod_ruler", last=True, config={
                 "periodo_authority_id": periodo_authority_id})
    doc = nlp(test_text2.lower())

    for ent in doc.ents:
        print(ent.ent_id_, ent.text, ent.label_)
