from tools.code_runner_tool import CodeRunnerTool


def test_runner_executes_inside_root(tmp_path):
    script = tmp_path / "hello.py"
    script.write_text("print('nexus')", encoding="utf-8")
    result = CodeRunnerTool(tmp_path).run_file("python", "hello.py")
    assert result.returncode == 0
    assert result.stdout.strip() == "nexus"


def test_runner_rejects_escape(tmp_path):
    runner = CodeRunnerTool(tmp_path)
    try:
        runner.run_file("python", "../outside.py")
    except ValueError as exc:
        assert "SANDBOX_ROOT" in str(exc)
    else:
        raise AssertionError("Expected escape to be rejected")
