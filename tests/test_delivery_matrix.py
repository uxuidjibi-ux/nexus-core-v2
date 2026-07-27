import pytest

from nexus.delivery_matrix import (
    AUTOCOMMERCE_PLAN,
    NEXUS_CORE_PLAN,
    ProjectTypology,
    delivery_plan_for,
)


def test_nexus_core_has_exactly_three_deliverables_and_sixteen_slides():
    assert NEXUS_CORE_PLAN.typology == ProjectTypology.DESIGN_SYSTEM_CASE_STUDY
    assert len(NEXUS_CORE_PLAN.deliverables) == 3
    assert len(NEXUS_CORE_PLAN.deliverables[1].slides) == 16


def test_autocommerce_has_exactly_four_bilingual_documents():
    assert len(AUTOCOMMERCE_PLAN.deliverables) == 4
    assert {language.code for language in AUTOCOMMERCE_PLAN.languages} == {"fr", "en"}
    assert all(item.kind == "document" for item in AUTOCOMMERCE_PLAN.deliverables)


def test_unknown_project_requires_confirmation():
    with pytest.raises(ValueError, match="must be confirmed"):
        delivery_plan_for("Unconfirmed Project")
