from django.db import models
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver
from PIL import Image
import os

# Create your models here.
class Student(models.Model):
    student_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, choices=[('M', 'Male'), ('F', 'Female')])
    student_id = models.CharField(max_length=10, null=True, blank=True)
    # roll = models.IntegerField()
    # city = models.CharField(max_length=100

    def __str__(self):
        return self.student_name

class ImageModel(models.Model):
    original_image = models.ImageField(upload_to='images/')
    small_tumbnail = models.ImageField(upload_to='images/thumbnails', null=True, blank=True)
    medium_thumbnail = models.ImageField(upload_to='images/thumbnails', null=True, blank=True)
    large_thumbnail = models.ImageField(upload_to='images/thumbnails', null=True, blank=True)


@receiver(post_save, sender=ImageModel)
def createThumbnails(sender, instance, created, **kwargs):
    if created: 
        sizes = {
            'mini': (50, 50),
            'small': (200, 200),
            'medium': (400, 400),
            'large': (600, 600)
        }
        for fields, size in sizes.items():
            img = Image.open(instance.original_image.path)
            img.thumbnail(size, Image.Resampling.LANCZOS)
            # thumb_name, thumb_extension = os.path.splitext(instance.original_image.name)
            thumb_name, thumb_extension = os.path.splitext(os.path.basename(instance.original_image.name))
            thumb_extension = thumb_extension.lower()
            thumb_name = f'{thumb_name}_{fields}{thumb_extension}'
            print(f'thumbnail name: {thumb_name}')
            thumb_path = os.path.join('images/thumbnails', thumb_name)
            # print(f'created thumbnail {thumb_path}') # os.path.join('images/thumbnails', thumb_path)
            img.save(thumb_path)
            # Set attribute in model instance object to store path of thumbnail image.
            setattr(instance, f'{fields}_thumbnail', thumb_path)

@receiver(post_save, sender=Student)    
def save_student(sender, instance, created, **kwargs):
    print(sender, instance, created)
    # If we don't pass created as paramater and check if created then instance.save() will recursively call save() method endlessly and will create infinite loop.
    # To avoid infinite loop we are checking if create then save()
    if created:
        instance.student_id = f'student-{instance.id}'
        instance.save()
        print('student saved')
        print(instance.student_name)
        print(instance.gender)
        print(instance.id)

post_save.connect(save_student, sender=Student)