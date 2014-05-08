import os
from django.db import transaction
from datetime import datetime 
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from django.core.urlresolvers import reverse
from django.contrib import messages

from djangocas.decorators import user_passes_test
from taassignment.perm import faculty_member_check, admin_member_check, ta_member_check

from taassignment.course.models import Course 
from taassignment.users.models import User 
from .forms import CourseForm
from django.http import HttpResponseRedirect
from taassignment.course.models import Course
from taassignment.users.models import User
from taassignment.course.forms import UploadFileForm
from django.db.models import Count, Min
from django.conf import settings
from .forms import CourseForm
import csv



# Upload Courses
@user_passes_test(admin_member_check, login_url="/accounts/login")
def upload_courses(request):
    error = None
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if  form.is_valid():
            try:
                with transaction.atomic():
                    _request_csv_courses_upload(request.FILES['file'])
            except (TypeError, ValueError) :
                error='Wrong file type, number of columns do not mach!'
            except Exception as e:
                error= '%s (%s)' % (e.message, type(e))
            else:
                return HttpResponseRedirect(reverse("staff-home"))
    else:
        form = UploadFileForm()
    return render(request,'admin/upload_courses_import.html', {'form': form, "error": error})


# Upload Tas
@user_passes_test(admin_member_check, login_url="/accounts/login")
def upload_tas(request):
    error = None
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if  form.is_valid():
            try:
                with transaction.atomic():
                    _request_csv_tas_upload(request.FILES['file'])
            except (TypeError, ValueError) :
                error='Wrong file type, number of columns do not mach!'
            except Exception as e:
                error= '%s (%s)' % (e.message, type(e))
            else:  
                return HttpResponseRedirect(reverse("staff-home"))
    else:
        form = UploadFileForm()
    return render(request,'admin/upload_tas_import.html', {'form': form, "error": error})


# Public view of the page, also act as homepage
def public_view_list(request):
    courses = Course.objects.all()
    no_of_course = Course.objects.count()

    return render(request, "course/public_view_list.html", {
        "courses" : courses,
        "has_courses" : no_of_course ,
    })


@user_passes_test(faculty_member_check, login_url='/accounts/login')
def faculty_view_list(request):
    courses = Course.objects.filter(faculties=request.user)
    no_of_course = courses.count()
    tas = User.objects.filter(is_ta=True)

    if request.POST:
        try:
            for course in courses:
                courseid = course.id 
                tag = 'tas_' + str(courseid)
                if request.POST.getlist(tag):
                    new_tas_id = request.POST.getlist(tag)
                    old_tas_id = User.objects.filter(tas__id=courseid)

                    for old_ta in old_tas_id:
                        course.tas.remove(old_ta)
                    for new_ta in new_tas_id:
                        course.tas.add(User.objects.get(id=new_ta))
                    
            messages.success(request, "TA information is updated.")
            
        except:
            pass

    return render(request, "course/faculty_view_list.html", {
        "courses" : courses,
        "has_courses" : no_of_course,
        "tas" : tas,
        })


def _request_csv_tas_upload(f):
    for r in csv.reader(f,delimiter=",",quoting=csv.QUOTE_NONNUMERIC):
        if len(r) != 1: raise ValueError 
        odin = r[0].strip()
        try:
            user_exists = User.objects.get(username=odin)
        except User.DoesNotExist:
            user = User()
            user.username = odin
            user.is_ta  = 1
            user.is_active = 1
            user.save()

def _request_csv_courses_upload(f):
    for r in csv.reader(f,delimiter=",",quoting=csv.QUOTE_NONNUMERIC):
        course_no, course_name, odin = [item.strip() for item in r] # IndexError or PackingError
        try:
            course = Course.objects.get(course_no=course_no)
        except Course.DoesNotExist:
            course = Course()
            course.course_no = course_no
            course.course_name = course_name
            course.save()

        try:
            user = User.objects.get(username=odin)
        except User.DoesNotExist:
            user = User()
            user.username  = odin
            user.is_faculty = 1
            user.is_active = 1
            user.save()

        course.faculties.course_id  = course_no
        course.faculties.add(user)
        course.save()



@user_passes_test(admin_member_check, login_url="/accounts/login")
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

@user_passes_test(admin_member_check, login_url="/accounts/login")
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

@user_passes_test(admin_member_check, login_url="/accounts/login")
def staff_delete_course(request, courseid):
    course = get_object_or_404(Course, pk=courseid)
    
    if request.POST:
        course.delete()
        return HttpResponseRedirect(reverse('staff-home'))

    return render(request, 'admin/staff_delete_dialog.html', {
        'course' : course,
    })
