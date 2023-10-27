from django.db import models
from accounts.models import User
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

    teacher = models.ForeignKey(to=User,on_delete=models.CASCADE)
    subject = models.ManyToManyField(Subject)
    room = models.ForeignKey(Room,on_delete=models.SET_NULL,null=True)
    teacher_profile_pic = models.ImageField(upload_to='teacher/profile_pic/',null=True,blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.teacher