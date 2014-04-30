from django.db import models
from taassignment.users.models import User 
# Create your models here.


class Course(models.Model):

	id = models.AutoField(primary_key=True)
	course_no = models.CharField(max_length=10, blank=False)
	course_name = models.CharField(max_length=100, blank=False)
	faculties = models.ManyToManyField(User, related_name='faculties', blank=True)
	tas = models.ManyToManyField(User, related_name='tas', blank=True)

	class Meta:
		ordering = ('course_name',)
        permissions = (
            ("change_ta", "Can change TA in this course"),
        )
