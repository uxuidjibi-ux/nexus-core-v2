from tools.wordpress_tool import WordPressTool


def test_wordpress_dry_run_never_publishes():
    tool = WordPressTool("https://example.test", "user", "secret", dry_run=True)
    result = tool.create_post("Title", "Body", status="publish")
    assert result["dry_run"] is True
    tool.close()
