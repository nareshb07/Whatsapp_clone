from django.db import models
import datetime

from django.utils import timezone

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from django.utils.translation import gettext_lazy as _


# Create your models here.
class CustomUserManager(BaseUserManager):

     def _create_user (self, email, password,first_name,last_name, **extra_fields):
     
         
        if not email:
            raise ValueError("The given email is invalid ")
        
        if not password:
            raise ValueError("password is not provided")
        
        email = self.normalize_email(email)

        user = self.model(email = email,first_name = first_name, last_name = last_name , **extra_fields)

        user.set_password(password)
        user.save(using = self._db)
        return user
     
     def create_user(self, email, password,first_name,last_name, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password,first_name,last_name, **extra_fields)

     def create_superuser(self, email, password,first_name,last_name, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password,first_name,last_name, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique= True, max_length=200)
    #username = models.CharField(unique=True,max_length=20)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    is_Follower = models.BooleanField(default=False)
    
    is_Creator = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    token = models.CharField(max_length = 200)

    objects = CustomUserManager()

    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name","last_name","username"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")



class Follower(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)

    def __str__(self) -> str:
        return self.user.email



class Creator(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
        
    def __str__(self) -> str:
        return self.user.email






from django.db import models
#from .models import User

# Create your models here.
"""
class UserProfileModel(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    name = models.CharField(blank=True, null=True, max_length=100)
    online_status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.first_name """


class ChatModel(models.Model):
    sender = models.CharField(max_length=100, default=None)
    message = models.TextField(null=True, blank=True)
    thread_name = models.CharField(null=True, blank=True, max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.message  

class ChatNotification(models.Model):
    chat = models.ForeignKey(to=ChatModel, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    is_seen = models.BooleanField(default=False)

    def __str__(self) -> str:
        #return self.user.username
        return self.user.first_name

