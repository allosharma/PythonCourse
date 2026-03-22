from django import forms
from home.models import Student as StudentModel

class Student(forms.Form):
    name = forms.CharField(max_length=100)
    age = forms.IntegerField()
    gender = forms.ChoiceField(choices=[
        ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], widget=forms.RadioSelect)
    phone_number = forms.CharField(max_length=15)
    email = forms.EmailField()
    bio = forms.CharField(widget=forms.Textarea, required=False)
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


# This way we can directly use the model to create the form, and it will automatically generate the fields based on the model's attributes.
# class Student(forms.ModelForm):
#     class Meta:
#         model = StudentModel
#         fields = '__all__' 
        # exclude = ['created_at', 'updated_at'] # This way we can exclude the fields which we don't want to show in the form.
        # field = ['name', 'age']