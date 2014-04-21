from django.shortcuts import render
from django.contrib.admin.views import decorators

from taassignment.course.models import Course
from taassignment.users.models import User

# Create your views here.
@decorators.staff_member_required
def staff_view_list(request):
    courses = Course.objects.filter(id__lt=5)
    tas = User.objects.filter(is_ta=True)
    
    return render(request, 'admin/staff_view_list.html', {
        'courses' : courses,
        'tas' : tas,
        })


