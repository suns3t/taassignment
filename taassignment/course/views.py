import time
from django.contrib import messages
from django.shortcuts import render, render_to_response
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.contrib.auth import decorators
from taassignment.course.models import Course
from taassignment.users.models import User
from taassignment.course.forms import UploadFileForm, ErrorForm
from django.db.models import Count, Min
#from django.contrib.auth.models import User
from django.conf import settings
import csv


# Course view of the pag
def teacher_view_list(request):
    current_user  = request.user
    courses       = Course.objects.all().filter(faculties__username=current_user.username).annotate(total=Count('tas')).order_by('course_name')
#    courses       = Course.objects.all().annotate(total=Count('tas')).order_by('course_name')
    no_of_courses = len(courses)

    return render(request, "course/teacher_view_list.html", {
        "courses" : courses,
        "no_of_courses" : no_of_courses,
        "has_courses" : courses
        })

def error_message(request):
        form = ErrorForm()
        return render(request,'admin/error_message.html', {})

def request_csv_tas_upload(request,f):
    #    User.objects.filter(is_ta = True).delete()
    #    f = open(file,'r')
    for r in csv.reader(f, delimiter=',',quotechar='"'):
        user_exits = User.objects.all().filter(username=format(Oidn))
        Oidn = r
        try:
            if user_exists :
                user = User()
                user.username = format(*Oidn)
                user.is_ta  = 1
                user.is_active = 1
                user.save()

def request_csv_courses_upload(request,f):
#    course.objects.filter(is_faculty = True).delete()
#    f = open(file,'r')
    for r in csv.reader(f, delimiter=',',quotechar='"'):
        course_no, course_name, Oidn = r
        try:
            course_exits = course.objects.all().filter(course_no=course_no)
            user_exits = user.objects.all().filter(username=format(Oidn))
            if course_exists :
                course = Course()
                course.course_no = course_no
                course.course_name = format(course_name)
                course.save()
                user_exits = User.objects.all().filter(username=format(Oidn))
            if user_exists :
                user = User()
                user.username  = format(Oidn)
                user.is_faculty = 1
                user.is_active = 1
                user.save()
            if user_exists and course_exists:
                course.faculties.course_id  = course_no
                course.faculties.add(user)
                course.save()

    # Upload Courses
def upload_courses(request):
    global url
    url = '/admin/'
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #            form.save()
            request_csv_courses_upload(request,request.FILES['file'])
            return HttpResponseRedirect(url)
    else:
        form = UploadFileForm()
        return render(request,'admin/upload_courses_import.html', {'form': form})

# Upload Tas
def upload_tas(request):
    global url
    url = '/admin/'
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #            form.save()
            request_csv_tas_upload(request,request.FILES['file'])
            return HttpResponseRedirect(url)
    else:
        form = UploadFileForm()
        return render(request,'admin/upload_tas_import.html', {'form': form})



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
