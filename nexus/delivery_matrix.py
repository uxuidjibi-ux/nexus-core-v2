from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class ProjectTypology(StrEnum):
    DESIGN_SYSTEM_CASE_STUDY = "design_system_ux_case_study"
    COMPLEX_DIGITAL_PRODUCT = "saas_ecommerce_complex_website"


class LanguageVariant(BaseModel):
    code: Literal["fr", "en"]
    drive_folder: str
    title: str


class SlideDefinition(BaseModel):
    order: int = Field(ge=1)
    key: str
    title_fr: str
    title_en: str
    purpose: str
    required_visuals: list[str] = Field(default_factory=list)


class DeliverableDefinition(BaseModel):
    order: int = Field(ge=1)
    key: str
    kind: Literal["figma_file", "figma_slides", "document"]
    title_fr: str
    title_en: str
    owner_agent: Literal["PIXEL", "ATELIER"]
    page_equivalent: str | None = None
    required_sections: list[str] = Field(default_factory=list)
    slides: list[SlideDefinition] = Field(default_factory=list)


class BrandDocumentRules(BaseModel):
    preserve_official_logo: bool = True
    preserve_brand_palette: bool = True
    mirrored_bilingual_layout: bool = True
    required_signature: tuple[str, str, str] = (
        "PREPARED BY",
        "DJIGO DJIBI",
        "CX Consultant | Strategic Product & UX/UI Designer | AI Front-End Developer",
    )
    cover_structure: tuple[str, ...] = (
        "centered_title",
        "horizontal_rule",
        "prepared_by_block",
    )
    toc_page: int = 2
    introduction_starts_at_page: int = 3
    isolated_project_drive_folder: bool = True
    bilingual_drive_subfolders: tuple[str, str] = ("Français", "English")
    required_final_formats: tuple[str, str, str] = ("google_docs", "docx", "pdf")
    verify_drive_upload_before_handoff: bool = True


class DeliveryPlan(BaseModel):
    project_name: str
    typology: ProjectTypology
    languages: tuple[LanguageVariant, LanguageVariant]
    deliverables: list[DeliverableDefinition]
    brand_rules: BrandDocumentRules = Field(default_factory=BrandDocumentRules)
    external_standards: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_matrix(self) -> DeliveryPlan:
        expected = 3 if self.typology == ProjectTypology.DESIGN_SYSTEM_CASE_STUDY else 4
        if len(self.deliverables) != expected:
            raise ValueError(f"{self.typology} requires exactly {expected} deliverables")
        orders = [item.order for item in self.deliverables]
        if orders != list(range(1, expected + 1)):
            raise ValueError("Deliverable order must be contiguous and start at 1")
        if {language.drive_folder for language in self.languages} != {
            "Français",
            "English",
        }:
            raise ValueError(
                "Every project must use separate Français and English Drive folders"
            )
        return self


CASE_STUDY_SLIDES = [
    SlideDefinition(
        order=index,
        key=title_en.lower().replace(" ", "_").replace("&", "and"),
        title_fr=title_fr,
        title_en=title_en,
        purpose=purpose,
        required_visuals=visuals,
    )
    for index, (title_en, title_fr, purpose, visuals) in enumerate(
        (
            ("Cover Page", "Page de couverture", "Frame the case study.", ["brand mark"]),
            ("Project Overview", "Vue d’ensemble", "Summarize context and outcome.", ["summary"]),
            (
                "The Systemic Problem",
                "Le problème systémique",
                "Explain the interconnected problem.",
                ["systems map"],
            ),
            (
                "My Role & Leadership",
                "Mon rôle et leadership",
                "Clarify ownership and decisions.",
                ["responsibility map"],
            ),
            (
                "Research Methodology",
                "Méthodologie de recherche",
                "Show methods and evidence.",
                ["research timeline"],
            ),
            (
                "Evidence & Critical Questions",
                "Preuves et questions critiques",
                "Connect evidence to inquiry.",
                ["evidence matrix"],
            ),
            (
                "Stakeholder Ecosystem",
                "Écosystème des parties prenantes",
                "Map actors and dependencies.",
                ["stakeholder map"],
            ),
            ("Persona 1", "Persona 1", "Represent the first core user.", ["persona card"]),
            ("Persona 2", "Persona 2", "Represent the second core user.", ["persona card"]),
            ("Persona 3", "Persona 3", "Represent the third core user.", ["persona card"]),
            (
                "Storyboard Close-Up",
                "Storyboard — gros plan",
                "Show a key moment.",
                ["storyboard"],
            ),
            (
                "Storyboard Big Picture",
                "Storyboard — vue d’ensemble",
                "Show the end-to-end context.",
                ["journey storyboard"],
            ),
            (
                "User Flow & Task Analysis",
                "Flux utilisateur et analyse des tâches",
                "Detail actions and decisions.",
                ["flow diagram"],
            ),
            (
                "Information Architecture (IA)",
                "Architecture de l’information",
                "Describe content organization.",
                ["site map"],
            ),
            ("Empathy Map", "Carte d’empathie", "Synthesize user understanding.", ["empathy map"]),
            (
                "Conclusion & Strategic Impact",
                "Conclusion et impact stratégique",
                "Close with outcomes and next steps.",
                ["impact summary"],
            ),
        ),
        start=1,
    )
]


NEXUS_CORE_PLAN = DeliveryPlan(
    project_name="NEXUS CORE v2",
    typology=ProjectTypology.DESIGN_SYSTEM_CASE_STUDY,
    languages=(
        LanguageVariant(code="fr", drive_folder="Français", title="Version française"),
        LanguageVariant(code="en", drive_folder="English", title="English version"),
    ),
    deliverables=[
        DeliverableDefinition(
            order=1,
            key="full_ui_design_system",
            kind="figma_file",
            title_fr="Design System UI complet",
            title_en="Full UI Design System",
            owner_agent="PIXEL",
            required_sections=[
                "tokens",
                "typography",
                "brand_palette",
                "components",
                "variants",
                "auto_layout",
                "responsive_rules",
                "wcag_2_2_aa",
            ],
        ),
        DeliverableDefinition(
            order=2,
            key="ux_ui_case_study_deck",
            kind="figma_slides",
            title_fr="Étude de cas UX/UI interactive",
            title_en="Interactive UX/UI Case Study",
            owner_agent="PIXEL",
            slides=CASE_STUDY_SLIDES,
        ),
        DeliverableDefinition(
            order=3,
            key="ux_research_strategic_synthesis",
            kind="document",
            title_fr="Analyse de recherche UX et synthèse stratégique",
            title_en="UX Research Analysis and Strategic Synthesis",
            owner_agent="ATELIER",
            page_equivalent="10-12",
        ),
    ],
    external_standards=[
        "Nielsen Norman Group usability heuristics",
        "WCAG 2.2 Level AA",
        "W3C WAI accessible authentication and target size guidance",
    ],
)


AUTOCOMMERCE_PLAN = DeliveryPlan(
    project_name="Autocommerce",
    typology=ProjectTypology.COMPLEX_DIGITAL_PRODUCT,
    languages=(
        LanguageVariant(code="fr", drive_folder="Français", title="Version française"),
        LanguageVariant(code="en", drive_folder="English", title="English version"),
    ),
    deliverables=[
        DeliverableDefinition(
            order=1,
            key="functional_analysis",
            kind="document",
            title_fr="Analyse fonctionnelle globale et architecture SaaS/Web",
            title_en="Global Functional Analysis and SaaS/Web Architecture",
            owner_agent="ATELIER",
            page_equivalent="10-12",
        ),
        DeliverableDefinition(
            order=2,
            key="market_benchmark",
            kind="document",
            title_fr="Étude comparative du marché et benchmark concurrentiel",
            title_en="Market Study and Competitive Benchmark",
            owner_agent="ATELIER",
            page_equivalent="10-12",
        ),
        DeliverableDefinition(
            order=3,
            key="applied_methodology",
            kind="document",
            title_fr="Méthodologie appliquée — prompts, modèles IA et sources",
            title_en="Applied Methodology — Prompts, AI Models and Sources",
            owner_agent="ATELIER",
            page_equivalent="10-12",
        ),
        DeliverableDefinition(
            order=4,
            key="mvp_specifications",
            kind="document",
            title_fr="Spécifications techniques du MVP — Figma et Make/ReadyAI",
            title_en="MVP Technical Specifications — Figma and Make/ReadyAI",
            owner_agent="ATELIER",
            page_equivalent="10-12",
        ),
    ],
    external_standards=[
        "Nielsen Norman Group usability heuristics and faceted-filter guidance",
        "WCAG 2.2 Level AA",
        "PIPEDA and applicable provincial privacy requirements",
        "Competition Bureau Canada transparent pricing guidance",
        "Automotive VIN, listing quality, and marketplace trust practices",
    ],
)


DELIVERY_PLANS = {
    NEXUS_CORE_PLAN.project_name.casefold(): NEXUS_CORE_PLAN,
    AUTOCOMMERCE_PLAN.project_name.casefold(): AUTOCOMMERCE_PLAN,
}


def delivery_plan_for(project_name: str) -> DeliveryPlan:
    try:
        return DELIVERY_PLANS[project_name.strip().casefold()]
    except KeyError as exc:
        raise ValueError(
            "Project typology and exact deliverable matrix must be confirmed before execution"
        ) from exc
