import pytest

from tools.figma_tool import FigmaTool


def test_figma_manifest_is_bilingual_and_deterministic():
    tool = FigmaTool("test-token")
    manifest = tool.build_case_study_manifest(
        project_name="NEXUS CORE v2",
        language="fr",
        slides=[{"order": 1, "title": "Couverture"}],
    )
    tool.close()
    assert manifest["canvas"]["ratio"] == "16:9"
    assert manifest["layout"]["engine"] == "auto-layout-v2"


def test_figma_manifest_rejects_invalid_slide_order():
    tool = FigmaTool("test-token")
    with pytest.raises(ValueError, match="contiguous"):
        tool.build_case_study_manifest(
            project_name="NEXUS CORE v2",
            language="en",
            slides=[{"order": 2, "title": "Overview"}],
        )
    tool.close()
