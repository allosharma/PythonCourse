from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from home.forms import Student
from home.models import Student as StudentModel, Contact
from django.db.models import Q
# Create your views here.

# def home(request):
#     return render(request, 'home/home.html')

def index(request):
    # print(5+7)
    emp = {'Alok': 30, 'Bob': 25, 'Charlie': 35}
    context = {'employees': emp}
    return render(request, 'index.html', context)

def contact(request):
    if request.method == 'POST':
        student_data = Student(request.POST)
        if student_data.is_valid():
            # Process the form data here (e.g., save to database, send email, etc.)
            # For now, we will just print the cleaned data to the console
            print(student_data.cleaned_data)

            StudentModel.objects.create(
                name=student_data.cleaned_data['name'],
                age=student_data.cleaned_data['age'],
                gender=student_data.cleaned_data['gender'],
                mobile_number=student_data.cleaned_data['phone_number'],
                email=student_data.cleaned_data['email'],
                student_bio = student_data.cleaned_data['bio'],
                date_of_birth=student_data.cleaned_data['dob']
            )

            messages.success(request, "Form submitted successfully!")
            return redirect('contact')

        return render(request, 'contact.html', {'form': student_data})

    return render(request, 'contact.html', {'form': Student()})

def dynamic_route(request, name):
    return HttpResponse(f"Hello, {name}! This is a dynamic route.")

def formPage(request):
    if request.method == 'POST':
        # print(request.POST)
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        file = request.FILES.get('file')
        print(f"Name: {name}, Age: {age}, Gender: {gender}, file: {file}") 
        Contact.objects.create(
            name=name,
            age=age,
            gender=gender,
            upload_file=file
        )
    context = {
        # 'form': Student()
    }
    return render(request, 'form.html', context)


def search_page(request):
    students = StudentModel.objects.all()

    search_query = request.GET.get('search')
    age_query = request.GET.get('select_age')
    if search_query:
        # similar to icontains , you can use startswith, endswith, exact, etc.
        # students = StudentModel.objects.filter(name__icontains=search_query)
        students = students.filter(
            Q(name__icontains = search_query) |
            Q(email__icontains = search_query) |
            Q(mobile_number__icontains = search_query) |
            Q(college__college_name__icontains = search_query) # assuming you have a related field 'college' in your StudentModel that points to a College model with a 'college_name' field
        )

    if age_query:
        if age_query == '1':
            students = students.filter(age__gte=15, age__lte=20).order_by('age')
        elif age_query == '2':
            students = students.filter(age__range=(21, 25)).order_by('age')
        elif age_query == '3':
            students = students.filter(age__range=(26, 30)).order_by('age')
    
    context = {
        'students': students,
        'search_query': search_query,
        'age_query': age_query
    }

    return render(request, 'search.html', context)
