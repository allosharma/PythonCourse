import json
from unittest import mock

from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from .executor import run_python_code


class CompilerViewTests(TestCase):
    def test_home_page_renders(self):
        response = self.client.get(reverse("compiler:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python Playground")
        self.assertContains(response, "Run code")

    def test_run_code_returns_stdout(self):
        response = self.client.post(
            reverse("compiler:run_code"),
            data=json.dumps({"code": "print('hello world')", "stdin": ""}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["stdout"], "hello world\n")
        self.assertEqual(payload["stderr"], "")

    def test_run_code_surfaces_python_errors(self):
        response = self.client.post(
            reverse("compiler:run_code"),
            data=json.dumps({"code": "raise ValueError('boom')", "stdin": ""}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertFalse(payload["ok"])
        self.assertIn("ValueError: boom", payload["stderr"])

    def test_run_code_requires_non_empty_source(self):
        response = self.client.post(
            reverse("compiler:run_code"),
            data=json.dumps({"code": "", "stdin": ""}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()["ok"])


class ExecutionServiceTests(SimpleTestCase):
    @mock.patch("compiler.executor.MAX_EXECUTION_SECONDS", new=0.1)
    def test_run_python_code_times_out(self):
        result = run_python_code("while True:\n    pass")

        self.assertTrue(result.timed_out)
        self.assertIsNone(result.returncode)
        self.assertIn("Execution timed out", result.stderr)
