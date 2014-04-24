from django.shortcuts import render
from django.contrib.auth import decorators
from taassignment.course.models import Course
from django.db.models import Count, Min
#from django.contrib.auth.models import User
from django.conf import settings

# Course view of the pag
def teacher_view_list(request):
    current_user  = request.user
    courses       = Course.objects.all().filter(faculties__username=current_user.username).annotate(total=Count('tas')).order_by('course_name')
    no_of_courses = len(courses)
    
    return render(request, "course/teacher_view_list.html", {
		"courses" : courses,
        "no_of_courses" : no_of_courses,
        "has_courses" : courses
	})



# Course view of the pag
def course_teacher_view_list(request):
    courses       = Course.objects.all().filter(faculties__username=request.GET['username']).annotate(total=Count('tas')).order_by('course_name')
    no_of_courses = len(courses)
    
    return render(request, "course/course_tas_view_list.html", {
		"courses" : courses,
        "no_of_courses" : no_of_courses,
        "has_courses" : courses
	})


# Course view of the pag
def course_tas_view_list(request):
    courses       = Course.objects.all().filter(course_no=request.GET['course']).annotate(total=Count('tas')).order_by('course_name')
    no_of_courses = len(courses)
    
    return render(request, "course/course_tas_view_list.html", {
		"courses" : courses,
        "no_of_courses" : no_of_courses,
        "has_courses" : courses
	})


# Public view of the page, also act as homepage
def public_view_list(request):
    current_user  = request.user
    courses       = Course.objects.all().annotate(total=Count('tas')).order_by('course_name')
 #   courses       = Course.objects.all().filter(faculties__username=current_user.username).annotate(total=Count('tas')).order_by('course_name')
    no_of_courses = len(courses)
    
    return render(request, "course/public_view_list.html", {
		"courses" : courses,
        "no_of_courses" : no_of_courses,
        "has_courses" : courses
	})

# Faculty home page
@decorators.permission_required('course.change_ta',raise_exception=True)
def faculty_view_list(request):
    courses = Course.objects.filter(faculties=request.user)
    no_of_courses = len(courses)

    return render(request, "course/public_view_list.html", {
        "courses" : courses,
        "has_courses" : no_of_course,
    })
