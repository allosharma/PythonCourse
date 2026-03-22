from django.db import models
from home.utils import generate_unique_slug

# Create your models here.

class College(models.Model):
    college_name = models.CharField(max_length=100)
    college_address = models.CharField(max_length=100)
    # established_year = models.IntegerField()

    def __str__(self):
        return self.college_name

class Student(models.Model):
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    name = models.CharField(max_length=100)
    college = models.ForeignKey(College, on_delete=models.CASCADE, null=True, blank=True)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField()
    gender = models.CharField(max_length=10, choices=gender_choices, default='Male')
    age = models.IntegerField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='student/profile_images/', null=True, blank=True)
    file = models.FileField(upload_to='student/files/', null=True, blank=True)
    student_bio = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Author(models.Model):
    author_name = models.CharField(max_length=100)
    # email = models.EmailField()
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    # It is used to return the string representation of the object. It is used in the admin panel and in the shell.
    def  __str__(self):
        return self.author_name

from django.db.models import CheckConstraint, Q
class Book(models.Model):
#     author = models.OneToOneField(Author, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book_name = models.CharField(max_length=100)
    published_date = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'AlokBooks' # It will change the name of the table in the database to 'Alok Books' instead of 'home_book'.
        ordering = ['published_date'] # It will order the books by published date in ascending order. Use '-published_date' for descending order.
        verbose_name = 'Book' # It will change the name of the model in the admin panel to 'Book' instead of 'Books'.
        verbose_name_plural = 'Books' # It will change the name of the model in the admin panel to 'Books' instead of 'Book'.
        unique_together = ['author', 'book_name'] # It will ensure that the combination of author and book name is unique in the database.
        indexes = [models.Index(fields=['author', 'published_date'])] # It will create an index on the combination of author and published date for faster queries.
        permissions = [
            ('can_publish', 'Can publish book')
        ]
        # constraints are used to add constraints to the model fields. In this case we are adding a check constraint to ensure that the price of the book is greater than or equal to 0.
        constraints = [
            models.CheckConstraint(
                condition=Q(price__gte=0),
                name="positive_price"
            )
        ]

    def __str__(self):
        return self.book_name

class Books2(Book):
    # This is an example of multi-table inheritance in Django. It will create a new table in the database for the Books2 model which will have a one-to-one relationship with the Book model. We can add additional fields to the Books2 model if needed.
    # additional_info = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        proxy = True # This will make the Books2 model a proxy model which means it will not create a new table in the database and it will use the same table as the Book model. We can use this to add additional methods to the Books2 model without changing the database schema.
        # It will pick the same table as the Book model and we can add additional methods to the Books2 model without changing the database schema. This is useful when we want to add additional functionality to the model without changing the database schema.
        ordering = ['-price']

class Brand(models.Model):
    brand_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='India')

    def __str__(self):
        return self.brand_name

class Products(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:  # Only generate slug if it doesn't exist to avoid changing it on every save.
            self.slug = generate_unique_slug(self.product_name, Products) # We are passing the model class to the utility function to check for uniqueness of the slug.
        return super().save(*args, **kwargs)

# We we can create skill manager to filter out the soft deleted records from the database. This way we can keep the records in the database for future reference and also we can restore them if needed.
class SkillManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_delete=False)

class Skills(models.Model):
    skill_name = models.CharField(max_length=100)
    # Soft delete implementation: Instead of deleting the record from the database, we can mark it as deleted by setting the is_delete field to True. This way we can keep the record in the database for future reference and also we can restore it if needed.
    is_delete = models.BooleanField(default=False)

    objects = SkillManager()
    new_objects = models.Manager() # This will allow us to access all the records including the soft deleted ones using Skills.new_objects.all()

    def __str__(self):
        return self.skill_name

class Person(models.Model):
    person_name = models.CharField(max_length=100)
    skills = models.ManyToManyField(Skills)

class Contact(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    upload_file = models.FileField(upload_to='contact/files/', null=True, blank=True)



# In the below case we are creating a parent class Human and two child classes Engineer and Doctor
# The child classes will inherit the fields of the parent class and we can also add additional fields to the child classes if needed. This is an example of multi-table inheritance in Django.
# I don't want this Human db to be created in the database, I just want to use it as a base class for the Engineer and Doctor models. For that we can use the abstract base class in Django by adding the Meta class with abstract = True in the Human model. This way the Human model will not be created in the database and we can still use it as a base class for the Engineer and Doctor models.
class Human(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)

    # Abstract base class: This is a base class which will not be created in the database. It is used to define common fields and methods for the child classes.
    class Meta:
        abstract = True

class Engineer(Human):
    tech_stack = models.CharField(max_length=100)

class Doctor(Human):
    specialization = models.CharField(max_length=100)