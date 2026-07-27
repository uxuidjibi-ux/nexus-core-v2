from pathlib import Path

from tools.drive_tool import DriveTool


def test_drive_upload_is_dry_run_and_language_tagged(tmp_path: Path):
    source = tmp_path / "report.pdf"
    source.write_bytes(b"%PDF")
    tool = DriveTool("test-token")
    result = tool.upload_document(source, language="fr", parent_id="folder-id")
    tool.close()
    assert result["dry_run"] is True
    assert result["metadata"]["appProperties"]["nexusLanguage"] == "fr"
    assert result["metadata"]["parents"] == ["folder-id"]
