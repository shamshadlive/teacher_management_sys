from django.db import models
from accounts.models import User
from django.core.exceptions import ValidationError

# Create your models here.

#room model 
class Room(models.Model):

    room_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.room_name

#subject model 
class Subject(models.Model):

    sub_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.sub_name

#teacher model 
class Teacher(models.Model):
    teacher_first_name = models.CharField(max_length=255)
    teacher_last_name = models.CharField(max_length=255)
    teacher_email = models.EmailField(max_length=100,unique=True)
    teacher_phone_number = models.CharField(max_length=12)
    # teacher_room = models.ForeignKey(Room,on_delete=models.SET_NULL,null=True)
    # teacher_subjects = models.ManyToManyField(Subject)
    teacher_room = models.CharField(max_length=10)
    teacher_subjects = models.CharField(max_length=255)

    teacher_profile_pic = models.ImageField(upload_to='teacher/profile_pic/',null=True,blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

        
        
        
    def __str__(self):
        return str(self.teacher_first_name)
    
class File(models.Model):
    file = models.FileField(upload_to='teacher/csv/')