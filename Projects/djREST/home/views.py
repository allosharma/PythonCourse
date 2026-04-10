from pathlib import Path

from django.conf import settings
from django.shortcuts import render

from .utils.readQuestions import read_questions

FILE_PATH = Path(settings.BASE_DIR) / "home" / "utils" / "Questions.json"


def homePage(request):
    data = read_questions(FILE_PATH)
    questions = []

    for question in data.get("physics_paper", []):
        options = question.get("options", {})
        correct_answer = question.get("correct_answer", "")
        questions.append(
            {
                **question,
                "option_items": [
                    {"key": key, "text": value} for key, value in options.items()
                ],
            }
        )

    context = {
        "exam_title": data.get("exam_title", "JEE Question Bank"),
        "questions": questions,
        "total_questions": data.get("total_questions", len(questions)),
    }
    return render(request, "index.html", context)
