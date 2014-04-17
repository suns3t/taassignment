from django.shortcuts import render
from taassignment.course.models import Course 
# Create your views here.

# Public view of the page, also act as homepage
def public_view_list(request):
	courses = Course.objects.all()
	no_of_course = Course.objects.count()

	return render(request, "course/public_view_list.html", {
		"courses" : courses,
		"has_courses" : no_of_course ,
	})