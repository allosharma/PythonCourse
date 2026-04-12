from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    dob = models.DateField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name
    
    
class Book(models.Model):
    book_title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # published_date = models.DateField()

    def __str__(self):
        return self.title