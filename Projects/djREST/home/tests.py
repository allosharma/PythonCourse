from django.conf import settings
from django.test import TestCase

from .utils.readQuestions import read_questions


class QuestionPageTests(TestCase):
    def test_question_json_loads_latex_without_mangling_backslashes(self):
        file_path = settings.BASE_DIR / "home" / "utils" / "Questions.json"

        data = read_questions(file_path)

        question = data["physics_paper"][11]["question"]
        explanation = data["physics_paper"][12]["explanation"]
        self.assertIn(r"r_\alpha", question)
        self.assertIn(r"\cdot", explanation)

    def test_home_page_renders_question_sheet_with_radio_options(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Submit Test")
        self.assertContains(response, "Check Later")
        self.assertContains(response, "Previous")
        self.assertContains(response, "Next")
        self.assertContains(response, 'id="question-navigation"', html=False)
        self.assertContains(response, 'type="radio"', count=100, html=False)
        self.assertContains(response, 'data-nav-index="', count=25, html=False)
        self.assertContains(response, 'data-correct-answer="B"', html=False)
