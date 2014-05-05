from django.contrib import admin
from taassignment.course.models import Course

# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    # This changes list form
    fields = ('course_no','course_name','faculties','tas')
    list_display = ('course_no','course_name','get_username','get_name','get_tas','teacher_link','tas_link')
    
    def get_tas(self, obj):
                return "\n".join([p.first_name+" "+p.last_name for p in obj.tas.all()])
    get_tas.short_description = "TAs Name"
    
    def get_username(self, obj):
                return obj.faculties.all().first().username
    get_username.short_description = "Username"

    def get_name(self, obj):
                return  obj.faculties.all().first().first_name+' '+obj.faculties.all().first().last_name
    get_name.short_description = "Teacher Name"
    
    def teacher_link(self,obj):
        return u'<a href="/admin/course/teachers/?username=%s">View Teachers</a>' % (obj.faculties.all().first().username) 
    teacher_link.allow_tags = True
    teacher_link.short_description = "Display"


    def tas_link(self,obj):
        return u'<a href="/admin/course/tas/?course=%s">View TAs</a>' % (obj.course_no) 
    tas_link.allow_tags = True
    tas_link.short_description = "Display"

admin.site.register(Course, CourseAdmin)
