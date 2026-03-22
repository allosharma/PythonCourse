from home.models import *
from faker import Faker
import random

fake = Faker('en_IN')

def dbSeeder(records = 10) -> None:
    # college_name = [
    #     'IIT Delhi',
    #     'IIT Bombay',
    #     'IIT Madras',
    #     'IIT Kanpur',
    #     'IIT Kharagpur',
    #     'IIT Roorkee',
    #     'IIT Guwahati',
    #     'IIT Hyderabad'
    # ]
    colleges = list(College.objects.all())
    for i in range(records):
        name = fake.name()
        college = random.choice(colleges)
        email = fake.email()
        mobile_number = fake.phone_number()
        gender = random.choice(['Male', 'Female', 'Other'])
        age = random.randint(18, 30)
        date_of_birth = fake.date_of_birth()
        student_bio = fake.text()
        Student.objects.create(
            name=name,
            college=college,
            mobile_number=mobile_number,
            email=email,
            gender=gender,
            age=age,
            date_of_birth=date_of_birth,
            student_bio=student_bio
        )