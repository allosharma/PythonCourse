from __future__ import annotations

import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

from .executor import MAX_EXECUTION_SECONDS, run_python_code
from .forms import CodeSubmissionForm


STARTER_CODE = """print("Hello from CodeIDE!")
name = input("What is your name? ")
print(f"Welcome, {name}")
"""


@require_GET
@ensure_csrf_cookie
def home(request):
    return render(
        request,
        "compiler/home.html",
        {
            "execution_timeout": MAX_EXECUTION_SECONDS,
            "starter_code": STARTER_CODE,
        },
    )


@require_POST
def run_code(request):
    payload, error_response = _get_payload(request)
    if error_response is not None:
        return error_response

    form = CodeSubmissionForm(payload)
    if not form.is_valid():
        return JsonResponse(
            {
                "ok": False,
                "message": _first_form_error(form),
                "field_errors": form.errors.get_json_data(),
            },
            status=400,
        )

    result = run_python_code(
        source_code=form.cleaned_data["code"],
        stdin=form.cleaned_data["stdin"],
    )

    return JsonResponse(
        {
            "ok": not result.timed_out and result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "duration_ms": result.duration_ms,
            "timed_out": result.timed_out,
        }
    )


def _get_payload(request):
    if request.content_type == "application/json":
        try:
            return json.loads(request.body.decode("utf-8")), None
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None, JsonResponse(
                {
                    "ok": False,
                    "message": "Request body must be valid JSON.",
                },
                status=400,
            )

    return request.POST, None


def _first_form_error(form: CodeSubmissionForm) -> str:
    for errors in form.errors.values():
        if errors:
            return errors[0]
    return "Please review the submitted code and try again."
