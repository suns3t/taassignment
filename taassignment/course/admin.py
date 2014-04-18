from django.contrib import admin
from taassignment.course.models import Course

# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    # This changes list form
    list_display = ('course_no','course_name')

admin.site.register(Course, CourseAdmin)
