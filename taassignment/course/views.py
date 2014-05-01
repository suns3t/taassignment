from django.shortcuts import render, get_object_or_404
from django.contrib.auth import decorators
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from taassignment.course.models import Course 
from taassignment.users.models import User 
from .forms import CourseForm

def public_view_list(request):
    courses = Course.objects.all()
    no_of_course = Course.objects.count()

    return render(request, "course/public_view_list.html", {
        "courses" : courses,
        "has_courses" : no_of_course ,
    })

# Faculty home page
@decorators.permission_required('course.change_ta',raise_exception=True)
def faculty_view_list(request):
    courses = Course.objects.filter(faculties=request.user)
    no_of_course = courses.count()
    tas = User.objects.filter(is_ta=True)

    return render(request, "course/faculty_view_list.html", {
        "courses" : courses,
        "has_courses" : no_of_course,
        "tas" : tas,
    })

@decorators.login_required
def staff_add_course(request):
    title = "Add New Course"

    if request.POST:
        course_form = CourseForm(request.POST)
        if course_form.is_valid():
            course = course_form.save(commit=False)
            course.save()
            course_form.save_m2m()

            return HttpResponseRedirect(reverse('staff-home'))
    else:
        course_form = CourseForm()

    return render(request, 'admin/staff_add_course.html', {
        'course_form' : course_form,
        'title' : title,
    })

@decorators.login_required
def staff_edit_course(request, courseid):
    course = get_object_or_404(Course, pk=courseid)
    title = "Edit Existing Course"

    if request.POST:
        course_form = CourseForm(request.POST, instance=course)
        if course_form.is_valid():
            course = course_form.save(commit=False)
            course.save()
            course_form.save_m2m()

            return HttpResponseRedirect(reverse('staff-home'))
    else:
        course_form = CourseForm(instance=course)

    return render(request, 'admin/staff_add_course.html', {
        'course_form' : course_form,
        'title' : title,
    })

@decorators.login_required
def staff_delete_course(request, courseid):
    course = get_object_or_404(Course, pk=courseid)
    
    if request.POST:
        course.delete()
        return HttpResponseRedirect(reverse('staff-home'))

    return render(request, 'admin/staff_delete_dialog.html', {
        'course' : course,
    })
