from django.shortcuts import render, get_object_or_404
from djangocas.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from taassignment.course.models import Course
from taassignment.users.models import User
from .forms import UserForm
from taassignment.perm import admin_member_check

# Create your views here.
@user_passes_test(admin_member_check, login_url="/accounts/login")
def staff_courses_view_list(request):
    courses = Course.objects.all()
    section = 'course-home'

    return render(request, 'admin/staff_course_view_list.html', {
        'courses' : courses,
        'section' : section,
    })

@user_passes_test(admin_member_check, login_url="/accounts/login")
def staff_users_view_list(request):
    users = User.objects.all()
    section = 'user-home'

    return render(request, 'admin/staff_user_view_list.html', {
        'users' : users,
        'section' : section,
    })



@user_passes_test(admin_member_check, login_url="/accounts/login")
def staff_add_user(request):
    title = "Add New User"
    section = 'user-home'

    if request.POST:
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'New user is added!')
            return HttpResponseRedirect(reverse('staff-home-users'))
    else:
        user_form = UserForm()

    return render(request, 'admin/staff_add_user.html', {
        'user_form' : user_form,
        'section' : section,
        'title' : title,
    })

@user_passes_test(admin_member_check, login_url="/accounts/login")
def staff_edit_user(request, userid):
    user = get_object_or_404(User, pk=userid)
    title = "Edit Existing User"
    section = 'user-home'

    if request.POST:
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "User information is saved!")
            return HttpResponseRedirect(reverse('staff-home-users'))
    else:
        user_form = UserForm(instance=user)

    return render(request, 'admin/staff_add_user.html', {
        'user_form' : user_form,
        'title' : title,
        'section' : section,
    })

@user_passes_test(admin_member_check, login_url="/accounts/login")
def staff_delete_user(request, userid):
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
        return HttpResponseRedirect(reverse("staff-home-users"))

@user_passes_test(admin_member_check, login_url="/accounts/login")
def staff_delete_all_faculties(request):
    title = "Faculties"
    redirect_url = '/admin/list_users'
    target_url = '/admin/delete_all_faculties'
    section = 'user-home'

    if request.POST:
        no_of_faculties = 0
        faculties = User.objects.filter(is_faculty=True)
        for faculty in faculties:
            if not faculty.is_staff:
                courses = Course.objects.filter(faculties=faculty)
                for course in courses:
                    if course.faculties.count() == 1:
                        course.delete()
                faculty.delete()
                no_of_faculties = no_of_faculties + 1
        if no_of_faculties > 0:
            messages.success(request, "%s faculties members are deleted!" % no_of_faculties )
        else:
            messages.success(request, "No faculty member is deleted!")

        return HttpResponseRedirect(redirect_url)

    return render(request, 'admin/staff_delete_all_template.html', {
        "title" : title,
        "redirect_url" : redirect_url,
        "target_url" : target_url,
        'section' : section,
        })

@user_passes_test(admin_member_check, login_url="/accounts/login")
def staff_delete_all_tas(request):
    title = "TAs"
    redirect_url = '/admin/list_users'
    target_url = '/admin/delete_all_tas'
    section = 'user-home'

    if request.POST:
        no_of_tas = 0
        tas = User.objects.filter(is_ta=True)
        for ta in tas:
            if not ta.is_staff:
                ta.delete()
                no_of_tas = no_of_tas + 1

        if no_of_tas > 0:
            messages.success(request, "%s TAs are deleted!" % no_of_tas )
        else:
            messages.success(request, "No TA is deleted!")

        return HttpResponseRedirect(redirect_url)

    return render(request, 'admin/staff_delete_all_template.html', {
        "title" : title,
        "redirect_url" : redirect_url,
        "target_url" : target_url,
        'section' : section,
        })
