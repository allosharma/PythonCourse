from rest_framework import serializers
from home.models import Student

#Model Serializer for Student model
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        # fields = ['id', 'name', 'dob', 'email', 'phone_number']
        fields = '__all__'
        # exclude = ['id', 'dob']
        
        
#Basic Serializer for Books model   
class BookSerializer(serializers.Serializer):
    book_title = serializers.CharField(max_length=200)
    author = serializers.CharField(max_length=100)
    price = serializers.DecimalField(max_digits=6, decimal_places=2)