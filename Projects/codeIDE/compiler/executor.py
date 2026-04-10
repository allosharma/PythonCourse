from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass


MAX_EXECUTION_SECONDS = 5
MAX_OUTPUT_CHARACTERS = 12000


@dataclass
class ExecutionResult:
    stdout: str
    stderr: str
    returncode: int | None
    duration_ms: int
    timed_out: bool = False


def run_python_code(source_code: str, stdin: str = "") -> ExecutionResult:
    with tempfile.TemporaryDirectory(prefix="codeide-") as temp_dir:
        script_path = os.path.join(temp_dir, "main.py")
        stdout_path = os.path.join(temp_dir, "stdout.txt")
        stderr_path = os.path.join(temp_dir, "stderr.txt")
        with open(script_path, "w", encoding="utf-8", newline="\n") as script_file:
            script_file.write(source_code)

        started_at = time.perf_counter()

        with open(stdout_path, "w+", encoding="utf-8") as stdout_file, open(
            stderr_path, "w+", encoding="utf-8"
        ) as stderr_file:
            try:
                completed = subprocess.run(
                    [sys.executable, "-I", script_path],
                    cwd=temp_dir,
                    env=_build_subprocess_env(),
                    input=stdin,
                    stderr=stderr_file,
                    stdout=stdout_file,
                    text=True,
                    timeout=MAX_EXECUTION_SECONDS,
                )
            except subprocess.TimeoutExpired:
                duration_ms = int((time.perf_counter() - started_at) * 1000)
                stdout = _read_limited_output(stdout_file)
                stderr = _read_limited_output(stderr_file)
                if not stderr:
                    stderr = (
                        f"Execution timed out after {MAX_EXECUTION_SECONDS} seconds. "
                        "Try simplifying the code or reducing loops."
                    )

                return ExecutionResult(
                    stdout=stdout,
                    stderr=stderr,
                    returncode=None,
                    duration_ms=duration_ms,
                    timed_out=True,
                )

            stdout = _read_limited_output(stdout_file)
            stderr = _read_limited_output(stderr_file)

        duration_ms = int((time.perf_counter() - started_at) * 1000)
        return ExecutionResult(
            stdout=stdout,
            stderr=stderr,
            returncode=completed.returncode,
            duration_ms=duration_ms,
        )


def _build_subprocess_env() -> dict[str, str]:
    baseline_keys = (
        "COMSPEC",
        "PATH",
        "PATHEXT",
        "SYSTEMROOT",
        "TEMP",
        "TMP",
        "WINDIR",
    )
    env = {key: os.environ[key] for key in baseline_keys if key in os.environ}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUNBUFFERED"] = "1"
    return env


def _read_limited_output(file_obj) -> str:
    file_obj.flush()
    file_obj.seek(0)
    output = file_obj.read(MAX_OUTPUT_CHARACTERS + 1)
    if len(output) <= MAX_OUTPUT_CHARACTERS:
        return output

    return (
        f"{output[:MAX_OUTPUT_CHARACTERS]}\n\n"
        f"[output truncated to {MAX_OUTPUT_CHARACTERS} characters]"
    )
