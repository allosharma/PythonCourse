import json


def read_questions(file_path):
    with open(file_path, "r", encoding="utf-8") as questions_file:
        return json.load(questions_file)
