from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager

# Create your models here.
class User(AbstractBaseUser):
    """
    A custom user model.
    We will have flags to distiguish among admin, faculty and TA
    """
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True, db_index=True)
    email = models.EmailField(max_length=100)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, blank=True)
    is_staff = models.
     
