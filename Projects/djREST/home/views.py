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



from rest_framework.decorators import api_view
from rest_framework.response import Response

# DRF API view for the API endpoint
@api_view(['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def apiHome(request):
    sudents = [
        {"id": 1, "name": "Alice", "age": 20},
        {"id": 2, "name": "Bob", "age": 22},
        {"id": 3, "name": "Charlie", "age": 21},
        ]
    data = {
        "message": "Welcome to the API endpoint!",
        "status": "success",
        "students": sudents,
        "method": f"Request method: {request.method}",
    }
    return Response(data)

from home.models import Student

@api_view(['POST'])
def create_api_record(request):
    if request.method == 'POST':
        # print(request.data)  # You can access the posted data here
        name = request.data.get('name')
        dob = request.data.get('dob')
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        student = Student(name=name, dob=dob, email=email, phone_number=phone_number)
        student.save()
        return Response({
            "message": "Record created successfully!",
            'status': "success",
            "student": {
                "name": student.name,
                "dob": student.dob,
                "email": student.email,
                "phone_number": student.phone_number,
            }
            }
        )
    return Response({"error": "Invalid request method."}, status=400)


@api_view(['GET'])
def get_students(request):
    students = Student.objects.all().order_by('id')
    student_data = [
        {
            "id": student.id,
            "name": student.name,
            "dob": student.dob,
            "email": student.email,
            "phone_number": student.phone_number,
        }
        for student in students
    ]
    return Response({"students": student_data})


@api_view(['DELETE'])
def delete_student(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
        student.delete()
        return Response({"message": "Student deleted successfully."})
    except Student.DoesNotExist:
        return Response({"error": "Student not found."}, status=404)