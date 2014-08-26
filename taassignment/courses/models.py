from django.db import models
from taassignment.users.models import User
# Create your models here.

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    course_no = models.CharField(max_length=10, blank=False)
    section_no = models.CharField(max_length=10, blank=True)
    course_name = models.CharField(max_length=100, blank=False)
    faculties = models.ManyToManyField(User, related_name='faculties', blank=True)
    tas = models.ManyToManyField(User, related_name='tas', blank=True)
    max_tas = models.IntegerField()

    class Meta:
        db_table = "course"
        ordering = ('course_name',)
        permissions = (
            ("change_ta", "Can change TA in this course"),
        )

    def __str__(self):
        if self.section_no:
            return "%s-%s" % (self.course_no, self.section_no)
        else:
            return "%s" % self.course_no
