from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
ASSETS = Path("/tmp/autocommerce-doc1-assets")
OUTPUT = ROOT / "artifacts" / "Autocommerce" / "document-01"

CHARCOAL = "202020"
RED = "E00810"
GREEN = "104830"
LIGHT = "F4F5F6"
MID = "D9DDE1"
WHITE = "FFFFFF"

SIGNATURE = (
    "PREPARED BY",
    "DJIGO DJIBI",
    "CX Consultant | Strategic Product & UX/UI Designer | AI Front-End Developer",
)

FR = {
    "code": "FR",
    "title": "Analyse fonctionnelle globale\n& Architecture SaaS/Web",
    "subtitle": "AUTOCOMMERCE · DOCUMENT 01",
    "toc": "Table des matières",
    "confidential": "AUTOCOMMERCE · CONFIDENTIEL",
    "pages": [
        (
            "Introduction et mandat",
            [
                (
                    "Objectif",
                    "Évaluer les écrans existants d’AutoCommerce, transformer les annotations "
                    "fournies en exigences actionnables et définir une architecture fonctionnelle "
                    "pour un MVP Figma/Make distinctif, simple et crédible.",
                ),
                (
                    "Positionnement",
                    "AutoCommerce demeure propriétaire du produit. La plateforme sert trois "
                    "publics : acheteurs, vendeurs/commerçants et équipe d’administration "
                    "AutoCommerce. Cars.ca constitue la référence de couverture fonctionnelle, "
                    "sans reproduction de son identité ou de son interface.",
                ),
                (
                    "Principe directeur",
                    "Simple au premier regard, puissant à la demande. Les véhicules et l’action "
                    "principale restent dominants; filtres, analyses et fonctions expertes se "
                    "déploient progressivement.",
                ),
            ],
        ),
        (
            "Périmètre observé et méthode",
            [
                (
                    "Corpus",
                    "Le corpus comprend 18 pages de captures annotées : accueil, navigation Buy, "
                    "inventaire, modes liste et galerie, fiche véhicule, achat immédiat, enchères, "
                    "vente, authentification, tableau de bord et assistant Add Vehicle.",
                ),
                (
                    "Méthode d’évaluation",
                    "Chaque écran est analysé selon l’objectif utilisateur, la hiérarchie visuelle, "
                    "la charge cognitive, la cohérence, les erreurs possibles, l’accessibilité, "
                    "la confiance et la capacité responsive. Les constats sont rapprochés des "
                    "heuristiques de Nielsen Norman Group et de WCAG 2.2 AA.",
                ),
                (
                    "Limites",
                    "Les captures ne démontrent pas tous les comportements, règles métier ni états "
                    "d’erreur. Les recommandations décrivent donc les exigences à valider dans le "
                    "prototype, et non un audit du code de production.",
                ),
            ],
        ),
        (
            "Accueil et navigation globale",
            [
                (
                    "Constat",
                    "L’accueil repose sur une forte dominante noire et une animation automobile. "
                    "L’identité est reconnaissable, mais la proposition de valeur, les chemins "
                    "Acheter/Vendre et la prochaine action ne sont pas suffisamment explicites.",
                ),
                (
                    "Recommandation",
                    "Conserver le logo, le noir, le rouge et le vert historiques, tout en faisant "
                    "du blanc et du gris clair les surfaces principales. Installer une recherche "
                    "centrale, deux entrées Acheter/Vendre, des preuves de confiance et un accès "
                    "direct au tableau de bord.",
                ),
                (
                    "Navigation cible",
                    "En-tête compact et persistant : logo, Acheter, Vendre, Enchères, Services, "
                    "Aide, langue et compte. Sur mobile, conserver Recherche, Favoris, Vendre et "
                    "Compte dans une navigation basse accessible au pouce.",
                ),
            ],
        ),
        (
            "Inventaire, recherche et filtres",
            [
                (
                    "Problème principal",
                    "L’annotation confirme que le filtre latéral statique prend trop de place. "
                    "Il réduit la surface d’inventaire et concurrence les véhicules. Le méga-menu "
                    "Inventory occupe également l’écran avec trop d’options simultanées.",
                ),
                (
                    "Solution fonctionnelle",
                    "Remplacer le panneau permanent par un tiroir rétractable sur ordinateur et "
                    "une feuille modale sur mobile. Les critères actifs deviennent des pastilles "
                    "supprimables. La fermeture du filtre conserve les choix et restaure toute la "
                    "largeur des résultats.",
                ),
                (
                    "Filtres prioritaires",
                    "Localisation, distance, marque, modèle, année, prix, kilométrage, carrosserie, "
                    "carburant, transmission, traction, état, vendeur et disponibilité. Les filtres "
                    "experts restent regroupés dans « Plus de critères ».",
                ),
            ],
        ),
        (
            "Résultats et fiche véhicule",
            [
                (
                    "Modes d’exploration",
                    "Les modes liste et galerie existent déjà. Ils doivent partager les mêmes "
                    "données, filtres et états. Une vue carte peut être ajoutée ultérieurement. "
                    "Le changement de vue ne doit jamais réinitialiser la recherche.",
                ),
                (
                    "Carte véhicule",
                    "Photo principale, année-marque-modèle, version, kilométrage, localisation, "
                    "prix total, badge de confiance, vendeur et actions Favori/Comparer. Les "
                    "actions Acheter maintenant, Faire une offre et Contacter doivent respecter "
                    "une hiérarchie constante.",
                ),
                (
                    "Fiche détaillée",
                    "Galerie plein écran, résumé du prix, historique, état, équipements, vendeur, "
                    "financement indicatif, disponibilité et actions. Les informations critiques "
                    "restent visibles pendant le défilement sans masquer le contenu.",
                ),
            ],
        ),
        (
            "Achat immédiat et enchères",
            [
                (
                    "Achat immédiat",
                    "Le parcours Buy Now doit afficher le prix total disponible, les frais "
                    "obligatoires, les conditions, l’identité du vendeur et la prochaine étape "
                    "avant tout engagement. Aucun prix d’appel inaccessible ne doit être utilisé.",
                ),
                (
                    "Offre",
                    "Faire une offre nécessite un montant, une échéance, un récapitulatif et une "
                    "confirmation. Les états envoyée, consultée, acceptée, refusée, expirée et "
                    "contre-offre doivent être visibles dans le tableau de bord.",
                ),
                (
                    "Enchères",
                    "L’état vide actuel doit devenir utile : explication, calendrier, alertes et "
                    "véhicules à venir. Une enchère active exige heure serveur, mise actuelle, "
                    "incrément, dépôt, historique, prolongation anti-sniping et confirmation.",
                ),
            ],
        ),
        (
            "Vente et cycle de vie des annonces",
            [
                (
                    "Cycle cible",
                    "Brouillon → contrôle qualité → en attente de validation → active → réservée "
                    "→ vendue, expirée ou refusée. Chaque statut doit expliquer la cause, les "
                    "actions disponibles et la prochaine étape.",
                ),
                (
                    "Tableau de bord commerçant",
                    "Vue synthétique des stocks, annonces à corriger, prospects chauds, rendez-vous, "
                    "offres, délais de réponse et ventes. Des vues Inventaire, Prospects, Messages, "
                    "Analytique, Équipe et Paramètres complètent le pilotage.",
                ),
                (
                    "Productivité",
                    "Recherche globale, filtres sauvegardés, actions groupées, duplication contrôlée, "
                    "import CSV/API, attribution des prospects et journal d’activité réduisent la "
                    "charge opérationnelle des commerçants.",
                ),
            ],
        ),
        (
            "Assistant d’ajout d’un véhicule",
            [
                (
                    "Structure existante",
                    "Les captures montrent quatre étapes : détails du véhicule, pneus, photos et "
                    "dommages, description. Le formulaire contient de nombreux choix utiles, mais "
                    "la densité et les listes de pastilles augmentent l’effort et le risque d’erreur.",
                ),
                (
                    "Parcours recommandé",
                    "1) VIN ou saisie manuelle; 2) caractéristiques vérifiées; 3) état et pneus; "
                    "4) photos guidées; 5) prix et description; 6) prévisualisation. Une sauvegarde "
                    "automatique et un indicateur de progression accompagnent chaque étape.",
                ),
                (
                    "Assistance intelligente",
                    "Le VIN préremplit les données disponibles sans verrouiller la correction. "
                    "L’analyse photo détecte flou, doublons et angles manquants. Une description "
                    "assistée résume les faits validés et reste entièrement modifiable.",
                ),
            ],
        ),
        (
            "Rôles, tableaux de bord et permissions",
            [
                (
                    "Acheteur",
                    "Favoris, comparateur, recherches et alertes, messages, rendez-vous, offres, "
                    "documents et progression d’achat.",
                ),
                (
                    "Vendeur ou commerçant",
                    "Inventaire, création d’annonce, score qualité, recommandations de prix, "
                    "prospects, tâches, performance, équipe et exports.",
                ),
                (
                    "AutoCommerce",
                    "Comptes, commerçants, modération, règles de publication, abonnements, fraude, "
                    "litiges, qualité, revenus, conversion, journal d’audit et contrôle d’accès.",
                ),
                (
                    "Permissions",
                    "Administrateur propriétaire, gestionnaire, vendeur, marketing et lecture seule. "
                    "Appliquer le moindre privilège, l’authentification renforcée pour les actions "
                    "sensibles et un historique traçable.",
                ),
            ],
        ),
        (
            "Architecture fonctionnelle cible",
            [
                (
                    "Couche expérience",
                    "Web responsive et prototype Figma couvrant accueil, recherche, résultats, fiche, "
                    "compte, vente et administration. Les composants partagent tokens, états et règles "
                    "d’accessibilité.",
                ),
                (
                    "Services métier",
                    "Catalogue, recherche, comptes, organisations, annonces, médias, offres, enchères, "
                    "prospects, messagerie, notifications, tarification, modération et analytique.",
                ),
                (
                    "Automatisation MVP",
                    "Make simule la réception VIN, le contrôle photo, la génération de brouillon, "
                    "l’alerte de validation et la notification de prospect. Les scénarios utilisent "
                    "des données fictives et des webhooks idempotents.",
                ),
                (
                    "Données et sécurité",
                    "Séparer utilisateurs, organisations, véhicules, annonces, médias et événements. "
                    "Consentement, minimisation, chiffrement, rétention, accès et suppression doivent "
                    "être définis avant toute production.",
                ),
            ],
        ),
        (
            "Priorités, critères d’acceptation et synthèse",
            [
                (
                    "Priorité MVP",
                    "Recherche et filtres rétractables; liste/galerie; fiche véhicule; connexion; "
                    "tableau de bord commerçant; assistant VIN/photos/description; modération "
                    "AutoCommerce; prototype responsive et accessible.",
                ),
                (
                    "Critères clés",
                    "Le filtre se ferme sans perdre les choix; toutes les actions sont utilisables "
                    "au clavier; le focus reste visible; les cibles tactiles respectent WCAG 2.2; "
                    "les erreurs sont explicites; la saisie est sauvegardée; les prix obligatoires "
                    "sont transparents; les rôles limitent réellement l’accès.",
                ),
                (
                    "Décision",
                    "AutoCommerce ne doit pas être une copie supplémentaire d’un marché automobile. "
                    "Sa différence est un système de vente assistée : inventaire plus lisible pour "
                    "l’acheteur, publication accélérée pour le commerçant et contrôle central de la "
                    "qualité pour AutoCommerce.",
                ),
            ],
        ),
    ],
    "sources": [
        "Capture AutoCommerce fournie — 18 pages annotées, 2026.",
        "Nielsen Norman Group — 10 Usability Heuristics for User Interface Design.",
        "Nielsen Norman Group — Defining Helpful Filter Categories and Values for Better UX.",
        "W3C Web Accessibility Initiative — WCAG 2.2.",
        "Office of the Privacy Commissioner of Canada — PIPEDA requirements in brief.",
        "Competition Bureau Canada — Drip pricing.",
    ],
}

EN = {
    "code": "EN",
    "title": "Global Functional Analysis\n& SaaS/Web Architecture",
    "subtitle": "AUTOCOMMERCE · DOCUMENT 01",
    "toc": "Table of Contents",
    "confidential": "AUTOCOMMERCE · CONFIDENTIAL",
    "pages": [
        (
            "Introduction and mandate",
            [
                (
                    "Objective",
                    "Assess the current AutoCommerce screens, convert the supplied annotations into "
                    "actionable requirements, and define a functional architecture for a distinctive, "
                    "simple and credible Figma/Make MVP.",
                ),
                (
                    "Positioning",
                    "AutoCommerce remains the product owner. The platform serves buyers, private or "
                    "professional sellers, and the AutoCommerce administration team. Cars.ca is the "
                    "functional coverage reference, without reproducing its identity or interface.",
                ),
                (
                    "Guiding principle",
                    "Simple at first sight, powerful on demand. Vehicles and the primary action remain "
                    "dominant; filters, analytics and expert capabilities progressively appear.",
                ),
            ],
        ),
        (
            "Observed scope and method",
            [
                (
                    "Evidence set",
                    "The evidence includes 18 annotated pages: home, Buy navigation, inventory, list "
                    "and gallery modes, vehicle detail, Buy Now, auctions, selling, authentication, "
                    "dashboard and the Add Vehicle assistant.",
                ),
                (
                    "Evaluation method",
                    "Each screen is assessed against user intent, visual hierarchy, cognitive load, "
                    "consistency, error exposure, accessibility, trust and responsive behaviour. "
                    "Findings are compared with Nielsen Norman Group heuristics and WCAG 2.2 AA.",
                ),
                (
                    "Limitations",
                    "Static captures do not reveal every behaviour, business rule or error state. "
                    "Recommendations therefore define requirements to validate in the prototype, "
                    "not a production-code audit.",
                ),
            ],
        ),
        (
            "Home and global navigation",
            [
                (
                    "Finding",
                    "The home experience relies on a strong black surface and automotive animation. "
                    "The identity is recognizable, but the value proposition, Buy/Sell paths and "
                    "next best action are not explicit enough.",
                ),
                (
                    "Recommendation",
                    "Retain the logo and established black, red and green while making white and light "
                    "grey the primary surfaces. Add central search, clear Buy/Sell entrances, trust "
                    "evidence and direct dashboard access.",
                ),
                (
                    "Target navigation",
                    "Compact persistent header: logo, Buy, Sell, Auctions, Services, Help, language "
                    "and account. On mobile, keep Search, Favourites, Sell and Account in a "
                    "thumb-accessible bottom navigation.",
                ),
            ],
        ),
        (
            "Inventory, search and filters",
            [
                (
                    "Primary issue",
                    "The annotation confirms that the static filter sidebar consumes too much space. "
                    "It reduces inventory visibility and competes with vehicle content. The Inventory "
                    "mega-menu also overwhelms the screen with simultaneous options.",
                ),
                (
                    "Functional solution",
                    "Replace the permanent sidebar with a collapsible desktop drawer and mobile bottom "
                    "sheet. Active criteria become removable chips. Closing filters preserves choices "
                    "and returns the full result width.",
                ),
                (
                    "Priority filters",
                    "Location, distance, make, model, year, price, mileage, body, fuel, transmission, "
                    "drivetrain, condition, seller and availability. Expert criteria remain under "
                    "“More filters.”",
                ),
            ],
        ),
        (
            "Results and vehicle detail",
            [
                (
                    "Exploration modes",
                    "List and gallery modes already exist. They must share the same data, filters and "
                    "states. A map can follow later. Changing view must never reset the search.",
                ),
                (
                    "Vehicle card",
                    "Primary image, year-make-model, trim, mileage, location, total price, confidence "
                    "badge, seller and Favourite/Compare actions. Buy Now, Make an Offer and Contact "
                    "must follow one consistent hierarchy.",
                ),
                (
                    "Detail page",
                    "Full gallery, price summary, history, condition, equipment, seller, indicative "
                    "financing, availability and actions. Critical information remains available "
                    "during scroll without masking the content.",
                ),
            ],
        ),
        (
            "Buy Now and auctions",
            [
                (
                    "Immediate purchase",
                    "Buy Now must show the attainable total price, mandatory fees, conditions, seller "
                    "identity and next step before commitment. Unattainable teaser pricing must not "
                    "be used.",
                ),
                (
                    "Offers",
                    "Making an offer requires an amount, expiry, summary and confirmation. Sent, viewed, "
                    "accepted, declined, expired and counter-offer states belong in the dashboard.",
                ),
                (
                    "Auctions",
                    "The current empty state should explain the service, show a calendar, enable alerts "
                    "and surface upcoming vehicles. A live auction needs server time, current bid, "
                    "increment, deposit, history, anti-sniping extension and confirmation.",
                ),
            ],
        ),
        (
            "Selling and listing lifecycle",
            [
                (
                    "Target lifecycle",
                    "Draft → quality check → pending approval → active → reserved → sold, expired or "
                    "declined. Every status must explain the reason, available action and next step.",
                ),
                (
                    "Dealer dashboard",
                    "Executive view of stock, listings to fix, hot leads, appointments, offers, response "
                    "times and sales. Inventory, Leads, Messages, Analytics, Team and Settings support "
                    "operational work.",
                ),
                (
                    "Productivity",
                    "Global search, saved filters, bulk actions, controlled duplication, CSV/API import, "
                    "lead assignment and activity history reduce dealer workload.",
                ),
            ],
        ),
        (
            "Add Vehicle assistant",
            [
                (
                    "Current structure",
                    "The captures show four steps: vehicle details, tyres, photos and damage, and "
                    "description. Many useful choices exist, but dense tags and long lists increase "
                    "effort and error risk.",
                ),
                (
                    "Recommended journey",
                    "1) VIN or manual entry; 2) verified specifications; 3) condition and tyres; "
                    "4) guided photos; 5) price and description; 6) preview. Autosave and progress "
                    "feedback support every step.",
                ),
                (
                    "Intelligent assistance",
                    "VIN pre-fills available data without blocking correction. Photo analysis detects "
                    "blur, duplicates and missing angles. Assisted copy summarizes verified facts "
                    "and remains fully editable.",
                ),
            ],
        ),
        (
            "Roles, dashboards and permissions",
            [
                (
                    "Buyer",
                    "Favourites, comparison, saved searches and alerts, messages, appointments, offers, "
                    "documents and purchase progress.",
                ),
                (
                    "Seller or dealer",
                    "Inventory, listing assistant, quality score, price recommendations, leads, tasks, "
                    "performance, team and exports.",
                ),
                (
                    "AutoCommerce",
                    "Accounts, dealers, moderation, publication rules, subscriptions, fraud, disputes, "
                    "quality, revenue, conversion, audit log and access control.",
                ),
                (
                    "Permissions",
                    "Owner administrator, manager, salesperson, marketing and read-only. Apply least "
                    "privilege, stronger authentication for sensitive actions and traceable history.",
                ),
            ],
        ),
        (
            "Target functional architecture",
            [
                (
                    "Experience layer",
                    "Responsive web and Figma prototype covering home, search, results, detail, account, "
                    "selling and administration. Components share tokens, states and accessibility rules.",
                ),
                (
                    "Business services",
                    "Catalogue, search, identity, organizations, listings, media, offers, auctions, leads, "
                    "messaging, notifications, pricing, moderation and analytics.",
                ),
                (
                    "MVP automation",
                    "Make simulates VIN intake, photo checks, draft generation, approval alerts and lead "
                    "notifications. Scenarios use fictional data and idempotent webhooks.",
                ),
                (
                    "Data and security",
                    "Separate users, organizations, vehicles, listings, media and events. Consent, "
                    "minimization, encryption, retention, access and deletion must be defined before "
                    "production.",
                ),
            ],
        ),
        (
            "Priorities, acceptance criteria and conclusion",
            [
                (
                    "MVP priority",
                    "Search and collapsible filters; list/gallery; vehicle detail; authentication; dealer "
                    "dashboard; VIN/photo/description assistant; AutoCommerce moderation; responsive and "
                    "accessible prototype.",
                ),
                (
                    "Key criteria",
                    "Filters close without losing choices; all actions work by keyboard; focus remains "
                    "visible; touch targets meet WCAG 2.2; errors are explicit; entry is saved; mandatory "
                    "prices are transparent; roles genuinely restrict access.",
                ),
                (
                    "Decision",
                    "AutoCommerce should not become another copy of an automotive marketplace. Its "
                    "difference is assisted selling: clearer inventory for buyers, faster publishing "
                    "for dealers and centralized quality control for AutoCommerce.",
                ),
            ],
        ),
    ],
    "sources": [
        "Supplied AutoCommerce capture — 18 annotated pages, 2026.",
        "Nielsen Norman Group — 10 Usability Heuristics for User Interface Design.",
        "Nielsen Norman Group — Defining Helpful Filter Categories and Values for Better UX.",
        "W3C Web Accessibility Initiative — WCAG 2.2.",
        "Office of the Privacy Commissioner of Canada — PIPEDA requirements in brief.",
        "Competition Bureau Canada — Drip pricing.",
    ],
}

IMAGE_BY_PAGE = {
    3: Path("/tmp/autocommerce-pdf-pages/page-02.jpg"),
    4: Path("/tmp/autocommerce-pdf-pages/page-04.jpg"),
    5: Path("/tmp/autocommerce-pdf-pages/page-06.jpg"),
    6: Path("/tmp/autocommerce-pdf-pages/page-06.jpg"),
    7: Path("/tmp/autocommerce-pdf-pages/page-09.jpg"),
    8: Path("/tmp/autocommerce-pdf-pages/page-14.jpg"),
    9: Path("/tmp/autocommerce-pdf-pages/page-13.jpg"),
    10: Path("/tmp/autocommerce-pdf-pages/page-18.jpg"),
}


def set_cell_shading(cell, fill: str) -> None:
    properties = cell._tc.get_or_add_tcPr()
    shading = OxmlElement("w:shd")
    shading.set(qn("w:fill"), fill)
    properties.append(shading)


def set_repeat_table_header(row) -> None:
    properties = row._tr.get_or_add_trPr()
    repeat = OxmlElement("w:tblHeader")
    repeat.set(qn("w:val"), "true")
    properties.append(repeat)


def add_page_number(paragraph) -> None:
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = paragraph.add_run()
    field_begin = OxmlElement("w:fldChar")
    field_begin.set(qn("w:fldCharType"), "begin")
    instruction = OxmlElement("w:instrText")
    instruction.set(qn("xml:space"), "preserve")
    instruction.text = "PAGE"
    field_end = OxmlElement("w:fldChar")
    field_end.set(qn("w:fldCharType"), "end")
    run._r.extend((field_begin, instruction, field_end))


def configure_document(document: Document, language: dict) -> None:
    section = document.sections[0]
    section.page_height = Inches(11.69)
    section.page_width = Inches(8.27)
    section.top_margin = Inches(0.68)
    section.bottom_margin = Inches(0.62)
    section.left_margin = Inches(0.72)
    section.right_margin = Inches(0.72)

    for style_name, size, colour in (
        ("Normal", 9.3, CHARCOAL),
        ("Title", 27, CHARCOAL),
        ("Heading 1", 20, CHARCOAL),
        ("Heading 2", 12.5, GREEN),
    ):
        style = document.styles[style_name]
        style.font.name = "Arial"
        style.font.size = Pt(size)
        style.font.color.rgb = RGBColor.from_string(colour)
    document.styles["Title"].font.bold = True
    document.styles["Heading 1"].font.bold = True
    document.styles["Heading 2"].font.bold = True
    document.styles["Normal"].paragraph_format.space_after = Pt(4)
    document.styles["Normal"].paragraph_format.line_spacing = 1.05

    footer = section.footer.paragraphs[0]
    footer.text = language["confidential"]
    footer.runs[0].font.name = "Arial"
    footer.runs[0].font.size = Pt(8)
    footer.runs[0].font.color.rgb = RGBColor.from_string(CHARCOAL)
    page = section.footer.add_paragraph()
    add_page_number(page)


def add_brand_bar(document: Document, label: str) -> None:
    table = document.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(1.35)
    table.columns[1].width = Inches(5.25)
    logo = ASSETS / "logo.png"
    if logo.exists():
        table.cell(0, 0).paragraphs[0].add_run().add_picture(str(logo), width=Inches(1.05))
    table.cell(0, 1).text = label
    for cell in table.rows[0].cells:
        set_cell_shading(cell, CHARCOAL)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        for run in cell.paragraphs[0].runs:
            run.font.name = "Arial"
            run.font.size = Pt(9)
            run.font.bold = True
            run.font.color.rgb = RGBColor.from_string(WHITE)


def add_cover(document: Document, language: dict) -> None:
    add_brand_bar(document, language["subtitle"])
    document.add_paragraph()
    document.add_paragraph()
    title = document.add_paragraph(language["title"], style="Title")
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.paragraph_format.space_before = Pt(80)
    title.paragraph_format.space_after = Pt(18)
    rule = document.add_paragraph("━" * 42)
    rule.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rule.runs[0].font.color.rgb = RGBColor.from_string(RED)
    rule.runs[0].font.size = Pt(10)
    document.add_paragraph()
    signature = document.add_paragraph("\n".join(SIGNATURE))
    signature.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for index, run in enumerate(signature.runs):
        run.font.name = "Arial"
        run.font.size = Pt(10 if index else 11)
        run.font.bold = True
    date_line = document.add_paragraph("JULY 2026")
    date_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    date_line.runs[0].font.color.rgb = RGBColor.from_string(GREEN)
    date_line.runs[0].font.bold = True


def add_toc(document: Document, language: dict) -> None:
    add_brand_bar(document, language["toc"])
    heading = document.add_paragraph(language["toc"], style="Title")
    heading.paragraph_format.space_before = Pt(24)
    table = document.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    headers = ("SECTION", "PAGE")
    for index, header in enumerate(headers):
        cell = table.rows[0].cells[index]
        cell.text = header
        set_cell_shading(cell, CHARCOAL)
        for run in cell.paragraphs[0].runs:
            run.font.bold = True
            run.font.color.rgb = RGBColor.from_string(WHITE)
    set_repeat_table_header(table.rows[0])
    for page_number, (title, _) in enumerate(language["pages"], start=3):
        cells = table.add_row().cells
        cells[0].text = f"{page_number - 2:02d}  {title}"
        cells[1].text = str(page_number)
        if page_number % 2 == 0:
            set_cell_shading(cells[0], LIGHT)
            set_cell_shading(cells[1], LIGHT)


def add_evidence_image(document: Document, page_number: int) -> None:
    image = IMAGE_BY_PAGE.get(page_number)
    if not image or not image.exists():
        return
    paragraph = document.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.add_run().add_picture(str(image), width=Inches(3.35))
    caption = document.add_paragraph(
        f"Source evidence · supplied AutoCommerce capture · page {page_number}"
    )
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    caption.runs[0].font.size = Pt(7.5)
    caption.runs[0].font.italic = True
    caption.runs[0].font.color.rgb = RGBColor.from_string("666666")


def add_analysis_page(
    document: Document,
    language: dict,
    content_index: int,
    title: str,
    sections: list[tuple[str, str]],
) -> None:
    page_number = content_index + 3
    add_brand_bar(document, f"{content_index + 1:02d} · {title.upper()}")
    heading = document.add_paragraph(title, style="Heading 1")
    heading.paragraph_format.space_before = Pt(12)
    for section_title, body in sections:
        subheading = document.add_paragraph(section_title, style="Heading 2")
        subheading.paragraph_format.space_before = Pt(6)
        paragraph = document.add_paragraph(body)
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    if page_number in IMAGE_BY_PAGE:
        add_evidence_image(document, page_number)

    if content_index == len(language["pages"]) - 1:
        document.add_paragraph("Sources", style="Heading 2")
        for source in language["sources"]:
            document.add_paragraph(source, style="List Bullet")


def build(language: dict) -> Path:
    document = Document()
    configure_document(document, language)
    add_cover(document, language)
    document.add_page_break()
    add_toc(document, language)
    for index, (title, sections) in enumerate(language["pages"]):
        document.add_page_break()
        add_analysis_page(document, language, index, title, sections)

    OUTPUT.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT / f"autocommerce-document-01-{language['code'].lower()}.docx"
    document.save(output_path)
    return output_path


if __name__ == "__main__":
    for payload in (FR, EN):
        print(build(payload))
