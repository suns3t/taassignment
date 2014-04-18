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
    is_staff = models.BooleanField(default=False, blank=True) # True if this user is admin
    is_superuser = models.BooleanField(default=False, blank=True)

    USERNAME_FIELD = 'username'

    # Custom flags
    is_faculty = models.BooleanField(default=False, blank=True) # True if this user is a faculty member
    is_ta = models.BooleanField(default=False, blank=True) # True if this user is a TA

    objects = UserManager()

    class Meta:
        db_table = 'user'

    def __unicode__(self):
        if self.first_name:
            return u'%s %s' % (self.first_name, self.last_name)
        else:
            return u'%s' % (self.username)

    # Get full name of user
    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.first_name + " " + self.last_name

    # Grant faculty permission to change_ta
    def has_perm(self, perm, obj=None): 
        if (self.is_faculty and perm == 'course.change_ta') or self.is_staff:
            return True
        return False

    def has_module_perms(self, app_label):  return True


     
