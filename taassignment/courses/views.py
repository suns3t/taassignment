import csv

from django.shortcuts import render, get_object_or_404
from djangocas.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db import transaction
from django.conf import settings

from taassignment.users.models import User
from taassignment.perm import faculty_member_check, admin_member_check, ta_member_check
from taassignment.utils import get_ldap_user_data

from .models import Course
from .forms import CourseForm, UploadFileForm, SelectionForm


@user_passes_test(admin_member_check, login_url="/accounts/login")
def list_(request):
    courses = Course.objects.all()
    section = 'course-home'

    return render(request, 'courses/list.html', {
        'courses' : courses,
        'section' : section,
    })

@user_passes_test(admin_member_check, login_url="/accounts/login")
def upload(request):
    error = None
    section = "course-home"

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if  form.is_valid():
            try:
                with transaction.atomic():
                    _request_csv_courses_upload(request, request.FILES['file'])
            except (TypeError, ValueError) :
                error='Wrong file type/number of columns do not mach!'
            except Exception as e:
                error= '%s (%s)' % (e.message, type(e))
            else:
                return HttpResponseRedirect(reverse("courses-list"))
    else:
        form = UploadFileForm()
    return render(request,'courses/upload.html', {
        'form': form, 
        'error': error,
        'section' : section,
    })

@user_passes_test(admin_member_check, login_url="/accounts/login")
def create(request):
    title = "Add New Course"
    section = "course-home"

    if request.POST:
        course_form = CourseForm(request.POST)
        if course_form.is_valid():
            course = course_form.save(commit=False)
            course.save()
            course_form.save_m2m()
            messages.success(request, "New course added!")

            return HttpResponseRedirect(reverse('courses-list'))
    else:
        course_form = CourseForm()

    return render(request, 'courses/create.html', {
        'course_form' : course_form,
        'title' : title,
        'section' : section,
    })

@user_passes_test(admin_member_check, login_url="/accounts/login")
def edit(request, courseid):
    course = get_object_or_404(Course, pk=courseid)
    title = "Edit Existing Course"
    section = "course-home"

    if request.POST:
        course_form = CourseForm(request.POST, instance=course)
        if course_form.is_valid():
            course = course_form.save(commit=False)
            course.save()
            course_form.save_m2m()
            messages.success(request, "Course information saved!")

            return HttpResponseRedirect(reverse('courses-list'))
    else:
        course_form = CourseForm(instance=course)

    return render(request, 'courses/create.html', {
        'course_form' : course_form,
        'title' : title,
        'section' : section,
    })

@user_passes_test(admin_member_check, login_url="/accounts/login")
def delete(request, courseid):
    course = get_object_or_404(Course, pk=courseid)
    section = "course-home"

    if request.POST:
        course.delete()

        messages.success(request, "Course is deleted!")
        return HttpResponseRedirect(reverse('courses-list'))

@user_passes_test(admin_member_check, login_url="/accounts/login")
def clear(request):
    courses = Course.objects.all()
    title = "Courses"
    redirect_url = reverse("courses-list")
    target_url = reverse("courses-clear")
    section = "course-home"

    if request.POST:
        courses.delete()

        messages.success(request, "All courses deleted!")
        return HttpResponseRedirect(redirect_url)

    return render(request, 'clear.html', {
        "title" : title,
        "redirect_url" : redirect_url,
        "target_url" : target_url,
        "section" : section,
    })

@user_passes_test(faculty_member_check, login_url='/accounts/login')
def change_tas(request):
    courses = Course.objects.filter(faculties=request.user)
    no_of_course = courses.count()
    tas = User.objects.filter(is_ta=True)
    section = "faculty-home"

    if request.POST:
        form = SelectionForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()          
            messages.success(request, "TA information updated.")
            return HttpResponseRedirect(request.get_full_path())
    else:
        form = SelectionForm(user=request.user)
    for course in courses:
        course.form_field = form[str(course.pk)]
    
    return render(request, "courses/change_tas.html", {
        "courses" : courses,
        "has_courses" : no_of_course,
        "section" : section,
    })

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
            first_name, last_name = get_ldap_user_data(odin)
            if first_name is not None:
                user = User()
                user.username  = odin
                user.first_name = first_name
                user.last_name = last_name
            else:
                invalid_users.append(odin + " for course " + course_no)

        try:
            course = Course.objects.get(course_no=course_no)
        except Course.DoesNotExist:
            course = Course()
            course.course_no = course_no
            course.course_name = course_name
            new_course = new_course + 1

        if user is not None and course is not None:
            user.is_faculty = 1
            user.is_active = 1
            user.save()
            course.save()
            course.faculties.add(user)
            course.save()

    if len(invalid_users) > 0:
        messages.warning(request, "There were invalid Odin usernames: %s." % ", ".join(map(str, invalid_users)))

    messages.success(request, "CSV file uploaded. %s new courses added!" % new_course)
