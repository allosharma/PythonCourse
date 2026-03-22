from faker import Faker
from home.models import Author, Book


def seed_author():
    fake = Faker('en_IN')  # You can specify the locale for more relevant data

    # Create 5 authors
    for _ in range(5):
        author_name = fake.name()
        Author.objects.create(author_name=author_name)

    print("Author seeding completed!")

def seed_book():
    fake = Faker('en_IN')  # You can specify the locale for more relevant data

    # Create 10 authors and books
    for _ in range(10):
        book_name = fake.sentence(nb_words=4)
        published_date = fake.date_between(start_date='-20y', end_date='today')
        price = round(fake.random_number(digits=2), 2)
        author = Author.objects.order_by('?').first()  # Randomly select an existing author
        Book.objects.create(author=author, book_name=book_name, published_date=published_date, price=price)

    print("Book seeding completed!")

# To seed the database, you can do following in Django shell:
# >>> python manage.py shell
# >>> from home.seed_author_book import seed_author, seed_book
# >>> seed_author()
# >>> seed_book()