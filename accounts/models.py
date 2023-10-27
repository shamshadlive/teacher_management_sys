from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,phone_number,password=None):
            
        user = self.model(
            
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self,first_name,last_name,phone_number,password):
        user = self.create_user(
                                first_name=first_name,
                                phone_number=phone_number,
                                last_name=last_name,
                                password=password,
                                )
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        
        user.save(using=self._db)
        return user
            

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=12,unique=True)
    
   
    
    #required field
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD  = 'phone_number'
    REQUIRED_FIELDS = ['first_name','last_name']
    
    objects = MyAccountManager()
    
    def __str__(self):
        return self.first_name
    
    def has_perm(self,perm,obj=None):
        return self.is_superuser
    
    def has_module_perms(self,add_label):
        return True
        