from faker import Faker
from home.models import Person

def bulk_create_persons(num_persons):
    fake = Faker('en_IN')  # You can specify the locale for more realistic data
    persons = []
    for _ in range(num_persons):
        person = Person(
            name=fake.name(),
            email=fake.email(),
            age=fake.random_int(min=18, max=80)
        )
        persons.append(person)
    Person.objects.bulk_create(persons)
    print(f'{num_persons} persons created successfully.')

def bulk_update_persons():
    persons = Person.objects.all()
    for person in persons:
        person.age += 1  # Increment age by 1 for demonstration
    Person.objects.bulk_update(persons, ['age'])
    print(f'{len(persons)} persons updated successfully.')

def bulk_delete_persons():
    persons = Person.objects.filter(age__gt=50)  # Example: Delete persons older than 50
    count = persons.count()
    persons.delete()
    print(f'{count} persons deleted successfully.')