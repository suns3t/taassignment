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
from taassignment.users.forms import SelectionForm
import csv

import ldap
from django.conf import settings


# Upload Courses
@user_passes_test(admin_member_check, login_url="/accounts/login")
def upload_courses(request):
    error = None
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if  form.is_valid():
            try:
                with transaction.atomic():
                    _request_csv_courses_upload(request, request.FILES['file'])
            except (TypeError, ValueError) :
                error='Wrong file type, number of columns do not mach!'
            except Exception as e:
                error= '%s (%s)' % (e.message, type(e))
            else:
                return HttpResponseRedirect(reverse("staff-home-courses"))
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
                    _request_csv_tas_upload(request, request.FILES['file'])
            except (TypeError, ValueError) :
                error='Wrong file type, number of columns do not mach!'
            except Exception as e:
                error= '%s (%s)' % (e.message, type(e))
            else:  
                return HttpResponseRedirect(reverse("staff-home-users"))
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
        form = SelectionForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()          
            messages.success(request, "TA information is updated.")
            return HttpResponseRedirect(request.get_full_path())
    else:
        form = SelectionForm(user=request.user)
    for course in courses:
        course.form_field = form[str(course.pk)]
    
    return render(request, "course/faculty_view_list.html", {
        "courses" : courses,
        "has_courses" : no_of_course,
        })

@user_passes_test(admin_member_check, login_url="/accounts/login")
def staff_add_course(request):
    title = "Add New Course"

    if request.POST:
        course_form = CourseForm(request.POST)
        if course_form.is_valid():
            course = course_form.save(commit=False)
            course.save()
            course_form.save_m2m()
            messages.success(request, "New course is added!")

            return HttpResponseRedirect(reverse('staff-home-courses'))
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
            messages.success(request, "Course information is saved!")

            return HttpResponseRedirect(reverse('staff-home-courses'))
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

        messages.success(request, "Course is deleted!")
        return HttpResponseRedirect(reverse('staff-home-courses'))

    return render(request, 'admin/staff_delete_dialog.html', {
        'course' : course,
    })

@user_passes_test(admin_member_check, login_url="/accounts/login")
def staff_delete_all_courses(request):
    courses = Course.objects.all()
    title = "Courses"
    redirect_url = '/admin/list_courses'
    target_url = '/admin/delete_all_courses'

    if request.POST:
        courses.delete()

        messages.success(request, "All courses are deleted!")
        return HttpResponseRedirect(redirect_url)

    return render(request, 'admin/staff_delete_all_template.html', {
        "title" : title,
        "redirect_url" : redirect_url,
        "target_url" : target_url,
        })

def _request_csv_tas_upload(request, f):
    count = 0
    invalid_users = []
    reader = csv.reader(f.read().splitlines())
    next(reader, None) # skip the headers
    for r in reader:
        if len(r) != 1: raise ValueError 
        odin = r[0].strip()
        try:
            user_exists = User.objects.get(username=odin)
        except User.DoesNotExist:
            first_name, last_name = _get_ldap_user_data(odin)
            if first_name is not None:
                user = User()
                user.username = odin
                user.first_name = first_name
                user.last_name = last_name
                user.is_ta  = 1
                user.is_active = 1
                user.save()
                count = count + 1
            else:
                invalid_users.append(odin) 

    if count:
        messages.success(request, "CSV file is uploaded. %s new TAs are added!" % count)
    else:
        messages.warning(request, "TAs are already exist! No new TAs are created")

    if len(invalid_users) > 0:
        messages.warning(request, "There are some invalid Odin usernames: %s. Please correct it and submit the file again!" % ", ".join(map(str, invalid_users)))

def _request_csv_courses_upload(request, f):
    new_course = 0
    invalid_users = []
    
    reader = csv.reader(f.read().splitlines())
    next(reader, None) # skip the headers
    for r in reader:
        user = None
        course = None
        course_no, course_name, odin = [item.strip() for item in r] # IndexError or PackingError
        try:
            user = User.objects.get(username=odin)
        except User.DoesNotExist:
            first_name, last_name = _get_ldap_user_data(odin)
            if first_name is not None:
                user = User()
                user.username  = odin
                user.first_name = first_name
                user.last_name = last_name
                user.is_faculty = 1
                user.is_active = 1
            else:
                invalid_users.append(odin)

        try:
            course = Course.objects.get(course_no=course_no)
        except Course.DoesNotExist:
            course = Course()
            course.course_no = course_no
            course.course_name = course_name
            new_course = new_course + 1
        
        if user is not None and course is not None:
            user.save()
            course.save()
            course.faculties.add(user)
            course.save()

    if len(invalid_users) > 0:
        messages.warning(request, "There are some invalid Odin usernames: %s. Please correct it and submit the file again!" % ", ".join(map(str, invalid_users)))
    
    new_course = new_course - len(invalid_users)
    if new_course:
        messages.success(request, "CSV file is uploaded. %s new courses are added!" % new_course)
    else:
        messages.warning(request, "Courses uploaded are already exist! No new courses are created")

def _get_ldap_user_data(username):
    try:
        # Check if this username is an valid Odin username
        ld = ldap.initialize(settings.LDAP_URL)
        ld.simple_bind_s()
        results = ld.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "uid=" + username)
        record = results[0][1]
    except IndexError:
        return None, None

    cn = record['cn']
    parts = cn[0].split(" ")
    first_name = parts[0]
    last_name = " ".join(parts[1:])
    return first_name, last_name