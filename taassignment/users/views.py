import csv

from django.shortcuts import render, get_object_or_404
from djangocas.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db import transaction
from django.conf import settings

from taassignment.utils import get_ldap_user_data
from taassignment.courses.models import Course
from taassignment.courses.forms import UploadFileForm
from taassignment.perm import admin_member_check

from .models import User
from .forms import UserForm

@user_passes_test(admin_member_check, login_url="/accounts/login")
def list_(request):
    users = User.objects.all()
    section = 'user-home'

    return render(request, 'users/list.html', {
        'users' : users,
        'section' : section,
    })

@user_passes_test(admin_member_check, login_url="/accounts/login")
def create(request):
    title = "Add New User"
    section = 'user-home'

    if request.POST:
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'New user is added!')
            return HttpResponseRedirect(reverse('users-list'))
    else:
        user_form = UserForm()

    return render(request, 'users/create.html', {
        'user_form' : user_form,
        'section' : section,
        'title' : title,
    })

@user_passes_test(admin_member_check, login_url="/accounts/login")
def edit(request, userid):
    user = get_object_or_404(User, pk=userid)
    title = "Edit Existing User"
    section = 'user-home'

    if request.POST:
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "User information saved!")
            return HttpResponseRedirect(reverse('users-list'))
    else:
        user_form = UserForm(instance=user)

    if user == request.user:
        user_form.fields.pop("is_staff")

    return render(request, 'users/create.html', {
        'user_form' : user_form,
        'title' : title,
        'section' : section,
    })

@user_passes_test(admin_member_check, login_url="/accounts/login")
def delete(request, userid):
    user = get_object_or_404(User, pk=userid)
    title = "Deleting User"
    section = 'user-home'

    if request.POST:
        courses = Course.objects.filter(faculties=user)
        for course in courses:
            if course.faculties.count() == 1:
                course.delete()
        user.delete()
        messages.success(request, "User is deleted!")
        return HttpResponseRedirect(reverse("users-list"))

@user_passes_test(admin_member_check, login_url="/accounts/login")
def clear_faculty(request):
    title = "Faculties"
    redirect_url = reverse("users-list")
    target_url = reverse("users-clear-faculty")
    section = 'user-home'

    if request.POST:
        no_of_faculties = 0
        faculties = User.objects.filter(is_faculty=True, is_staff=False)
        for faculty in faculties:
            courses = Course.objects.filter(faculties=faculty)
            for course in courses:
                if course.faculties.count() == 1:
                    course.delete()
            faculty.delete()
            no_of_faculties = no_of_faculties + 1
        if no_of_faculties > 0:
            messages.success(request, "%s faculties members deleted!" % no_of_faculties )
        else:
            messages.success(request, "No faculty members deleted!")

        return HttpResponseRedirect(redirect_url)

@user_passes_test(admin_member_check, login_url="/accounts/login")
def clear_tas(request):
    title = "TAs"
    redirect_url = reverse("users-list")
    target_url = reverse("users-clear-tas")
    section = 'user-home'

    if request.POST:
        no_of_tas = 0
        tas = User.objects.filter(is_ta=True, is_staff=False)
        for ta in tas:
            ta.delete()
            no_of_tas = no_of_tas + 1

        if no_of_tas > 0:
            messages.success(request, "%s TAs deleted!" % no_of_tas )
        else:
            messages.success(request, "No TA deleted!")

        return HttpResponseRedirect(redirect_url)

# Upload Tas
@user_passes_test(admin_member_check, login_url="/accounts/login")
def upload(request):
    error = None
    section = 'user-home'

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if  form.is_valid():
            try:
                with transaction.atomic():
                    _request_csv_tas_upload(request, request.FILES['file'])
            except (TypeError, ValueError) :
                error='Wrong file type/number of columns do not mach!'
            except Exception as e:
                error= '%s (%s)' % (e.message, type(e))
            else:  
                return HttpResponseRedirect(reverse("users-list"))
    else:
        form = UploadFileForm()

    return render(request,'users/upload.html', {
        'form': form, 
        'error': error,
        'section' : section
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
            user = User.objects.get(username=odin)
            user.is_ta = 1
            user.is_active = 1
            user.save()
        except User.DoesNotExist:
            first_name, last_name = get_ldap_user_data(odin)
            if first_name is not None:
                user = User()
                user.username = odin
                user.first_name = first_name
                user.last_name = last_name
                user.is_ta = 1
                user.is_active = 1
                user.save()
                count = count + 1
            else:
                invalid_users.append(odin) 

    if count:
        messages.success(request, "CSV file uploaded. %s new TAs added!" % count)

    if len(invalid_users) > 0:
        messages.warning(request, "There are some invalid Odin usernames: %s. They were not created." % ", ".join(map(str, invalid_users)))

