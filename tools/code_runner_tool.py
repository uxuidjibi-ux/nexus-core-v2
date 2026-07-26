from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Literal

from pydantic import BaseModel


class ExecutionResult(BaseModel):
    command: list[str]
    returncode: int
    stdout: str
    stderr: str
    timed_out: bool = False


class CodeRunnerTool:
    """Small local runner. Production should replace this with an isolated container service."""

    ALLOWED: dict[str, tuple[str, ...]] = {
        "python": (sys.executable, "-I"),
        "node": ("node", "--disable-proto=delete"),
    }

    def __init__(self, root: Path, timeout_seconds: int = 20):
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.timeout_seconds = timeout_seconds

    def run_file(self, runtime: Literal["python", "node"], relative_path: str) -> ExecutionResult:
        target = (self.root / relative_path).resolve()
        if self.root not in target.parents or not target.is_file():
            raise ValueError("Execution target must be an existing file inside SANDBOX_ROOT")
        command = [*self.ALLOWED[runtime], str(target)]
        env = {"PATH": os.environ.get("PATH", ""), "LANG": "C.UTF-8", "NO_COLOR": "1"}
        try:
            # Command prefix is selected from ALLOWED and target is root-contained.
            completed = subprocess.run(  # noqa: S603
                command,
                cwd=self.root,
                env=env,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                check=False,
            )
            return ExecutionResult(
                command=command,
                returncode=completed.returncode,
                stdout=completed.stdout[-20_000:],
                stderr=completed.stderr[-20_000:],
            )
        except subprocess.TimeoutExpired as exc:
            return ExecutionResult(
                command=command,
                returncode=124,
                stdout=(exc.stdout or "")[-20_000:],
                stderr=(exc.stderr or "")[-20_000:],
                timed_out=True,
            )
